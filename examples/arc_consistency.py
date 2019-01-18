from sys import argv, path as sys_path, stdout
from os import path as os_path, getcwd

module_path = os_path.abspath(getcwd())
if module_path not in sys_path: sys_path.append(module_path)

from cspsolver import CSPSolver, Algorithm, Policy, draw_constraint_graph, draw_decision_tree

# esempio recuperato da un esercizio svolto in classe, in cui viene applicata la arc-consistenza
if __name__ == "__main__":
    solver = CSPSolver()

    solver.add_variables(["a", "b", "c", "d", "e"], [1, 2, 3, 4])

    solver.add_constraint(("b", ), lambda b: b != 3)
    solver.add_constraint(("c", ), lambda c: c != 2)
    solver.add_constraint(("a", "b"), lambda a, b: a != b)
    solver.add_constraint(("b", "c"), lambda b, c: b != c)
    solver.add_constraint(("c", "d"), lambda c, d: c < d)
    solver.add_constraint(("a", "d"), lambda a, d: a == d)
    solver.add_constraint(("e", "a"), lambda e, a: e < a)
    solver.add_constraint(("e", "b"), lambda e, b: e < b)
    solver.add_constraint(("e", "c"), lambda e, c: e < c)
    solver.add_constraint(("e", "d"), lambda e, d: e < d)
    solver.add_constraint(("b", "d"), lambda b, d: b != d)

    f = open("arc_consistency_steps.txt", "w+")
    f = stdout

    print(solver, file=f)
    solver.apply_arc_consistency(target=f)
    print(solver, file=f)

    f.close()

    draw_constraint_graph(solver, target="arc_constraint_graph.pdf")