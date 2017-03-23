#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 15 12:46:03 2017

@author: jfm
"""

from sympy.core import symbols
from sympy import *
from sympy.abc import x, y
from sympy.logic.boolalg import *
from util import constraint

N = 2
a, b = symbols("a b")  
diffRow = constraint("diffRow",Ne(a,b))

vars = symbols("vars:" + str(N))

constraints = {x: set() for x in vars}
domains = {x : set(range(N)) for x in vars}
indexes = [(i,j) for i in range(N) for j in range(N) if i != j]
for (i, j) in indexes :
    constraints[vars[i]].add(diffRow.subs({a:vars[i],b:vars[j]}))



def revise(var1, var2, constraint):
    revised = False
    for x in set(domains[var1]) :
        if all([constraint.subs({var1:x,var2:y}) == False for y in domains[var2]]) :
            domains[var1].remove(x)
            revised = True            
    return revised

assignment = {vars[0]: 0}

def inference(var, value) :
    inferences = {}
    arcs = constraints[var]
    
    for arc in arcs :
        neighbour = [v for v in arc.free_symbols if v != var][0]
        vals = domains[neighbour]
        if not(arc.subs

#print("domain of {} before revise : {}".format(vars[0],domains[vars[0]]))
#cstr = list(constraints[vars[0]])[5]
#domains[vars[9]]= {9}
#print("revising constraint : {}".format(cstr))
#print("free variables in constraint: {} ".format(cstr.free_symbols))
#revised = revise(vars[0], vars[9], cstr)
#print("domain of {} has been revised: {}!".format(vars[0],revised))
#print(domains[_vars[0]])