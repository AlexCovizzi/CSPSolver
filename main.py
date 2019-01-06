from CSPSolver import CSPSolver
from CSPAlgorithm import CSPAlgorithm
from CSPPolicy import CSPPolicy
from TreePlot import TreePlot

if __name__ == "__main__":
    solver = CSPSolver(CSPAlgorithm.FullLookAhead, CSPPolicy.MinimumRemainingValues, True)
    
    for i in range(1, 9):
        solver.add_variable("r"+str(i), list(range(1, 9)))
    for i in range(1, 9):
        for j in range(i + 1, 9):
            solver.add_constraint(("r" + str(i), "r" + str(j)), lambda x1, x2: x1 != x2)

    for i in range(1, 9):
        for j in range(i + 1, 9):
            solver.add_constraint(("r" + str(i), "r" + str(j)), lambda xi, xj, j=j, i=i: xi != xj + (j - i))
            solver.add_constraint(("r" + str(i), "r" + str(j)), lambda xi, xj, j=j, i=i: xi != xj - (j - i))

    #solver.apply_node_consistency()

    
    solver.solve(True)

    # solver.print_solutions()
    solver.print_tree()

    plotter = TreePlot()
    plotter.draw(solver._root)