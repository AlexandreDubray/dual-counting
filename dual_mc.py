import sys
import os
import subprocess

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
INSTANCE_DIR = os.path.join(SCRIPT_DIR,  'benchmarks')
GRAPH_DIR = os.path.join(SCRIPT_DIR, 'benchmarks-primal-graph')
TD_DIR = os.path.join(SCRIPT_DIR, 'benchmarks-td')

benchmark = sys.argv[1]

def create_subdirs(path):
    subdirs = '/'.join(path.split('/')[:-1])
    os.makedirs(subdirs, exist_ok=True)
    return path

cnf_file = create_subdirs(os.path.join(INSTANCE_DIR, benchmark))
graph_file = create_subdirs(os.path.join(GRAPH_DIR, benchmark))
td_file = create_subdirs(os.path.join(TD_DIR, benchmark))

def cnf_to_primal_graph():
    with open(cnf_file) as f:
        edges = set()
        nb_var = None
        for line in f:
            s = line.strip().split()
            if line.startswith('c'):
                continue
            if line.startswith('p cnf'):
                print(f"Header of the cnf {line.strip()}")
                nb_var = int(s[2])
                continue
            variables = [abs(int(x)) for x in s[:-1]]
            for i in range(len(variables)):
                for j in range(i + 1, len(variables)):
                    x = abs(variables[i])
                    y = abs(variables[j])
                    n1 = min(x,y)
                    n2 = max(x, y)
                    edges.add((n1, n2))

    with open(graph_file, 'w') as fout:
        print(f"Primal graph with {nb_var} variables and {len(edges)} edges")
        fout.write(f'p tw {nb_var} {len(edges)}\n')
        fout.write('\n'.join([f'{x} {y}' for (x, y) in edges]))

def compute_td():
    if os.path.isfile(graph_file):
        with open(td_file, 'w') as f:
            subprocess.run(["timeout", "5", "flow_cutter_pace17", graph_file], stdout=f)

def td_stat():
    width = None
    if os.path.isfile(td_file):
        with open(td_file) as f:
            for line in f:
                s = line.strip().split()
                if line.startswith('s td'):
                    width = int(s[3]) - 1
                    break
    print(f'{sys.argv[1]},{width}')

#cnf_to_primal_graph()
#compute_td()
#td_stat()
