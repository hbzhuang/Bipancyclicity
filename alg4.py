from Hypercube import hypercube
import random
import networkx as nx
from alg1 import HP
from alg3 import CYCLE_FFD
# from networkx import nx
# import matplotlib.pyplot as plt

def CYCLE(nn, Graph, V_0, V_1, F, FFD, leng, F_res):
    F_copy = F.copy()
    F_copy2 = F.copy()
    F_copy3 = F.copy()
    Cycle_edges = []

    F_res_copy = F_res[:nn - 1]


    if nn == 2 or nn == 3:

        for cycle in nx.simple_cycles(Graph):
            if len(cycle) == leng:
                Cycle_nodes = cycle
                break

        for i in range(len(Cycle_nodes) - 1):
            e = (Cycle_nodes[i], Cycle_nodes[i + 1])
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
            locate = '0'
            opposite = '1'
            FFD_0 = []
            FFD_1 = []
            for g in FFD:
                if g[0] in Q_sub['0'].nodes and g[1] in Q_sub['0'].nodes:
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
            Cycle_0 = CYCLE(nn - 1, Q_sub[locate], V_0, V_1, F_copy2, FFD_0, leng, F_res_copy)
            Cycle_edges.extend(Cycle_0)

        else:
            FFD_0 = []
            FFD_1 = []
            for g in FFD:
                if g[0] in Q_sub['0'].nodes and g[1] in Q_sub['0'].nodes:
                    FFD_0.append(g)
                else :
                    FFD_1.append(g)
            del F_copy2[maxdim]
            del F_copy3[maxdim]
            Q_sub_0Count = []
            Q_sub_1Count = []
            for i in F_copy2.keys():
                F_2 = []
                F_3 = []
                num_0 = 0
                num_1 = 0
                for f in F_copy2[i]:
                    if f[0] in Q_sub['0'].nodes and f[1] in Q_sub['0'].nodes:
                        F_2.append(f)
                        num_0 = num_0 + 1
                    else:
                        F_3.append(f)
                        num_1 = num_1 + 1
                F_copy2[i] = F_2
                F_copy3[i] = F_3
                Q_sub_0Count.append(num_0)
                Q_sub_1Count.append(num_1)

            Q_sub_0Count.sort()
            Q_sub_1Count.sort()

            for i in range(len(Q_sub_0Count)):
                if Q_sub_0Count[i] <= F_res[i]:
                    locate = '0'
                else:
                    locate = '1'
                    break

            if locate == '0':
                FFD_opposite = FFD_1
            else:
                FFD_opposite = FFD_0

            for e in FFD_opposite:
                a = e[0]
                a_star = e[1]
                a_locate0 = a[0: len(a) - 1 - maxdim] + locate + a[len(a) - maxdim: len(a)]
                a_locate1 = a_star[0: len(a_star) - 1 - maxdim] + locate + a_star[len(a_star) - maxdim: len(a_star)]
                e_new = (a_locate0, a_locate1)
                e_cross0 = (a, a_locate0)
                e_cross1 = (a_star, a_locate1)
                if Graph.has_edge(a, a_locate0) and Graph.has_edge(a_star, a_locate1):
                    Cycle_edges.append(e_cross0)
                    Cycle_edges.append(e_cross1)
                    break

            if locate == '0':       # locate指代符合较小限制元组的子图编号
                HP_opposite = HP(nn - 1, Q_sub['1'], V_0, V_1, F_copy3, a, a_star)
            else:
                HP_opposite = HP(nn - 1, Q_sub['0'], V_0, V_1, F_copy2, a, a_star)
            Cycle_edges.extend(HP_opposite)

            if leng == int(len(Graph.nodes)/2) + 2:
                Cycle_edges.append(e_new)
            else:
                if locate == '0':
                    Cycle_locate = CYCLE_FFD(nn - 1, Q_sub['0'], V_0, V_1, F_copy2, e_new, FFD_0, leng - int(len(Graph.nodes)/2))
                else:
                    Cycle_locate = CYCLE_FFD(nn - 1, Q_sub['1'], V_0, V_1, F_copy3, e_new, FFD_1, leng - int(len(Graph.nodes)/2))

                Cycle_edges.extend(Cycle_locate)
                if e_new in Cycle_edges:
                    Cycle_edges.remove(e_new)
                else:
                    i0 = e_new[0]
                    i1 = e_new[1]
                    Cycle_edges.remove((i1, i0))
    return Cycle_edges

def is_right_cycle(Graph, leng):
    G = nx.Graph()
    G.add_edges_from(Graph)
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



if __name__ == '__main__':
    n = 6
    F_rest = [0, 0, 1, 3, 7, 15]
    F_rest1 = [0, 0, 0, 2, 6, 14]

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
    F = {0: [], 1: [], 2: [('001011', '001111')], 3: [('100110', '101110'), ('000111', '001111'), ('000011', '001011')], 4: [('101110', '111110'), ('101101', '111101'), ('100111', '110111'), ('101000', '111000'), ('100000', '110000'), ('100100', '110100'), ('100011', '110011')], 5: [('000101', '100101'), ('000110', '100110'), ('000000', '100000'), ('010111', '110111'), ('010011', '110011'), ('001010', '101010'), ('011100', '111100'), ('010001', '110001'), ('000011', '100011'), ('011000', '111000'), ('001111', '101111'), ('011111', '111111'), ('001000', '101000'), ('000111', '100111'), ('000001', '100001')]}
    FFD = []

    # for i in N:
    #     F_act = F_rest[num]
    #     F[i] = random.sample(Q_edges[i], F_act)
    #     Q_G.remove_edges_from(F[i])
    #     if F_act == 0:
    #         FFD.extend(Q_edges[i])
    #     num += 1

    num_x = 0
    for i in range(n):
        num_x += len(F[i])
        Q_G.remove_edges_from(F[i])
        if len(F[i]) == 0:
            FFD.extend(Q_edges[i])

    length = 56
    Cycle = CYCLE(n, Q_G, V_0, V_1, F, FFD, length, F_rest1)
    is_right_cycle(Cycle, length)


    # for i in range(int(len(Q_G.nodes)/2) - 1):
    #     length = length + 2
    #     Cycle = CYCLE(n, Q_G, V_0, V_1, F, FFD, length, F_rest1)
    #     is_right_cycle(Cycle, length)
    #     print(length)
    #     print(Cycle)


