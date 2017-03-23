#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 15 15:48:08 2017

@author: jfm
"""
import matplotlib as mpl
import matplotlib.pyplot as plt

from util import constraint, displayBoard
from sympy import *
from IPython.display import display

a,b = symbols("a b")
i, j = symbols("i j")

diffRow = constraint("diffRow",Ne(a,b))
diffDiag = constraint("diffDiag",Ne(abs(a - b), abs(i - j)))

class NQueensCSP :
    
    def __init__(self, N) :
        _vars = symbols("_vars:" + str(N))
        _domain = set(range(N))
        self.size = N
        self.variables = _vars
        self.domains = {v: set(_domain) for v in _vars}
        self._constraints = {x: set() for x in _vars}
        
        indexes = set([tuple(sorted([i,j])) for i in range(N) for j in range(N) if i != j])
        for k, l in indexes : 
            self._constraints[_vars[k]].add(diffRow.subs({a:_vars[k],b:_vars[l]}))
            self._constraints[_vars[l]].add(diffRow.subs({a:_vars[k],b:_vars[l]}))
            self._constraints[_vars[k]].add(diffDiag.subs({a:_vars[k],b:_vars[l],i:k,j:l}))
            self._constraints[_vars[l]].add(diffDiag.subs({a:_vars[k],b:_vars[l],i:k,j:l}))
            
    @property
    def constraints(self):
        """Read-only list of constraints -- cannot be used for evaluation """
        constraints = set()
        for _cons in self._constraints.values():
            constraints |= _cons
        return list(constraints)
    
    def is_complete(self,assignment):
        return (len(assignment) == self.size)
    
    def is_consistent(self, var, value, assignment):
        for constraint in self._constraints[var]:
            constraint_assigned = constraint.subs(assignment)
            if not(constraint_assigned.subs(var,value)):
                return False
        return True
    
    def inference(self, var, value):
        print("inference - var: {} - value: {}".format(var,value))
        inferences = {}
        arcs = self._constraints[var]
        for arc in arcs :
            neighbour = [v for v in arc.free_symbols if v != var][0] # binary constraints : only 1 neighbour
            print("inference - arc : {} - neighbour : {}".format(arc,neighbour))
            vals = set(self.domains[neighbour])
            print("inference - domain[{}] : {}".format(neighbour,vals))
            for val in vals:
                if not(arc.subs({var:value, neighbour:val})):
                    self.domains[neighbour].remove(val)
                    print("inference - Removed val {} from domain of neighbour {}".format(val, neighbour))
                    if len(self.domains[neighbour]) == 1 :
                        inferences[neighbour] = val
                    else :
                        if len(self.domains[neighbour]) == 0 :
                            return None
        return inferences

    def show(self, assignment):
        """Display a chessboard with queens drawn in the locations specified by an
        assignment
        
        Parameters
        ----------
        assignment : dict(sympy.Symbol: Integer)
            A dictionary mapping CSP variables to row assignment of each queen
            
        """
        locations = [(i, assignment[j]) for i, j in enumerate(self.variables)
                     if assignment.get(j, None) is not None]
        displayBoard(locations, self.size)  
    
def select(csp, assignment):
    sorted_vars = sorted(csp.variables,key =lambda var: len(csp.domains[var]))
    for var in sorted_vars :
        if var not in assignment :
            return var
    return None

def order_values(var, assignment, csp):
    """Select the order of the values in the domain of a variable for checking during search;
    the default is lexicographically.
    """
    # TODO (Optional): Implement a more sophisticated search ordering routine from AIMA
    return csp.domains[var]

def backtracking_search(csp):
    """Helper function used to initiate backtracking search """
    return backtrack({}, csp)

def backtrack(assignment, csp):

    if csp.is_complete(assignment):
        return assignment
    
    var = select(csp, assignment)
    print("current assignment : {}".format(assignment))
    print("selected var : {}".format(var))

    values = set(order_values(var,assignment, csp))
    for value in values:
        domains = dict(csp.domains) # the domains are reduced by inference method !!!!
        if csp.is_consistent(var, value, assignment):
            assignment[var] = value
            print("current assignment (augmented) : {}".format(assignment))
            inferences = csp.inference(var,value) # side effect : reduction of the domains !!!
            print("inferences following assignment of {} to {} : {}".format(value, var, inferences))
            if inferences != None :
                assignment.update(inferences)
                result = backtrack(assignment, csp) 
                if result :
                    return result
        vs = [var]
        if inferences :
            vs = vs + list(inferences.keys())
        for v in vs :
            if v in assignment.keys():
                del assignment[v]
        csp.domains = domains
        
    return None

