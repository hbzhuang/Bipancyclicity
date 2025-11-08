from Hypercube import hypercube
import random
import networkx as nx
# from networkx import nx
# import matplotlib.pyplot as plt

def HP(nn, Graph, V_00, V_11, F, s, d):
    F_copy = F.copy()
    F_copy2 = F.copy()
    F_copy3 = F.copy()
    HP_edges = []

    if nn == 2 or nn == 3:
        for path in nx.all_simple_paths(Graph, s, d):
            if len(path) == len(list(Graph.nodes)):
                HP_nodes = path
                break

        for i in range(len(HP_nodes) - 1):
            e = (HP_nodes[i],HP_nodes[i+1])
            HP_edges.append(e)

    else:
        maxfault = max(len(i) for i in F_copy.values())
        for ks, vs in F_copy.items():
            if len(vs) == maxfault:
                maxdim = ks

        V_Partion_0 = []
        V_Partion_1 = []
        for u in Graph.nodes:
            if u[len(u) - 1 - maxdim] == '0':
                V_Partion_0.append(u)
            else:
                V_Partion_1.append(u)
        Q_sub = dict()
        Q_sub['0'] = nx.induced_subgraph(Graph, V_Partion_0)
        Q_sub['1'] = nx.induced_subgraph(Graph, V_Partion_1)

        if s[len(s) - 1 - maxdim] == d[len(d) - 1 - maxdim]:
            locate = s[len(s) - 1 - maxdim]
            totalloc = ['0', '1']
            totalloc.remove(locate)
            opposite = totalloc[0]
            del F_copy2[maxdim]
            del F_copy3[maxdim]
            for i in F_copy2.keys():
                F_2 = []
                F_3 = []
                for f in F_copy2[i]:
                    if f[0] in Q_sub[locate].nodes and f[1] in Q_sub[locate].nodes:
                        F_2.append(f)
                    else:
                        F_3.append(f)
                F_copy2[i] = F_2
                F_copy3[i] = F_3
            HP_0 = HP(nn-1, Q_sub[locate], V_00, V_11, F_copy2, s, d)
            HP_edges.extend(HP_0)
            for e in HP_0:
                a = e[0]
                a_star = e[1]
                a_opposite1 = a[0: len(s) - 1 - maxdim] + opposite + a[len(s)- maxdim: len(s)]
                a_opposite2 = a_star[0: len(s) - 1 - maxdim] + opposite + a_star[len(s)- maxdim: len(s)]
                e1 = (a, a_opposite1)
                e2 = (a_star, a_opposite2)
                if Graph.has_edge(a, a_opposite1) and Graph.has_edge(a_star, a_opposite2):
                    HP_edges.append(e1)
                    HP_edges.append(e2)
                    HP_edges.remove(e)
                    break
            HP_1 = HP(nn-1, Q_sub[opposite], V_00, V_11, F_copy3, a_opposite1, a_opposite2)
            HP_edges.extend(HP_1)

        else:
            locate = s[len(s) - 1 - maxdim]
            totalloc = ['0', '1']
            totalloc.remove(locate)
            opposite = totalloc[0]

            del F_copy2[maxdim]
            del F_copy3[maxdim]
            for i in F_copy2.keys():
                F_2 = []
                F_3 = []
                for f in F_copy2[i]:
                    if f[0] in Q_sub[locate].nodes and f[1] in Q_sub[locate].nodes:
                        F_2.append(f)
                    else:
                        F_3.append(f)
                F_copy2[i] = F_2
                F_copy3[i] = F_3

            if s in V_00:
                V_even = list(set(V_11) & set(Q_sub[locate].nodes))
            if s in V_11:
                V_even = list(set(V_00) & set(Q_sub[locate].nodes))

            for u in V_even:
                u_star = u[0: len(u) - 1 -maxdim] + opposite + u[len(u) - maxdim: len(u)]
                e_0 = (u, u_star)
                if Graph.has_edge(u, u_star):
                    HP_0 = HP(nn - 1, Q_sub[locate], V_00, V_11, F_copy2, s, u)
                    HP_edges.extend(HP_0)
                    HP_edges.append(e_0)
                    HP_1 = HP(nn - 1, Q_sub[opposite], V_00, V_11, F_copy3, u_star, d)
                    HP_edges.extend(HP_1)
                    break
    return HP_edges

def is_path_HP(Ham, s, d):
    G = nx.Graph()
    G.add_edges_from(Ham)
    if nx.has_path(G, s, d):
        if len(G.nodes) - 1 == nx.shortest_path_length(G, s, d):
            num_0 = 0
            num_1 = 0
            for u in G.nodes:
                if G.degree(u) == 1:
                    num_0 = num_0 + 1
                if G.degree(u) == 2:
                    num_1 = num_1 + 1
            if num_0 == 2 and num_1 == len(G.nodes) - 2:
                return True
            else:
                return False
        else:
            return False
    else:
        return False

if __name__ == '__main__':
    n = 7
    F_rest = [0, 0, 1, 3, 7, 15, 31]
    Q_n = hypercube(n)
    Q_nodes = Q_n.nodes
    Q_edges = Q_n.edges
    Q_G = nx.Graph()

    for i in range(len(Q_edges)):
        Q_G.add_edges_from(Q_edges[i])

    V_0 = []    # The set of odd nodes
    V_1 = []    # The set of even nodes
    for i in range(len(Q_nodes)):
        for u in Q_nodes[i]:
            oddif = u.count('1')
            if oddif % 2 == 1:
                V_0.append(u)
            else:
                V_1.append(u)



    # The set denoting the dimensions
    N = [i for i in range(n)]
    random.shuffle(N)
    num = 0
    F = dict()
    for i in N:
        F_act = F_rest[num]
        F[i] = random.sample(Q_edges[i], F_act)
        Q_G.remove_edges_from(F[i])
        num += 1





    x = "1110000"  # x should be an odd node
    y = "0000000"  # y should be an even node
    Hami = HP(n, Q_G, V_0, V_1, F, x, y)

    is_path_HP(Hami, x, y)
