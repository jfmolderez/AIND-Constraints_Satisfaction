#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 13 10:28:40 2017

@author: jfm
"""

from sympy.core import symbols
from sympy import *
#from sympy.abc import x, y
from sympy.logic.boolalg import *
from util import constraint

 

a, b = symbols("a b") # symbols for 2 columns
k,l = symbols("k l") # symbols for 2 indexes

diffRow = constraint("diffRow",Ne(a,b))
diffDiag = constraint("diffDiag", Ne(abs(a - b), abs(k - l)))
N = 10
_vars = symbols("_vars:" + str(N))
#print(_vars)
constraints = {x: set() for x in _vars}
domains = {x : set(range(N)) for x in _vars}
indexes = [(i,j) for i in range(N) for j in range(N) if i != j]
for (i, j) in indexes :
    constraints[_vars[i]].add(diffRow.subs({a:_vars[i],b:_vars[j]}))
    constraints[_vars[j]].add(diffDiag.subs({a:_vars[i], b:_vars[j], k:i, l:j}))



    
#print(constraints[_vars[0]])
#print(set([v for cstr in constraints[_vars[0]] for v in cstr.free_symbols if v != _vars[0]]))
    
def revise(var1, var2, constraint):
    revised = False
    for x in set(domains[var1]) :
        if all([constraint.subs({var1:x,var2:y}) == False for y in domains[var2]]) :
            domains[var1].remove(x)
            revised = True
            
    return revised

print("domain of {} before revise : {}".format(_vars[0],domains[_vars[0]]))
cstr = list(constraints[_vars[0]])[5]
domains[_vars[9]]= {9}
print("revising constraint : {}".format(cstr))
print("free variables in constraint: {} ".format(cstr.free_symbols))
revised = revise(_vars[0], _vars[9], cstr)
print("domain of {} has been revised: {}!".format(_vars[0],revised))
print(domains[_vars[0]])