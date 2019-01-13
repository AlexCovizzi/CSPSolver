from sys import argv, path as sys_path
from os import path as os_path, getcwd

module_path = os_path.abspath(getcwd())
if module_path not in sys_path: sys_path.append(module_path)

from cspsolver import CSPSolver, Algorithm, Policy, draw_constraint_graph, draw_decision_tree


# esempio del sudoku risolto con algoritmo Full Look Ahead,
# con scelta della variabile da assegnare secondo la regola Minimum Remaining Values,
# e con arc-consistency applicata ad ogni passo
if __name__ == "__main__":
    solver = CSPSolver(Algorithm.FullLookAhead, Policy.MinimumRemainingValues, True)

    # cell_ij -> riga i, colonna j
    for i in range(1, 10):
        for j in range(1, 10):
            solver.add_variable("cell_" + str(i) + str(j), list(range(1, 10)))

    different = lambda x, y: x != y
    for i in range(1, 10):
        for j in range(1, 10):
            for k in range(j, 10):
                solver.add_constraint(("cell_" + str(i) + str(j), "cell_" + str(i) + str(k)), different)
                solver.add_constraint(("cell_" + str(j) + str(i), "cell_" + str(k) + str(i)), different)

    start = [1, 4, 7, 10]

    for r in range(3):
        for i in range(start[r], start[r + 1]):
            for c in range(3):
                for j in range(start[c], start[c + 1]):
                    for k in range(start[r], start[r + 1]):
                        for h in range(start[c], start[c + 1]):
                            c1, c2 = solver._constraints.get_binary_constraints("cell_" + str(i) + str(j), "cell_" + str(k) + str(h))
                            if not (c1 or c2):
                                solver.add_constraint(("cell_" + str(i) + str(j), "cell_" + str(k) + str(h)), different)

    # situazione iniziale
    solver.add_constraint(("cell_14" ,), lambda x: x == 1)
    solver.add_constraint(("cell_16" ,), lambda x: x == 2)
    solver.add_constraint(("cell_22" ,), lambda x: x == 8)
    solver.add_constraint(("cell_25" ,), lambda x: x == 5)
    solver.add_constraint(("cell_28" ,), lambda x: x == 3)
    solver.add_constraint(("cell_33" ,), lambda x: x == 4)
    solver.add_constraint(("cell_35" ,), lambda x: x == 8)
    solver.add_constraint(("cell_37" ,), lambda x: x == 7)
    solver.add_constraint(("cell_42" ,), lambda x: x == 6)
    solver.add_constraint(("cell_47" ,), lambda x: x == 9)
    solver.add_constraint(("cell_48" ,), lambda x: x == 5)
    solver.add_constraint(("cell_51" ,), lambda x: x == 3)
    solver.add_constraint(("cell_55" ,), lambda x: x == 9)
    solver.add_constraint(("cell_56" ,), lambda x: x == 6)
    solver.add_constraint(("cell_59" ,), lambda x: x == 2)
    solver.add_constraint(("cell_62" ,), lambda x: x == 5)
    solver.add_constraint(("cell_68" ,), lambda x: x == 7)
    solver.add_constraint(("cell_71" ,), lambda x: x == 5)
    solver.add_constraint(("cell_77" ,), lambda x: x == 4)
    solver.add_constraint(("cell_82" ,), lambda x: x == 9)
    solver.add_constraint(("cell_85" ,), lambda x: x == 3)
    solver.add_constraint(("cell_88" ,), lambda x: x == 6)
    solver.add_constraint(("cell_89" ,), lambda x: x == 7)
    solver.add_constraint(("cell_94" ,), lambda x: x == 4)
    solver.add_constraint(("cell_96" ,), lambda x: x == 8)
    solver.add_constraint(("cell_97" ,), lambda x: x == 5)
    

    f = open("sudoku_steps.txt", "w+")

    solver.apply_node_consistency(target=f)
    solver.apply_arc_consistency(target = f)

    solver.solve(one_solution=True, target=f)
    
    f.close()

    solver.print_solutions()
    # solver.print_tree()

    draw_decision_tree(solver, print_domains=False, target="sudoku_decision_tree.pdf")
    draw_constraint_graph(solver, target="sudoku_constraint_graph.pdf")