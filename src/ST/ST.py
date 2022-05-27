# -*- coding: utf-8 -*-
"""
"""
from charm.toolbox.pairinggroup import PairingGroup, ZR, G1, G2, GT, pair
from charm.toolbox.ABEncMultiAuth import ABEncMultiAuth
import time
import numpy as np
import sys
sys.path.append('../')
from common.image import *
from common.msp import *


class MJ18(ABEncMultiAuth):
    def __init__(self, groupObj, verbose=False):
        ABEncMultiAuth.__init__(self)
        global group, g, g2, delta1, delta2, theta1, theta2, omega, g1, d
        group = groupObj

        g = group.random(G1)
        g2 = group.random(G1)
        delta1 = group.random(ZR)
        delta2 = group.random(ZR)
        theta1 = group.random(ZR)
        theta2 = group.random(ZR)
        omega = group.random(ZR)
        g1 = g_exp(g, omega)[0]
        d = group.random(ZR)

    def setup_ippre(self, n):
        start = time.time()
        w1n = random_array(n)
        t1n = random_array(n)
        f1n = random_array(n)
        f2n = random_array(n)
        h1n = random_array(n)
        h2n = random_array(n)

        w2n = []
        for i in range(n):
            temp = (omega + delta2 * w1n[i]) / delta1
            w2n.append(temp)

        t2n = []
        for i in range(n):
            temp = (omega + theta2 * t1n[i]) / theta1
            t2n.append(temp)

        W1n = g_exp_n(g, w1n)
        W2n = g_exp_n(g, w2n)
        T1n = g_exp_n(g, t1n)
        T2n = g_exp_n(g, t2n)
        F1n = g_exp_n(g, f1n)
        F2n = g_exp_n(g, f2n)
        H1n = g_exp_n(g, h1n)
        H2n = g_exp_n(g, h2n)

        U1 = g_exp(g, delta1)
        U2 = g_exp(g, delta2)
        V1 = g_exp(g, theta1)
        V2 = g_exp(g, theta2)
        egg2 = pair(g, g2)

        PK3 = {'W1n': W1n, 'W2n': W2n, 'F1n': F1n, 'F2n': F2n}
        PK4 = {'T1n': T1n, 'T2n': T2n, 'H1n': H1n, 'H2n': H2n}
        PK5 = {'U1': U1, 'U2': U2, 'V1': V1, 'V2': V2}
        PK = {'g': g, 'g1': g1, 'PK3': PK3, 'PK4': PK4, 'PK5': PK5, 'egg2': egg2}

        MSK1 = {'w1n': w1n, 'w2n': w2n, 't1n': t1n, 't2n': t2n, 'f1n': f1n, 'f2n': f2n, 'h1n': h1n, 'h2n': h2n}
        MSK2 = {'delta1': delta1, 'delta2': delta2, 'theta1': theta1, 'theta2': theta2}
        MSK = {'MSK1': MSK1, 'MSK2': MSK2}

        end = time.time()
        rt = end - start
        return PK, MSK, rt

    def enc_ippre(self, n, PK, M):
        start = time.time()
        x, v, xZ = testcase_generate(n)

        s1 = group.random(ZR)
        s2 = group.random(ZR)
        s3 = group.random(ZR)
        s4 = group.random(ZR)

        A = g_exp(g, s2)[0]
        B = g_exp(g1, s1)[0]
        C1n = CT3_function(n, x, s1, s2, s3, PK['PK3']['W1n'], PK['PK3']['F1n'], PK['PK5']['U1'])
        C2n = CT3_function(n, x, s1, s2, s3, PK['PK3']['W2n'], PK['PK3']['F2n'], PK['PK5']['U2'])
        C3n = CT3_function(n, x, s1, s2, s4, PK['PK4']['T1n'], PK['PK4']['H1n'], PK['PK5']['V1'])
        C4n = CT3_function(n, x, s1, s2, s4, PK['PK4']['T2n'], PK['PK4']['H2n'], PK['PK5']['V2'])
        CT3 = {'C1n': C1n, 'C2n': C2n, 'C3n': C3n, 'C4n': C4n}

        D = g_exp(PK['egg2'], -s2)[0] * M
        CT = {'A': A, 'B': B, 'CT3': CT3, 'D': D}

        end = time.time()
        rt = end - start
        return CT, v, rt

    def keyGen_ippre(self, n, v, MSK):
        start = time.time()

        landa1 = group.random(ZR)
        landa2 = group.random(ZR)
        rn = random_array(n)
        phin = random_array(n)
        K1n = SK3_function(n, -delta2, rn, landa1, v, MSK['MSK1']['w2n'])
        K2n = SK3_function(n, delta1, rn, -landa1, v, MSK['MSK1']['w1n'])
        K3n = SK3_function(n, -theta2, phin, landa2, v, MSK['MSK1']['t2n'])
        K4n = SK3_function(n, theta1, phin, -landa2, v, MSK['MSK1']['t1n'])
        KA = KA_function_(n, K1n, K2n, K3n, K4n, MSK['MSK1']['f1n'], MSK['MSK1']['f2n'], MSK['MSK1']['h1n'],
                          MSK['MSK1']['h2n'])
        KB = KB_function_(n, rn, phin)
        SK3 = {'K1n': K1n, 'K2n': K2n, 'K3n': K3n, 'K4n': K4n}
        SK = {'KA': KA, 'KB': KB, 'SK3': SK3}

        end = time.time()
        rt = end - start
        return SK, rt

    def reKeyGen_ippre(self, ahnipe, n, v, M1, PK, MSK):
        start = time.time()

        CT1, v_, EncTime_ = ahnipe.enc_ippre(n, PK, M1)
        SK_, KeyGenTime_ = ahnipe.keyGen_ippre(n, v_, MSK)

        landa1_ = group.random(ZR)
        landa2_ = group.random(ZR)
        rn_ = random_array(n)
        phin_ = random_array(n)

        K1n_ = RK3_function(n, -delta2, rn_, landa1_, v, MSK['MSK1']['w2n'], d * delta2)
        K2n_ = RK3_function(n, delta1, rn_, -landa1_, v, MSK['MSK1']['w1n'], -d * delta1)
        K3n_ = RK3_function(n, -theta2, phin_, landa2_, v, MSK['MSK1']['t2n'], d * theta2)
        K4n_ = RK3_function(n, theta1, phin_, -landa2_, v, MSK['MSK1']['t1n'], -d * theta1)

        KA_ = KA_function_(n, K1n_, K2n_, K3n_, K4n_, MSK['MSK1']['f1n'], MSK['MSK1']['f2n'], MSK['MSK1']['h1n'],
                           MSK['MSK1']['h2n'])
        KB_ = KB_function_(n, rn_, phin_)
        SK3_ = {'K1n': K1n_, 'K2n': K2n_, 'K3n': K3n_, 'K4n': K4n_}
        RK = {'KA_': KA_, 'KB_': KB_, 'SK3': SK3_}

        end = time.time()
        rt = end - start
        return RK, CT1, SK_, v_, rt

    def reenc_ippre(self, n, RK, CT, CT1):
        start = time.time()

        A = CT['A']
        B = CT['B']
        D = CT['D']
        CT2 = CT2_function(n, RK, CT)
        CT_ = {'A': A, 'B': B, 'CT1': CT1, 'CT2': CT2, 'D': D}

        end = time.time()
        rt = end - start
        return CT_, rt

    def dec1_ippre(self, n, SK, CT, SK_, CT_):
        start = time.time()

        M_output_1 = M_output_1_function(n, SK, CT)
        M1_output = M_output_1_function(n, SK_, CT_['CT1'])

        end = time.time()
        rt = end - start
        return M_output_1, M1_output, rt

    def dec2_ippre(self, CT_):
        start = time.time()

        B = CT_['B']
        g2d = g_exp(g2, d)[0]
        CT3 = pair(B, g2d)

        CT2 = CT_['CT2']
        M_output_2 = CT_['D'] * CT2 * CT3

        end = time.time()
        rt = end - start
        return M_output_2, rt


