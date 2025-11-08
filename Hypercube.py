class hypercube():
    def __init__(self, n):
        self.n = n
        self.nodes = self.getnodes(n)
        self.edges = self.getedges(n)

    def getnodes(self, n):
        # n-bit address, each of which is 0 or 1
        if n == 1:
            node_add = ['0', '1']
        else:
            node_add = []
            node_subone = ['0', '1']
            node_subtwo = ['0', '1']
            for i in range(1, n):
                subone = []
                subtwo = []
                for l in range(len(node_subone)):
                    vertex = '0' + node_subone[l]
                    subone.append(vertex)
                for l in range(len(node_subtwo)):
                    vertex = '1' + node_subtwo[l]
                    subtwo.append(vertex)
                if i < n - 1:
                    node_subone = subone.copy()
                    node_subone.extend(subtwo)
                    node_subtwo = node_subone.copy()
                else:
                    node_subone = subone.copy()
                    node_subtwo = subtwo.copy()


            node_add.append(node_subone)
            node_add.append(node_subtwo)

        return node_add

    def getedges(self, n):
        vertices = self.nodes
        vertices_copy = vertices[0].copy()
        vertices_copy.extend(vertices[1])

        edges = []
        for i in range(n):
            k = n - 1 - i
            edge_k = []
            V_copy = vertices_copy.copy()
            for u in V_copy:
                u_0_k = u[0: k]
                u_k = u[k]
                u_k_n = u[k+1: n]
                if u_k == '0':
                    u_k_copy = '1'
                else:
                    u_k_copy = '0'
                u_v = u_0_k + u_k_copy + u_k_n
                e = (u, u_v)
                edge_k.append(e)
                V_copy.remove(u_v)
            edges.append(edge_k)

        return edges




if __name__ == '__main__':
    n = 3
    print(hypercube(n).edges)