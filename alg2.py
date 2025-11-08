from Hypercube import hypercube
import random
import networkx as nx
from alg1 import HP
# from networkx import nx
# import matplotlib.pyplot as plt

def HP_FFD(nn, Graph, V_0, V_1, F, e_0, e_1, FFD):
    F_copy = F.copy()
    F_copy2 = F.copy()
    F_copy3 = F.copy()
    HP_edges = []
    z = e_0[0]
    w = e_0[1]
    c = e_1[0]
    d = e_1[1]
    if nn == 2 or nn == 3:
        flag = 0
        for path in nx.all_simple_paths(Graph, z, w):
            if len(path) == len(Graph.nodes):
                for i in range(len(path) - 1):
                    if c == path[i] and d == path[i + 1]:
                        HP_nodes = path
                        flag = 1
                        break
                    if d == path[i] and c == path[i + 1]:
                        HP_nodes = path
                        flag = 1
                        break
            if flag == 1:
                break

        for i in range(len(HP_nodes) - 1):
            e = (HP_nodes[i], HP_nodes[i+1])
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

        if z[len(z) - 1 - maxdim] == c[len(c) - 1 - maxdim]:
            locate = z[len(z) - 1 - maxdim]
            totalloc = ['0', '1']
            totalloc.remove(locate)
            opposite = totalloc[0]
            FFD_0 = []
            FFD_1 = []
            for g in FFD:
                if g[0] in Q_sub[locate].nodes and g[1] in Q_sub[locate].nodes:
                    FFD_0.append(g)
                else :
                    FFD_1.append(g)
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
            HP_0 = HP_FFD(nn-1, Q_sub[locate], V_0, V_1, F_copy2, e_0, e_1, FFD_0)
            HP_edges.extend(HP_0)
            for e in HP_0:
                L0 = set(e) & set(e_1)
                if len(L0) != 2:
                    a = e[0]
                    a_star = e[1]
                    a_opposite0 = a[0: len(a) - 1 - maxdim] + opposite + a[len(a) - maxdim: len(a)]
                    a_opposite1 = a_star[0: len(a_star) - 1 - maxdim] + opposite + a_star[len(a_star) - maxdim: len(a_star)]
                    e_cross0 = (a, a_opposite0)
                    e_cross1 = (a_star, a_opposite1)
                    if Graph.has_edge(a, a_opposite0) and Graph.has_edge(a_star, a_opposite1):
                        HP_edges.append(e_cross0)
                        HP_edges.append(e_cross1)
                        HP_edges.remove(e)
                        break
            HP_1 = HP(nn-1, Q_sub[opposite], V_0, V_1, F_copy3, a_opposite0, a_opposite1)
            HP_edges.extend(HP_1)

        else:
            locate = z[len(z) - 1 - maxdim]
            totalloc = ['0', '1']
            totalloc.remove(locate)
            opposite = totalloc[0]
            FFD_0 = []
            FFD_1 = []
            for g in FFD:
                if g[0] in Q_sub[locate].nodes and g[1] in Q_sub[locate].nodes:
                    FFD_0.append(g)
                else :
                    FFD_1.append(g)
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

            for e in FFD_0:
                L1 = set(e) & set(e_0)
                if len(L1) != 2:
                    a = e[0]
                    a_star = e[1]
                    a_opposite0 = a[0: len(a) - 1 - maxdim] + opposite + a[len(a) - maxdim: len(a)]
                    a_opposite1 = a_star[0: len(a_star) - 1 - maxdim] + opposite + a_star[len(a_star) - maxdim: len(a_star)]
                    e_new = (a_opposite0, a_opposite1)
                    L2 = set(e_new) & set(e_1)
                    if len(L2) != 2:
                        e_cross0 = (a, a_opposite0)
                        e_cross1 = (a_star, a_opposite1)
                        if Graph.has_edge(a, a_opposite0) and Graph.has_edge(a_star, a_opposite1):
                            e_locate = e
                            HP_edges.append(e_cross0)
                            HP_edges.append(e_cross1)
                            break
            HP_0 = HP_FFD(nn-1, Q_sub[locate], V_0, V_1, F_copy2, e_0, e_locate, FFD_0)
            HP_edges.extend(HP_0)
            if e_locate in HP_edges:
                HP_edges.remove(e_locate)
            else:
                i0 = e_locate[0]
                i1 = e_locate[1]
                HP_edges.remove((i1,i0))
            HP_1 = HP_FFD(nn-1, Q_sub[opposite], V_0, V_1, F_copy3, e_new, e_1, FFD_1)
            HP_edges.extend(HP_1)
    return HP_edges

def is_right_path(Graph, e_0, e_1, FFD):
    z = e_0[0]
    w = e_0[1]
    c = e_1[0]
    d = e_1[1]
    G = nx.Graph()
    G.add_edges_from(Graph)
    if e_0 not in FFD or e_1 not in FFD:
        print('Fault')
    if G.has_edge(c,d):
        if nx.has_path(G, z, w):
            if len(G.nodes) - 1 == nx.shortest_path_length(G, z, w):
                num_0 = 0
                num_1 = 0
                for u in G.nodes:
                    if G.degree(u) == 1:
                        num_0 = num_0 + 1
                    if G.degree(u) == 2:
                        num_1 = num_1 + 1
                if num_0 == 2 and num_1 == len(G.nodes) - 2:
                    print("Success")
                    return True
                else:
                    return False
            else:
                return False



if __name__ == '__main__':
    n = 6
    F_rest = [0, 0, 1, 3, 7, 15]
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

    num = 0
    F = dict()
    FFD = []

    for i in N:
        F_act = F_rest[num]
        F[i] = random.sample(Q_edges[i], F_act)
        Q_G.remove_edges_from(F[i])
        if F_act == 0:
            FFD.extend(Q_edges[i])
        num += 1

    S_P = random.sample(FFD, 2)
    e_00 = S_P[0]
    e_11 = S_P[1]

    print(e_00)
    print(e_11)

    Hami = HP_FFD(n, Q_G, V_0, V_1, F, e_00, e_11, FFD)
    Q_Hami = nx.Graph()
    Q_Hami.add_edges_from(Hami)
    print(Q_Hami.edges)
    is_right_path(Hami, e_00, e_11, FFD)