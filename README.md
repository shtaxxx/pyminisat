Pyminsat
====================
MinSat Wrapper for Python

How to use
--------------------
1. Please install [MiniSat](http://minisat.se/Main.html) on your environment.
2. Create an instance of SatSolver().

<pre><code>from minisat import *
solver = SatSolver()
a = SatClause()
b = SatClause()
c = SatClause()
solver.append((a, b))
solver.append((-b, c))
solver.solve()
print solver[a], solver[b], solver[c]</code></pre>
