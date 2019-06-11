import sys
import subprocess
import yaml
import networkx as nx
import pygraphviz as pgv
import sys


binary = sys.argv[1]
elfdata = subprocess.check_output(['readelf', '-s', binary])
elfdata = elfdata.split('\n')

fns = []
for line in elfdata:
    if len(line.split()) > 8:
        fn, lib = line.split()[7].split('@')

        if (lib.startswith("FBSD")):
            fns.append(fn)

fns = list(dict.fromkeys(fns))

gtmp = pgv.AGraph(sys.argv[2])
graph = nx.DiGraph(gtmp)

fn_to_node = dict()
node_to_fn = dict()
for i in gtmp.nodes():
    fn_to_node[ i.attr['label'][1:-1]] =  i.name
    node_to_fn[ i.name ] = i.attr['label'][1:-1]

fn_to_capunsafe = dict()
with open(sys.argv[3]) as f:
    for line in f:
        if line.strip() in fn_to_node:
            callers = nx.algorithms.dag.ancestors(graph, fn_to_node[line.strip()])

            for call in callers:
                fn = node_to_fn[call]
                if fn in fn_to_capunsafe:
                    fn_to_capunsafe[fn].append(line.strip())
                else:
                    tmp = list()
                    tmp.append(line.strip())
                    fn_to_capunsafe[fn] = tmp

for fn in fns:
    if fn in fn_to_capunsafe:
        print(fn, fn_to_capunsafe[fn])

# print(fn_to_capunsafe)
# print(fns)
