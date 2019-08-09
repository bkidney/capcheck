import sys
import pygraphviz as pgv

Gtmp = pgv.AGraph(sys.argv[1])

trans = dict()
for i in Gtmp.nodes():
    if i.name in trans:
        trans[ i.name ] = i.attr['label'].replace(" ", "_").replace(".", "_")
    

with open(sys.argv[1]) as f:
    dot = f.read()
    for k in trans:
        dot = dot.replace(k, trans[k])

    print(dot)
