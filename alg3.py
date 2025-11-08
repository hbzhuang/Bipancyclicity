from Hypercube import hypercube
import random
import networkx as nx
from alg2 import HP_FFD
# from networkx import nx
# import matplotlib.pyplot as plt

def CYCLE_FFD(nn, Graph, V_0, V_1, F, e_0, FFD, leng):
    F_copy = F.copy()
    F_copy2 = F.copy()
    F_copy3 = F.copy()
    Cycle_edges = []
    z = e_0[0]
    w = e_0[1]

    if nn == 2 or nn == 3:
        flag = 0
        for path in nx.all_simple_paths(Graph, z, w):
            if len(path) == leng:
                if z == path[0] and w == path[-1]:
                    Cycle_nodes = path
                    flag = 1
                    break
                if w == path[0] and z == path[-1]:
                    Cycle_nodes = path
                    flag = 1
                    break
                for i in range(len(path) - 1):
                    if z == path[i] and w == path[i + 1]:
                        Cycle_nodes = path
                        flag = 1
                        break
                    if z == path[i] and w == path[i + 1]:
                        Cycle_nodes = path
                        flag = 1
                        break
            if flag == 1:
                break

        for i in range(len(Cycle_nodes) - 1):
            e = (Cycle_nodes[i], Cycle_nodes[i+1])
            Cycle_edges.append(e)

        Cycle_edges.append((Cycle_nodes[-1], Cycle_nodes[0])) # 使其形成一个环

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

        if 4 <= leng <= int(len(Graph.nodes)/2):
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
            Cycle_0 = CYCLE_FFD(nn-1, Q_sub[locate], V_0, V_1, F_copy2, e_0, FFD_0, leng)
            Cycle_edges.extend(Cycle_0)

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
                    e_cross0 = (a, a_opposite0)
                    e_cross1 = (a_star, a_opposite1)
                    if Graph.has_edge(a, a_opposite0) and Graph.has_edge(a_star, a_opposite1):
                        e_locate = e
                        Cycle_edges.append(e_cross0)
                        Cycle_edges.append(e_cross1)
                        break

            HP_0 = HP_FFD(nn-1, Q_sub[locate], V_0, V_1, F_copy2, e_0, e_locate, FFD_0)
            Cycle_edges.extend(HP_0)
            Cycle_edges.append((z,w))

            if e_locate in Cycle_edges:
                Cycle_edges.remove(e_locate)
            else:
                i0 = e_locate[0]
                i1 = e_locate[1]
                Cycle_edges.remove((i1,i0))

            if leng == int(len(Graph.nodes)/2) + 2:
                Cycle_edges.append(e_new)
            else:
                Cycle_1 = CYCLE_FFD(nn - 1, Q_sub[opposite], V_0, V_1, F_copy3, e_new, FFD_1, leng - int(len(Graph.nodes)/2))
                Cycle_edges.extend(Cycle_1)
                if e_new in Cycle_edges:
                    Cycle_edges.remove(e_new)
                else:
                    i0 = e_new[0]
                    i1 = e_new[1]
                    Cycle_edges.remove((i1, i0))
    return Cycle_edges

def is_right_cycle_FFD(Graph, e_0, FFD, leng):
    z = e_0[0]
    w = e_0[1]
    G = nx.Graph()
    G.add_edges_from(Graph)
    if e_0 not in FFD:
        print('Fault')
    if G.has_edge(z,w):
        if nx.has_path(G, z, w):
            if len(G.nodes) == leng:
                num = 0
                for u in G.nodes:
                    if G.degree(u) == 2:
                        num = num + 1
                if num == len(G.nodes):
                    return True
                else:
                    return False
            else:
                return False
    else:
        return False



if __name__ == '__main__':
    n = 4
    F_rest = [0, 0, 0, 2]
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
    random.shuffle(N)  # N denotes the dimension
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

    S_P = random.sample(FFD, 1)
    e_00 = S_P[0]

    print(e_00)

    length = 4

    print(len(Q_G.nodes))

    for i in range(int(len(Q_G.nodes)/2) - 1):
        print(length)
        Cycle = CYCLE_FFD(n, Q_G, V_0, V_1, F, e_00, FFD, length)
        is_right_cycle_FFD(Cycle, e_00, FFD, length)
        length = length + 2

