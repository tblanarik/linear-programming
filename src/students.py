"""
My solution to a question asked on Reddit r/sysor using PuLP

>>> https://www.reddit.com/r/sysor/comments/5w6nvf/algorithm_formulation_for_an_assignment_problem/
>>> I'm trying to formulate an optimization equation for a scenario.
>>> the objective is to maximize diversity in creating groups with 3-4 individuals in a class of 96 students.
>>> So basically it's an assignment problem.
>>> There are 4 diversity criteria which all of them are Boolean.
>>> I'm a bit rust on my linear programming skills. Anyone could help me with this problem or an example of such problem?
>>> It would be much appreciated.
>>> Cheers!
"""

import pulp
import numpy as np
from math import ceil
import random

n_students = 201
n_characteristics = 8
group_max_size = 4
group_min_size = 3
n_groups = ceil(n_students / group_max_size)

students = np.random.choice((0,1), (n_students, n_characteristics))

prob = pulp.LpProblem("Groups")

# No student can be in two groups
group_assignments = []
for i in range(n_students):
    tmp = []
    for k in range(n_groups):
        tmp.append(pulp.LpVariable("s_%i_%i" % (i, k), lowBound=0, upBound=1, cat='Binary'))
    group_assignments.append(tmp)
    prob += pulp.lpSum(tmp) == 1
    
# All groups must have 3-4 students
for k in range(n_groups):
    prob += pulp.lpSum([group_assignments[i][k] for i in range(n_students)]) <= group_max_size
    prob += pulp.lpSum([group_assignments[i][k] for i in range(n_students)])  >= group_min_size
    
# Diversity Constraint    
for k in range(n_groups):
    for j in range(n_characteristics):
        char_column = pulp.LpAffineExpression()
        for i in range(n_students):
            char_column += students[i][j] * group_assignments[i][k]
        prob += char_column >= 1
        
prob.solve()

for i in range(n_students):
    for k in range(n_groups):
        if group_assignments[i][k].varValue == 1:
            print("Student %i in Group %i" % (i, k))
            
for k in range(n_groups):
    print("Group %i Size %i" % (k, sum([group_assignments[i][k].varValue for i in range(n_students)])))
