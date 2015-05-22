'''
Created on May 15, 2015

@author: sbluen
'''

import sys
import time

nodes = {}

# scanned_nodes = set()

class Node():
    def __init__(self, name):
        self.name = name
        self.outg = {} #outgoing edges
        self.edges = {} #bidirectional edges
        
    def __eq__(self, other):
        return self.name.__eq__(other.name)
    
    def __lt__(self, other):
        return self.name < other.name
    
    def __hash__(self):
        return hash(self.name)
    
    def __str__(self):
        return self.name
    
    def __repr__(self):
        return "Node(%s)" % repr(self.name)
 
class Clique():
    """A container with a frozenset of data containing nodes
    and the subclique flag.
    Also stored data structures of adjacent nodes for searching for
    more cliques in. 
    
    from_operation refers to wherther or not this node is being created out of an addition operation
    """

    def __init__(self, data, from_operation=False):
        """Stores data. 
        data should be an iterable."""
        self.data = frozenset(data)
        self.subclique = False
        if not from_operation:
            #adj is used to search by name
            #counts is used to search by number
            self.adj = {}
            self.counts = [set() for i in range(len(nodes)+1)]# @UnusedVariable
            for node in self.data:
                for link in node.edges.values():
                    if link in self.data:
                        #Whatever is in this clique is not adjacent to it.
                        continue
                    if link not in self.adj:
                        self.adj[link] = 1
                        self.counts[1].add(link)
                    else:
                        self.counts[self.adj[link]].remove(link)
                        self.counts[self.adj[link]+1] .add(link)
                        self.adj[link] += 1
                    #Remove the link from the adjacency structures not that this link
                    #no longer counts as adjacent.
                    if node in self.adj:
                        count = self.adj[node]
                        del self.adj[node]
                        self.counts[count].remove(node)
                    
            
    def __hash__(self):
        return hash(self.data)
    
    def __eq__(self, other):
        return self.data == other.data
    
    def __lt__(self, other):
        return list(self.data) < list(other.data)
    
    def __cmp__(self, other):
        sys.exit()
    
    def __str__(self):
        return str(self.data)
    
    def __repr__(self):
        return "Clique(%s)" % repr(self.data)
    
    def __add__(self, other):
        """Makes a new clique composed of this clique's data with the
        addition of a new node.
        other must be a Node.
        """
        rv = Clique(self.data, from_operation=True)
        rv.adj = dict(self.adj)
        rv.counts = [set(i) for i in self.counts]
        rv._add(node)
        return rv
    
    def _add(self, node):
        """Adds a new node to this clique's data
        and updates the adjacency data structures."""
        self.data |= set((node,))
        for link in node.edges.values():
            if link in self.data:
                #Whatever is in this clique is not adjacent to it.
                continue
            if link not in self.adj:
                self.adj[link] = 1
                self.counts[1].add(link) 
            else:
                self.counts[self.adj[link]].remove(link)
                self.counts[self.adj[link]+1].add(link)
                self.adj[link] += 1
                #Remove the link from the adjacency structures not that this link
                #no longer counts as adjacent.
                if node in self.adj:
                    count = self.adj[node]
                    del self.adj[node]
                    self.counts[count].remove(node)

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


triangles = set()
final_cliques = set()

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
                    triangles.add(temp_clique)



#Find larger cliques
def examine(clique):
    if clique.counts[len(clique.data)] == set():
        if [i.name for i in sorted(list(clique.data))] == list("uwxz"):
            import pdb
            pdb.set_trace()  
        #base case where this clique has no supercliques
        final_cliques.add(clique.data)
    else:
        for link in clique.counts[len(clique.data)]:
            examine(clique+link)
        
t1 = time.time()
for triangle in triangles:
    examine(triangle)


#Not to +2 because at len(nodes), we don't have any other nodes to join into the
#clique
# for degree in range(4, len(nodes)+1):
#     for clique in cliques[degree-1]:
#         nodes_to_check = clique.counts[degree-1]
#         for node in nodes_to_check:
#             cliques[degree].add(clique + node)
#         for node in clique.data:
#             
#             #See if that node is in a new clique containing just the current
#             #clique and the new node.
#             in_clique = True
#             for link in node.edges.values():
#                 if link in clique.data:
#                     #This would not make a larger clique of unique elements
#                     continue
#                 if link in scanned_nodes:
#                     #Scanning this again would waste a lot of time.
#                     continue
#                 for node in clique.data:
#                     if node not in link.edges.values():
#                         in_clique = False
#                 scanned_nodes.add(link)
#             
#             if in_clique:
#                 clique.subclique = True
#                 temp_clique = clique + link
#                 cliques[degree].add(temp_clique)
#     scanned_nodes = set()
                
#Final code to take only the cliques that are not subcluques.
#Also takes them out of their containers.
# final_cliques = []
# for degree in range(3, len(nodes)+1):
#     for clique in cliques[degree]:
#         if not clique.subclique:
#             final_cliques.append(sorted(list(clique.data)))

final_cliques = [sorted(list(i)) for i in final_cliques]

#Printing code
for clique in sorted(final_cliques):
    print ", ".join(str(node)+"@facebook.com" for node in clique)
t2 = time.time()
print(t2-t1)

# t@facebook.com, w@facebook.com, x@facebook.com, y@facebook.com, z@facebook.com
# t@facebook.com, w@facebook.com, x@facebook.com, z@facebook.com
# t@facebook.com, w@facebook.com, y@facebook.com, z@facebook.com
# t@facebook.com, w@facebook.com, z@facebook.com
# t@facebook.com, x@facebook.com, y@facebook.com, z@facebook.com
# t@facebook.com, x@facebook.com, z@facebook.com
# t@facebook.com, y@facebook.com, z@facebook.com
# u@facebook.com, v@facebook.com, x@facebook.com, y@facebook.com, z@facebook.com
# u@facebook.com, v@facebook.com, x@facebook.com, z@facebook.com
# u@facebook.com, v@facebook.com, y@facebook.com, z@facebook.com
# u@facebook.com, v@facebook.com, z@facebook.com
# u@facebook.com, w@facebook.com, x@facebook.com, y@facebook.com, z@facebook.com