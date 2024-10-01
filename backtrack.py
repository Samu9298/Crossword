import copy
import time
import numpy


def backtrackingSearch(csp):
    startTime = time.time()
    result = backtrack(csp, {})
    endTime = time.time()

    return result, endTime - startTime


def backtrack(csp, assignment):
    if len(assignment) == len(csp.variables):
        return assignment

    var = selectUnassignedVariable(csp, assignment)

    for value in orderDomainValues(csp, var, assignment):
        if value is not None:
            print("Trying value", value, "for variable", var)
            if isConsistent(csp, var, value, assignment):
                assignment[var] = value
                print("Assignment with", value, "added:", assignment)
                oldDomains = csp.domains.copy()
                inference = doInference(csp)
                print("INFERENCE DONE")
                if inference:
                    result = backtrack(csp, assignment)
                    if result:
                        return result
                    csp.domains.clear()
                    csp.domains.update(oldDomains)
                del assignment[var]
                print("Backtracked. Assignment is now:", assignment)
            """
            else:
                print(f"Value {value} is not consistent for variable {var}")
            """
    return False


def selectUnassignedVariable(csp, assignment):
    # choose the variable to assign according to the heuristic MRV (minimum remaining variables):
    # it chooses the variable which domain is the smallest

    unassignedVariables = []
    for variable in csp.variables:
        if variable not in assignment.keys():
            unassignedVariables.append(variable)

    minDomSize = numpy.inf
    for var in unassignedVariables:
        if len(csp.domains[var]) < minDomSize:
            minDomSize = len(csp.domains[var])
            varToAssign = var

    return varToAssign


def isConsistent(csp, var, value, assignment):
    consistent = True
    if value in assignment.values():
        consistent = False
    for testVar, testValue in assignment.items():
        if var != testVar:
            overlap = csp.variablesOverlap(var, testVar)
            if overlap:
                i, j = overlap
                if value[i] != assignment[testVar][j]:
                    consistent = False

    return consistent


def doInference(csp):
    return ac3(csp)


def ac3(csp):
    queue = set()
    for xi in csp.variables:
        for xj in csp.variables:
            if xi != xj and csp.variablesOverlap(xi, xj):
                queue.add((xi, xj))

    while len(queue) > 0:
        print("lunghezza: " + str(len(queue)))
        xi, xj = queue.pop()
        if revise(csp, xi, xj):
            if len(csp.domains[xi]) == 0:
                return False
            for xk in csp.variablesNeighbors[xi]:
                if xk != xj:
                    queue.add((xk, xi))
    return True


def revise(csp, xi, xj):
    print("start revise: ", xi, xj)
    revised = False
    overlap = csp.variablesOverlap(xi, xj)
    for x in csp.domains[xi]:
        if all(x[overlap[0]] != y[overlap[1]] for y in csp.domains[xj]):
            csp.domains[xi].remove(x)
            print("removed x from xi")
            revised = True

    # print("end revise")
    return revised


def orderDomainValues(csp, var, assignment):
    # using least constraining value (LCV)

    def countConstrainingValues(value):
        count = 0
        if var in csp.variablesNeighbors.keys():
            for var2 in csp.variablesNeighbors[var]:
                if var2 not in assignment:
                    overlap = csp.variablesOverlap(var, var2)
                    if overlap:
                        i, j = overlap
                        for val2 in csp.domains[var2]:
                            if value[i] != val2[j]:
                                count += 1
        return count

    ret = sorted(csp.domains[var], key=countConstrainingValues)
    return ret
