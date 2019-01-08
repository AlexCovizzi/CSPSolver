from CSPSolver import CSPSolver
from CSPAlgorithm import CSPAlgorithm
from CSPPolicy import CSPPolicy
from TreePlot import SolverPlot

if __name__ == "__main__":
    solver = CSPSolver(CSPAlgorithm.StandardBacktracking, CSPPolicy.InsertOrder, True)
    
    n = 9
    for i in range(1, n):
        solver.add_variable("r"+str(i), list(range(1, n)))

    solver.add_constraint(("r1",), lambda x: x > 5)

    for i in range(1, n):
        for j in range(i + 1, n):
            solver.add_constraint(("r" + str(i), "r" + str(j)), lambda xi, xj: xi != xj)

    for i in range(1, n):
        for j in range(i + 1, n):
            solver.add_constraint(("r" + str(i), "r" + str(j)), lambda xi, xj, j=j, i=i: xi != xj + (j - i))
            solver.add_constraint(("r" + str(i), "r" + str(j)), lambda xi, xj, j=j, i=i: xi != xj - (j - i))

    #solver.apply_node_consistency()

    
    solver.solve(True)

    # solver.print_solutions()
    solver.print_tree()

    plotter = SolverPlot(solver)
    plotter.draw_decision_tree()

    plotter.draw_constraint_graph()

    import inspect
    print(inspect.getsourcelines(solver._constraints.get_binary_constraints("r1", "r2")[0][0]))