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
 
class Clique(list):
    """A modified list with a flag to determine whether a clique has been used
    in a larger clique, and should therefore not be part of the final answer.
    """

    def __init__(self, *args, **kwargs):
        super.__init__(*args, **kwargs)
        self.subclique = False

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


cliques = set() * (len(nodes)+1)

#put cliques of 3 nodes in cliques
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
                    cliques[3] = cliques[3] or Clique(sorted([node, link1, link2]))

#Find larger cliques
#Not +2 because at len(nodes), we don't have any other nodes to join into the
#clique.
for degree in range(4, len(nodes)+1):
    for clique in cliques[degree-1]:
        for node in clique:
            
            #See if that node is in a new clique containing just the current
            #clique and the new node.
            in_clique = True
            for link in node.edges:
                for node in clique:
                    if node not in link.edges:
                        in_clique = False
            
            if in_clique:
                clique.subclique = True
                temp_clique = Clique(sorted(clique + [link]))
                cliques[degree] = cliques[degree] or temp_clique
                
#Final code to take only the cliques that are not subcluques
final_cliques = []
for degree in range(3, len(nodes)+1):
    for clique in cliques[degree]:
        if not clique.subclique:
            final_cliques.append(clique)
final_cliques = sorted(final_cliques)

#Printing code
for clique in final_cliques:
    print ", ".join(clique)