'''
Created on May 15, 2015

@author: sbluen
'''

nodes = {}

class Node():
    def __init__(self, name):
        self.name=name
        self.outg = {} #outgoing edges
        self.edges = {} #bidirectional edges
    def __cmp__(self, other):
        return self.name.__cmp__(other.name)

import sys
with open(sys.argv[1], "r") as f:
    for line in f:
        
        sender = line.split()[6].split("@")[0]
        recip = line.split()[7].split("@")[0]
        
        if sender == recip:
            continue
        
        if sender not in nodes:
            nodes[sender] = Node(sender)
        if recip not in nodes:
            nodes[recip] = Node(recip)
        
        if recip in nodes[sender].edges:
            #It's already bidirectional
            continue
        
        if recip in nodes[sender].outg:
            #This has already been handled
            continue
    
        if sender in nodes[recip].outg:
            #make this a bidirectional mapping
            nodes[sender].edges[recip] = nodes[recip]
            nodes[recip].edges[sender] = nodes[sender]
            del nodes[recip].outg[sender]
            continue
            
        nodes[sender].outg[recip] = (nodes[recip])


groups = [None] * (len(nodes)+1)

#put groups of 3 nodes in variable groups

if len(nodes) < 3:
    #degenerate case
    pass
else:
    for node in nodes.values():
        for link1 in node.edges.values():
            for link2 in link1.edges.values():
                if link2 == node:
                    #This is the link back to node
                    continue
                if node in link2.edges.values():
                    #sorted by name
                    groups[3].append(sorted([node, link1, link2]))

havework = True
while havework:
    havework = False
    