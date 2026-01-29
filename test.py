import subprocess

mc = int(subprocess.check_output(["d4", "example.cnf"]).decode('utf-8').split('\n')[-3].split()[-1])

clauses = []
number_variables = 0
with open('example.cnf') as f:
    for line in f:
        if line.startswith('p'):
            continue
        clauses.append([int(x) for x in line.strip().split()[:-1]])
        number_variables = max(number_variables, max(clauses[-1]))

def new_problem(clauses, mapping):
    new_clauses = []
    for cls in clauses:
        new_cls = []
        for x in cls:
            if x < 0:
                new_cls.append(-mapping[abs(x)])
            else:
                new_cls.append(mapping[x])
        new_clauses.append(new_cls)
    return new_clauses

def restriction():
    for x in range(1, number_variables + 1):
        for y in range(x + 1, number_variables + 1):
            print(f"\t ---- {x} = {y} ----")
            # First case, x = y
            mapping = {}
            for var in range(1, number_variables + 1):
                if var < x:
                    mapping[var] = var
                elif var == x:
                    mapping[var] = y - 1
                else:
                    mapping[var] = var - 1
            
            new_cls = new_problem(clauses, mapping)
            with open('tmp.cnf', 'w') as f:
                f.write(f'p cnf {number_variables - 1} {len(new_cls)}\n')
                f.write('\n'.join([' '.join([str(var) for var in cls]) + ' 0' for cls in new_cls]))
            model_count = int(subprocess.check_output(["d4", "tmp.cnf"]).decode('utf-8').split('\n')[-3].split()[-1])
            print(f"Mapping x -> y: model_count is {model_count} < {mc} (gap {(model_count / mc)*100})")

restriction()