def random_array(n):
    array = []
    for i in range(n):
        a = group.random(ZR)
        array.append(a)
    return array


def testcase_generate(n):
    xi = np.random.randint(10, size=n)
    xi[n - 1] = 1
    xV = random_perpendicular_vector(n, xi)
    xZ = random_perpendicular_vector(n, xi)

    VX1 = check_perpendicular(n, xi, xV)
    VX2 = check_perpendicular(n, xi, xZ)
    return xi, xV, xZ


def random_perpendicular_vector(n, vec):
    res = np.random.randint(10, size=n)
    sum = 0
    for i in range(n):
        sum = sum + vec[i] * res[i]
    res[n - 1] = res[n - 1] - sum
    return res


def check_perpendicular(n, xi, xV):
    sum = 0
    for i in range(n):
        sum = sum + xi[i] * xV[i]
    return sum


def CT3_function(n, xi, s1, s2, s3, W1n, F1n, U1):
    res = []
    for i in range(n):
        equ1 = g_exp(W1n[i], s1)[0]
        equ2 = g_exp(F1n[i], s2)[0]
        equ3 = g_exp(U1[0], xi[i] * s3)[0]
        res.append(equ1 * equ2 * equ3)
    return res


def CT2_function(n, RK, CT):
    temp = 1
    for i in range(n):
        equ1 = pair(CT['CT3']['C1n'][i], RK['SK3']['K1n'][i])
        equ2 = pair(CT['CT3']['C2n'][i], RK['SK3']['K2n'][i])
        equ3 = pair(CT['CT3']['C3n'][i], RK['SK3']['K3n'][i])
        equ4 = pair(CT['CT3']['C4n'][i], RK['SK3']['K4n'][i])
        temp = temp * equ1 * equ2 * equ3 * equ4
    CT2 = pair(CT['A'], RK['KA_']) * pair(CT['B'], RK['KB_']) * temp
    return CT2


