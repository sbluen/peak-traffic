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
        if sender not in nodes:
            nodes[sender] = Node(sender)
        recip = line.split()[7].split("@")[0]
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

#TODO: Analysis code