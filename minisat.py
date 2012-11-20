import sys
import os
import commands

class SatSolver(object):
    def __init__(self, minisat_cmd='minisat', inputfilename='tmp.cnf', outputfilename='rslt.out'):
        self.minisat_cmd = minisat_cmd
        self.inputfilename = inputfilename
        self.outputfilename = outputfilename
        self.clauses = []
        self.unique_varnames = {}
        self.unique_varname_cnt = 1
        self.result = []
    def append(self, var):
        if not isinstance(var, tuple): raise Exception, "'clause' should be tuple."
        for v in var:
            if not isinstance(v, SatClauseBase): raise Exception, "Illegal variable type."
            if v.name not in self.unique_varnames:
                self.unique_varnames[v.name] = self.unique_varname_cnt
                self.unique_varname_cnt += 1
        self.clauses.append(var)
    def tonum(self, name):
        return str(self.unique_varnames[name])
    def solve(self, all=False, dump=False):
        inputfile = open(self.inputfilename, 'w')
        num_variables = len(self.unique_varnames)
        num_clauses = len(self.clauses)
        inputfile.write("p cnf %d %d\n" % (num_variables, num_clauses))
        for clause in self.clauses:
            write_var = ''
            for e in clause:
                if isinstance(e, SatClause): write_var += self.tonum(e.name) + ' ' 
                if isinstance(e, SatClauseInv): write_var += '-' + self.tonum(e.name) + ' '
            inputfile.write(write_var + '0\n')
        inputfile.close()
        if dump: print open(self.inputfilename, 'r').read()

        cmd = self.minisat_cmd + ' ' + self.inputfilename + ' ' + self.outputfilename
        minisat_result = commands.getoutput(cmd)
        if dump: print minisat_result
        if dump: print open(self.outputfilename, 'r').read()

        outputfile = open(self.outputfilename, 'r')
        outputfile.readline() # skip 1st line
        rslt = outputfile.readline().split()
        for r in rslt[:-1]:
            self.result.append(int(r))
    def __getitem__(self, clause):
        if not isinstance(clause, SatClauseBase): raise Exception, 'Type Error'
        index = int(self.tonum(clause.name)) - 1
        return self.result[index]
        
class SatClauseBase(object):
    def __init__(self, name=None):
        self.name = id(self)
        if name is not None:
            self.name = name

class SatClause(SatClauseBase):
    def __neg__(self):
        return SatClauseInv(self.name)
class SatClauseInv(SatClauseBase):
    def __neg__(self):
        return SatClause(self.name)

if __name__ == '__main__':
    solver = SatSolver()
    a = SatClause()
    b = SatClause()
    c = SatClause()
    solver.append((a, b))
    solver.append((-b, c))
    solver.solve(dump=False)
    print solver[a], solver[b], solver[c]
