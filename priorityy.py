class DisjSet:
    def __init__(self,threshold,visit_order):

        self.components = set(visit_order)
        self.parent = {}
        self.rank = {}
        self.element_cnt = {}
        self.threshold = threshold
        for i in visit_order:
            self.parent[i] = i
            self.rank[i] = 1
            self.element_cnt[i] = 1

    # Finds set of given item x
    def find(self, x):

        # Finds the representative of the set that x is an element of
        if (self.parent[x] != x):

            # if x is not the parent of itself. Then x is not the representative of its set
            self.parent[x] = self.find(self.parent[x])

            # So we recursively call Find on its parent and move i's node directly under the representative of this set
        return self.parent[x]


    # Do union of two sets represented by x and y.
    def Union(self, x, y):

        # Find current sets of x and y
        xset = self.find(x)
        yset = self.find(y)

        # If they are already in same set
        if xset == yset:
            return
        if self.element_cnt[xset] + self.element_cnt[yset] > self.threshold:
            return

        # Put smaller ranked item under bigger ranked item if ranks are different (balancing of ranks)
        if self.rank[xset] < self.rank[yset]:
            self.components.remove(self.parent[xset])
            self.parent[xset] = yset
            self.element_cnt[yset] += self.element_cnt[xset]


        elif self.rank[xset] > self.rank[yset]:
            self.components.remove(self.parent[yset])
            self.parent[yset] = xset
            self.element_cnt[xset] += self.element_cnt[yset]

        # If ranks are same, then move y under x (doesn't matter which one goes where) and increment rank of x's tree
        else:
            self.components.remove(self.parent[yset])
            self.parent[yset] = xset
            self.rank[xset] = self.rank[xset] + 1
            self.element_cnt[xset] += self.element_cnt[yset]

def priority_based_linkage(G, threshold = 100, visit_order = []):
    '''
        G to be in the form [(u,v,p),..] denoting list of tuples (node1, node2 and priority)
        where priority needs to be a consecutive number(1,2,3 and so on)
        and lower the value higher the priority i.e. Priority(1>2>3 and so on)

        visit_order is an optional parameter providing users an option to input the visit ordering of nodes.
        Input format [u1,u2,u3...un], list of nodes, u1 will be visited before u2 and u2 before u3 and so on.
        If the user doesn't provide any ordering, the nodes will be visited in any order.

    '''

    # Initialisation
    nodes = set()
    priorities = set()
    edges = {}

    for link in G:
        u = link[0];v = link[1];p = link[2];
        nodes.add(u);nodes.add(v);

        # Create edge
        if (u,p) in edges:
            edges[(u,p)].append(v)
        else:
            edges[(u,p)] = [v]

        if (v,p) in edges:
            edges[(v,p)].append(u)
        else:
            edges[(v,p)] = [u]

        # Create list of priorities
            priorities.add(p)

    if visit_order == []:
        visit_order = nodes


    obj = DisjSet(threshold, visit_order)
    for priority in priorities:
        for node in visit_order:
            if (node,priority) not in edges:
                continue
            for connected_node in edges[(node,priority)]:
                obj.Union(node,connected_node)

    components = {}
    for node in visit_order:
        parent = obj.find(node)
        if parent not in components:
            components[parent] = [node]
        else:
            components[parent].append(node)

    return list(components.values())
