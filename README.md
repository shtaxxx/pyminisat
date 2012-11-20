Pyminsat
====================
MinSat Wrapper for Python

How to use
--------------------
1. Please install MiniSat <http://minisat.se/Main.html> on your environment.
2. Create an instance of SatSolver().


    from minsat import *
    solver = SatSolver()
    a = SatVar('a')
    b = SatVar('b')
    c = SatVar('c')
    solver.append((a, b))
    solver.append((-b, c))
    solver.solve(dump=False)
    print solver[0]


