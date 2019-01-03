from CSPSolver import CSPSolver
from CSPAlgorithm import CSPAlgorithm
from CSPPolicy import CSPPolicy
from copy import copy

if __name__ == "__main__":
    solver = CSPSolver(CSPAlgorithm.StandardBacktracking, CSPPolicy.InsertOrder, False)
    for i in range(1, 5):
        solver.add_variable("r"+str(i), [1, 2, 3, 4])
    for i in range(1, 5):
        for j in range(i + 1, 5):
            solver.add_constraint(("r"+str(i), "r"+str(j)), lambda x1, x2: x1 != x2)
    
    for i in range(1, 5):
        for j in range(1, 5):
            if i != j:
                solver.add_constraint(("r"+str(i), "r"+str(j)), lambda xi, xj: xj != xi + abs(j-i))
                solver.add_constraint(("r"+str(i), "r"+str(j)), lambda xi, xj: xj != xi - abs(j-i))


    solver.solve(True)

    solver.print_tree()

    #print(solver._solutions[0])