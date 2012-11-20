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
        if not isinstance(var, tuple): raise Exception, "'var' should be tuple."
        for v in var:
            if not isinstance(v, SatVarBase): raise Exception, "Illegal variable type."
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
                if isinstance(e, SatVar): write_var += self.tonum(e.name) + ' ' 
                if isinstance(e, SatVarInv): write_var += '-' + self.tonum(e.name) + ' '
            inputfile.write(write_var + '0\n')
        inputfile.close()
        if dump: print open(self.inputfilename, 'r').read()

        cmd = self.minisat_cmd + ' ' + self.inputfilename + ' ' + self.outputfilename
        minisat_result = commands.getoutput(cmd)
        if dump: print minisat_result
        if dump: print open(self.outputfilename, 'r').read()

        outputfile = open(self.outputfilename, 'r')
        line = outputfile.readline() # skip 1st line
        line = outputfile.readline()
        while line:
            rslt = tuple(line.split())
            int_rslt = []
            for r in rslt:
                int_rslt.append(int(r))
            self.result.append(tuple(int_rslt))
            line = outputfile.readline()
    def __getitem__(self, index):
        return self.result[index]
        
class SatVarBase(object):
    def __init__(self, name):
        if not isinstance(name, str): raise Exception, "'name' should be str."
        self.name = name
class SatVar(SatVarBase):
    def __neg__(self):
        return SatVarInv(self.name)
class SatVarInv(SatVarBase):
    def __neg__(self):
        return SatVar(self.name)

if __name__ == '__main__':
    solver = SatSolver()
    a = SatVar('a')
    b = SatVar('b')
    c = SatVar('c')
    solver.append((a, b))
    solver.append((-b, c))
    solver.solve(dump=False)
    print solver[0]
