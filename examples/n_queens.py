from sys import argv, path as sys_path
from os import path as os_path, getcwd

module_path = os_path.abspath(getcwd())
if module_path not in sys_path: sys_path.append(module_path)

from cspsolver import CSPSolver, Algorithm, Policy, draw_constraint_graph, draw_decision_tree

# esempio delle N regine risolto con algoritmo Forward Checking e
# con scelta della variabile da assegnare secondo la regola Insert Order
if __name__ == "__main__":
    solver = CSPSolver(Algorithm.ForwardChecking, Policy.InsertOrder, step_arc_consistency=False)
    
    n = int(argv[1]) if len(argv) > 1 else 8
    n += 1

    for i in range(1, n):
        solver.add_variable("r"+str(i), list(range(1, n)))

    for i in range(1, n):
        for j in range(i + 1, n):
            solver.add_constraint(("r" + str(i), "r" + str(j)), lambda xi, xj: xi != xj)

    for i in range(1, n):
        for j in range(i + 1, n):
            solver.add_constraint(("r" + str(i), "r" + str(j)), lambda xi, xj, j=j, i=i: xi != xj + (j - i))
            solver.add_constraint(("r" + str(i), "r" + str(j)), lambda xi, xj, j=j, i=i: xi != xj - (j - i))

    f = open("nqueens_steps.txt", "w+")

    solver.solve(one_solution=True, target=f)
    f.close()

    solver.print_solutions()

    draw_decision_tree(solver, print_domains=True, target="nqueens_decision_tree.pdf")
    draw_constraint_graph(solver, target="nqueens_constraint_graph.pdf")