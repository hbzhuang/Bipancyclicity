import math

from Hypercube import hypercube
from alg4 import CYCLE, is_right_cycle
import random
from multiprocessing import Pool
import xlwt
import time
import numpy as np
import networkx as nx


def t_link(n, flength, edges_partition, Q_Graph, V_00, V_11, length, F_rest1):

    Graph_copy = Q_Graph.copy()

    f, F = f_num(n, edges_partition)

    FFD_num = []
    for i in range(len(F)):
        if len(F[i]) == 0:
            FFD_num.append(i)

    FFD = []
    for i in FFD_num:
        FFD.extend(edges_partition[i])

    for i in range(len(F)):
        Graph_copy.remove_edges_from(F[i])

    # 生成每维边的图
    E = []
    for i in range(len(edges_partition)):
        G_edge = nx.Graph()
        G_edge.add_edges_from(edges_partition[i])
        E.append(G_edge)

    F_f = []
    for i in range(flength):    # Add flength faulty edges into F_f, which is not FFD edge
        sign = True
        while sign:
            f_choose = random.sample(list(Graph_copy.edges), 1)
            SD = f_choose[0]
            if (SD[0], SD[1]) not in FFD or (SD[1], SD[0]) not in FFD:
                F_f.append(SD)
                sign = False

    Graph_copy.remove_edges_from(F_f)

    # determine f_ran belongs to which dimension
    for f_ran in F_f:
        for i in range(len(E)):
            if E[i].has_edge(f_ran[0], f_ran[1]):
                F[i].append(f_ran)
                break

    suss = capture(n, Graph_copy, V_00, V_11, F, FFD, length, F_rest1)

        # suss_i, record_s, record_d = capture(n, Graph_copy, V_00, V_11, F, s, d)
        # if suss_i == 0:
        #     sd = (record_s, record_d)
        #     SD.append(sd)
        # else:
        #     suss += suss_i

    # if suss <= 5:
    #     print(F)
    #     print(SD)
        # try:
        #     P = HP(n, Graph_copy, V_00, V_11, F, s, d)
        #
        #     if is_path_HP(P, s, d):
        #         suss = suss + 1
        #     # else:
        #     #     suss = suss
        #
        # except Exception:
        #     print(s, d)
        #     print(F)

    return suss


def capture(n, Graph_copy, V_00, V_11, F, FFD, length, F_rest1):
    suss = 0
    try:
        Cycle = CYCLE(n, Graph_copy, V_00, V_11, F, FFD, length, F_rest1)
        if is_right_cycle(Cycle, length):
            suss = 1
        # else:
        #     suss = suss

    except Exception:
        suss = 0

    # return suss, s, d
    return suss



def f_num(n, edges):
    F = dict()
    F[0] = []
    F[1] = []

    if n >= 3:
        f_sum = 0

        for i in range(2, n):
            t = 2 ** (i-1) - 1
            f_sum += t
            F[i] = random.sample(edges[i], t)

    return f_sum, F

def t_core(n, flength, edges_partition, Q_Graph, test_num, V_00, V_11, length, F_rest1):
    suss_sum = 0
    for i in range(test_num):
        suss_i = t_link(n, flength, edges_partition, Q_Graph, V_00, V_11, length, F_rest1)   # the value of suss_i is 0 or 1
        suss_sum += suss_i

    return suss_sum


def pool_core(n, flength, edges_partition, Q_Graph, test_num, processes_num, V_00, V_11, length, F_rest1):
    pool = Pool(processes = processes_num)
    ress = []   # This array stores the success number obtained by the process, but the value of each element is not of type int
    for i in range(processes_num):
        res = pool.apply_async(t_core, (n, flength, edges_partition, Q_Graph, test_num, V_00, V_11, length, F_rest1))    # t_core is responsible for testing the success rate
        ress.append(res)
    pool.close()
    pool.join()
    suss = []   # This array extracts the elements of the ress array as an int type
    for res in ress:
        x = res.get()
        suss.append(x)

    np_suss = np.array(suss)
    sum_suss = np.sum(np_suss)

    return sum_suss



def pool_fin(n, edges_partition, Q_Graph, test_num, processes_num, V_00, V_11, length, F_rest1, th):
    ptest_num = int(test_num / processes_num)   # The number of tests that each process needs to undertake
    f, F_initial = f_num(n, edges_partition)    # Generate theoretical upper bound value f and corresponding fault set

    s1 = "hypercube({0},{1})_bipan.xls".format(n, f)
    hyperQ = xlwt.Workbook(encoding='utf-8')
    sheet1 = hyperQ.add_sheet('hyperQ', cell_overwrite_ok=True)

    kk = 1

    mm = []
    for i in range(int(len(Q_G.nodes)/2) - 1):
        length = length + 2
        suss = []
        flength = 18  # Newly added faulty edge
        time_star0 = time.time()
        while True:
            x = pool_core(n, flength, edges_partition, Q_Graph, ptest_num, processes_num, V_00, V_11, length, F_rest1) # test_num个故障集中成功构造的个数
            suss.append(x)
            mm.append(flength)
            flength = flength + 4
            if flength > 18:
                break

        time_end0 = time.time()
        print('The cycle length is：', length)
        print('The cost time is：', time_end0 - time_star0)
        sheet1.write(0, kk, length)
        for i in range(len(suss)):
            sheet1.write(i + 1, kk, int(suss[i]))
        kk += 1

    for i in range(len(mm)):
        sheet1.write(i + 1, 0, f + mm[i])

    hyperQ.save(s1)


if __name__ == '__main__':
    n = 6
    test_number = 10000
    th = 1
    length = 2
    F_rest1 = [0, 0, 0]
    for i in range(3, n):
        y = 2 ** (i - 1) - 2
        F_rest1.append(y)

    Q_n = hypercube(n)
    Q_nodes = Q_n.nodes
    Q_edges = Q_n.edges
    Q_G = nx.Graph()

    for i in range(len(Q_edges)):
        Q_G.add_edges_from(Q_edges[i])

    # f, F_initial = f_num(n, k, edges)

    # suss_num = test_link(n, k, f, F_initial, edges, BCube)
    # suss_num = test_core(n, k, 6, F_initial, edges, BCube, test_number)
    # print(suss_num)

    V_0 = []  # The set of odd nodes
    V_1 = []  # The set of even nodes
    for u in Q_G.nodes:
        oddif = u.count('1')
        if oddif % 2 == 1:
            V_0.append(u)
        else:
            V_1.append(u)

    time_star = time.time()

    pool_fin(n, Q_edges, Q_G, test_number, 20, V_0, V_1, length, F_rest1, th)

    time_end = time.time()

    print(time_end - time_star)