def M_output_1_function(n, SK, CT):
    D = CT['D']
    A = CT['A']
    B = CT['B']
    KA = SK['KA']
    KB = SK['KB']

    temp = 1
    for i in range(n):
        equ1 = pair(CT['CT3']['C1n'][i], SK['SK3']['K1n'][i])
        equ2 = pair(CT['CT3']['C2n'][i], SK['SK3']['K2n'][i])
        equ3 = pair(CT['CT3']['C3n'][i], SK['SK3']['K3n'][i])
        equ4 = pair(CT['CT3']['C4n'][i], SK['SK3']['K4n'][i])
        temp = temp * equ1 * equ2 * equ3 * equ4
    res = D * pair(A, KA) * pair(B, KB) * temp
    return res


def SK3_function(n, theta2, rn, landa1, v, w2n):
    res = []
    for i in range(n):
        equ1 = g_exp(g, theta2 * rn[i])[0]
        equ2 = g_exp(g, landa1 * v[i] * w2n[i])[0]
        res.append(equ1 * equ2)
    return res


def RK3_function(n, theta2, rn, landa1, v, w2n, dtheta2):
    res = []
    for i in range(n):
        equ1 = g_exp(g, theta2 * rn[i])[0]
        equ2 = g_exp(g, landa1 * v[i] * w2n[i])[0]
        equ3 = g_exp(g2, dtheta2)[0]
        res.append(equ1 * equ2 * equ3)
    return res


def KA_function_(n, K1n, K2n, K3n, K4n, f1n, f2n, h1n, h2n):
    temp = 1
    for i in range(n):
        equ1 = g_exp(K1n[i], -f1n[i])[0]
        equ2 = g_exp(K2n[i], -f2n[i])[0]
        equ3 = g_exp(K3n[i], -h1n[i])[0]
        equ4 = g_exp(K4n[i], -h2n[i])[0]
        temp = temp * equ1 * equ2 * equ3 * equ4

    KA = g2 * temp
    return KA


def KB_function_(n, r1n, r2n):
    KB = 1
    for i in range(n):
        equ = g_exp(g, -(r1n[i] + r2n[i]))
        KB = KB * equ[0]
    return KB


def g_exp_n(g1Val, arrayInput):
    array = []
    for i in range(len(arrayInput)):
        val = g1Val ** arrayInput[i]
        array.append(val)
    return array


def g_exp(g1Val, arrayInput):
    array = []
    val = g1Val ** arrayInput
    array.append(val)
    return array


def main():
    groupObj = PairingGroup('SS512')
    n_array = np.arange(5, 30, 5)
    output_txt = './ST.txt'

    with open(output_txt, 'w+', encoding='utf-8') as f:
        f.write(
            "Seq SetupAveTime       KeygenAveTime      EncAveTime         Dec1AVeTime        RekeygenAveTime    ReencAveTime       Dec2AveTime   " + '\n')
        for i in range(len(n_array)):
            seq = 5
            sttot, kgtot, enctot, dec1tot, rktot, retot, dec2tot = 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0
            for j in range(seq):
                ahnipe = MJ18(groupObj)

                n = n_array[i]
                M = group.random(GT)
                M1 = group.random(GT)

                PK, MSK, setuptime = ahnipe.setup_ippre(n)
                CT, v, enctime = ahnipe.enc_ippre(n, PK, M)
                SK, keygentime = ahnipe.keyGen_ippre(n, v, MSK)
                RK, CT1, SK_, v_, rekeygentime = ahnipe.reKeyGen_ippre(ahnipe, n, v, M1, PK, MSK)
                CT_, reenctime = ahnipe.reenc_ippre(n, RK, CT, CT1)

                M_output_1, M1_output, dec1time = ahnipe.dec1_ippre(n, SK, CT, SK_, CT_)
                M_output_2, dec2time = ahnipe.dec2_ippre(CT_)

                print("\nn, seq", n, j)
                print("M1_input:  ", M1)
                print("M1_output: ", M1_output)

                print("M_input:   ", M)
                print("M_output_1:", M_output_1)

                m_inputkey = group.serialize(M).decode("utf-8")
                m_outputkey = group.serialize(M_output_1).decode("utf-8")
                encrypt(m_inputkey)
                decrypt(m_outputkey)

                sttot, kgtot, enctot, dec1tot, rktot, retot, dec2tot = sttot + setuptime, kgtot + keygentime, enctot + enctime, dec1tot + dec1time, rktot + rekeygentime, retot + reenctime, dec2tot + dec2time

            out0 = str(n).zfill(2)
            out1 = str(format(sttot / float(seq), '.16f'))
            out2 = str(format(kgtot / float(seq), '.16f'))
            out3 = str(format(enctot / float(seq), '.16f'))
            out4 = str(format(dec1tot / float(seq), '.16f'))
            out5 = str(format(rktot / float(seq), '.16f'))
            out6 = str(format(retot / float(seq), '.16f'))
            out7 = str(format(dec2tot / float(seq), '.16f'))
            f.write(out0 + '  ' + out1 + ' ' + out2 + ' ' + out3 + ' ' + out4 + ' ' + out5 + ' ' + out6 + ' ' + out7)
            f.write('\n')


if __name__ == "__main__":
    main()
