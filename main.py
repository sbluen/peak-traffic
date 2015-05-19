'''
Created on May 15, 2015

@author: sbluen
'''

import sys
import time
import collections

nodes = {}

scanned_nodes = set()

class Node():
    def __init__(self, name):
        self.name = name
        self.outg = {} #outgoing edges
        self.edges = {} #bidirectional edges
        
#     def __eq__(self, other):
#         return self.name.__eq__(other.name)
    
    def __lt__(self, other):
        return self.name<other.name
    
    def __hash__(self):
        return hash(self.name)
    
    def __str__(self):
        return self.name
    
    def __repr__(self):
        return repr(self.name)
 
class Clique():
    """A container with a frozenset of data containing nodes
    and the subclique flag.
    Also stored a dict of adjacent nodes for searching for more cliques in. 
    """

    def __init__(self, data):
        """Stores data. """
        self.data = frozenset(data)
        self.subclique = False
        if len(data) == 3:
            self.adj = {}
            self.counts = [set() for i in range(len(nodes)-2)]  # @UnusedVariable
            for node in data:
                if node not in self.adj:
                    self.adj[node] = 1
                    self.counts[1] |= node 
                else:
                    self.counts[self.adj[node]] -= node
                    self.counts[self.adj[node]+1] |= node
                    self.adj[node] += 1
                    
            
    def __hash__(self):
        return hash(self.data)
    
    def __eq__(self, other):
        return self.data == other.data
    
    def __str__(self):
        return str(self.data)
    
    def __repr__(self):
        return repr(self.data)

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


cliques = [set() for i in range(len(nodes)+1)]

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
                    temp_clique = Clique([node, link1, link2])
                    cliques[3].add(temp_clique)

#Find larger cliques
#Not +2 because at len(nodes), we don't have any other nodes to join into the
#clique.
t1 = time.time()
for degree in range(4, len(nodes)+1):
    for clique in cliques[degree-1]:
        for node in clique.data:
            
            #See if that node is in a new clique containing just the current
            #clique and the new node.
            in_clique = True
            for link in node.edges.values():
                if link in clique.data:
                    #This would not make a larger clique of unique elements
                    continue
                if link in scanned_nodes:
                    #Scanning this again would waste a lot of time.
                    continue
                for node in clique.data:
                    if node not in link.edges.values():
                        in_clique = False
                scanned_nodes.add(link)
            
            if in_clique:
                clique.subclique = True
                temp_clique = Clique(clique.data | set((link,)))
                cliques[degree].add(temp_clique)
    scanned_nodes = set()
                
#Final code to take only the cliques that are not subcluques.
#Also takes them out of their containers.
final_cliques = []
for degree in range(3, len(nodes)+1):
    for clique in cliques[degree]:
        if not clique.subclique:
            final_cliques.append(list(clique.data))

#Printing code
for clique in sorted(final_cliques):
    print ", ".join(str(node)+"@facebook.com" for node in sorted(clique))
t2 = time.time()
print(t2-t1)