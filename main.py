from CSPSolver import CSPSolver
from CSPAlgorithm import CSPAlgorithm
from CSPPolicy import CSPPolicy

if __name__ == "__main__":
    solver = CSPSolver(CSPAlgorithm.FullLookAhead, CSPPolicy.InsertOrder, False)
    
    for i in range(1, 17):
        solver.add_variable("r"+str(i), list(range(1, 17)))
    for i in range(1, 17):
        for j in range(i + 1, 17):
            solver.add_constraint(("r" + str(i), "r" + str(j)), lambda x1, x2: x1 != x2)

    for i in range(1, 17):
        for j in range(i + 1, 17):
            solver.add_constraint(("r" + str(i), "r" + str(j)), lambda xi, xj, j=j, i=i: xi != xj + (j - i))
            solver.add_constraint(("r" + str(i), "r" + str(j)), lambda xi, xj, j=j, i=i: xi != xj - (j - i))

    solver.solve(True)

    solver.print_tree()