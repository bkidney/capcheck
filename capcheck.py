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
        type = line.split()[6]

        if type == "UND":
            fn, lib = line.split()[7].split('@')
            fns.append(fn)

fns = list(dict.fromkeys(fns))
print(fns)

ldd_data = subprocess.check_output(['ldd', binary])
ldd_data = ldd_data.split('\n')

libs= []
for line in ldd_data:
    if len(line.split()) > 1:
        lib = line.split()[0]
        libs.append(lib)


callgraph = nx.DiGraph()
fn_to_node = dict()
node_to_fn = dict()
for lib in libs:
    gtmp = pgv.AGraph(sys.argv[2] + "/" + lib + ".bc.dot")
    for i in gtmp.nodes():
        fn_to_node[ i.attr['label'][1:-1]] =  i.name
        node_to_fn[ i.name ] = i.attr['label'][1:-1]
    graph = nx.DiGraph(gtmp)
    tmp = callgraph.copy()
    callgraph = nx.compose(tmp, graph)

# nx.nx_agraph.write_dot(callgraph, "test.dot")

fn_to_capunsafe = dict()
with open(sys.argv[3]) as f:
    for line in f:
        if line.strip() in fn_to_node:
            callers = nx.algorithms.dag.ancestors(callgraph, fn_to_node[line.strip()])

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
