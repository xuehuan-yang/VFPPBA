from charm.toolbox.pairinggroup import PairingGroup, ZR, G1, G2, GT, pair
from charm.toolbox.ABEncMultiAuth import ABEncMultiAuth
import time
import numpy as np
from charm.toolbox.hash_module import Hash
import sys
sys.path.append('../')
from common.image import *
from common.msp import *


class MJ18(ABEncMultiAuth):
    def __init__(self, groupObj, verbose=False):
        ABEncMultiAuth.__init__(self)
        global group, g, u, h, gamma, beta, theta, p, ele1, H

        group = groupObj
        g = group.random(G1)
        u = group.random(G2)
        h = group.random(G2)
        gamma = group.random(ZR)
        beta = group.random(ZR)
        theta = group.random(ZR)
        p = group.random(ZR)
        ele = group.random(ZR)
        ele1 = ele / ele
        H = Hash(group)

    def setup_ibbpre(self, n):
        start = time.time()
        alphan = random_array(n)

        g0 = g_exp(g, p)
        g1 = g_exp(g, theta)
        g2n = g_exp_n(g, alphan)

        u0 = g_exp(u, beta * gamma)
        u1 = g_exp(u, theta)
        u2n = g_exp_n(u, alphan)

        h0 = h
        h1 = g_exp(h, theta)
        h2n = g_exp_n(h, alphan)
        inputGT = group.random(GT)
        H = H_function(h, inputGT)

        uby = g_exp(u, beta * gamma)
        eguby = pair(g, uby)
        pp = {'g0': g0, 'g1': g1, 'g2n': g2n, 'h0': h0, 'h1': h1, 'h2n': h2n, 'H': H, 'eguby': eguby}
        msk = {'uby': uby, 'u0': u0, 'u1': u1, 'u2n': u2n}

        end = time.time()
        rt = end - start
        return pp, msk, rt

    def register_ibbpre(self, n, msk):
        start = time.time()

        r = group.random(ZR)
        R = group.random(ZR)
        y, x, y2 = testcase_generate(n)

        u2n = msk['u2n']
        u0 = msk['u0']
        u1 = msk['u1']
        sk1 = sk1_function(n, u0, u2n, y, r, u1, R)
        sk2 = g_exp(u, r)
        sk3 = g_exp(u, R)
        sk = {'sk1': sk1, 'sk2': sk2, 'sk3': sk3, 'y': y}

        end = time.time()
        rt = end - start
        return sk, x, rt

    def enc_ibbpre(self, n, x, pp, msk):
        start = time.time()

        z = group.random(ZR)
        M = group.random(GT)

        u0 = msk['u0']
        c0 = M * g_exp(pair(g, u0), z)
        c1 = g_exp(g, z)

        g0 = pp['g0']
        g1 = pp['g1']
        g2n = pp['g2n']

        c2n = c2_function(n, g0, x, z, g2n)
        c3 = g_exp(g1, z)
        c4 = g_exp(g0, z)
        ct = {'c0': c0, 'c1': c1, 'c2n': c2n, 'c3': c3, 'c4': c4}

        end = time.time()
        rt = end - start
        return ct, M, rt

    def authorize_ibbpre(self, n, pp, msk, sk, x1):
        start = time.time()

        wn = x1
        t = group.random(ZR)
        r1 = group.random(ZR)
        R1 = group.random(ZR)
        q = group.random(ZR)

        g0 = pp['g0']
        g1 = pp['g1']
        g2n = pp['g2n']

        d1 = g_exp(g, t)
        d2n = d2n_function(n, g0, wn, t, g2n)
        d3 = g_exp(g1, t)
        sk1 = sk['sk1']
        sk2 = sk['sk2']
        sk3 = sk['sk3']
        y = sk['y']
        h1 = pp['h1']
        h2n = pp['h2n']

        d4 = sk1 * g_exp(h1, R1)
        d5 = g_exp(sk2 * g_exp(h, r1), q)

        d6 = sk3 * g_exp(h, R1)
        d7 = d7_function(n, t, h2n, y, r1, pp)

        d8n = d8_function(n, y, q)
        d9 = sk2 * g_exp(h, r1)
        atyw = {'d1': d1, 'd2n': d2n, 'd3': d3, 'd4': d4, 'd5': d5, 'd6': d6, 'd7': d7, 'd8n': d8n, 'd9': d9}

        end = time.time()
        rt = end - start
        return atyw, rt

    def transform_ibbpre(self, n, ct, atyw, sk):
        start = time.time()

        c0 = ct['c0']
        c1 = ct['c1']
        c2n = ct['c2n']
        c3 = ct['c3']

        d4 = atyw['d4']
        d5 = atyw['d5']
        d6 = atyw['d6']
        d8n = atyw['d8n']

        C1 = atyw['d1']
        C2n = atyw['d2n']
        C3 = atyw['d3']

        C4 = ct['c1']
        C5 = atyw['d7']
        y = sk['y']
        d9 = atyw['d9']

        C6 = C6_function(n, c0, c2n, d8n, d5, c3, d6, c1, d4, d9, y)
        ctxw = {'C1': C1, 'C2n': C2n, 'C3': C3, 'C4': C4, 'C5': C5, 'C6': C6}

        end = time.time()
        rt = end - start
        return ctxw, rt

    def dec1_ibbpre(self, n, sk, ct):
        start = time.time()

        c0 = ct['c0']
        c1 = ct['c1']
        c2n = ct['c2n']
        c3 = ct['c3']
        sk1 = sk['sk1']
        sk2 = sk['sk2']
        sk3 = sk['sk3']
        y = sk['y']

        temp = 1
        for i in range(n):
            temp = temp * g_exp(c2n[i], y[i] * ele1)
        M_output_1 = c0 * pair(c3, sk3) * pair(temp, sk2) / (pair(c1, sk1))

        end = time.time()
        rt = end - start
        return M_output_1, rt

    def dec2_ibbpre(self, n, pp, sk1, ctxw):
        start = time.time()

        C4 = ctxw['C4']
        C5 = ctxw['C5']
        C6 = ctxw['C6']
        H = pp['H']

        sk11 = sk1['sk1']
        sk21 = sk1['sk2']
        sk31 = sk1['sk3']
        C1 = ctxw['C1']
        C2n = ctxw['C2n']
        C3 = ctxw['C3']
        y1 = sk1['y']

        temp = 1
        for i in range(n):
            temp = temp * g_exp(C2n[i], y1[i] * ele1)
        A = pair(C1, sk11) / (pair(C3, sk31) * pair(temp, sk21))

        A1 = pair(C5 / H_function(h, A), C4)
        M_output_2 = C6 * A1

        end = time.time()
        rt = end - start
        return M_output_2, rt


def testcase_generate(n):
    xi = np.random.randint(1, 10, size=n)
    xi[n - 1] = 1
    xV = random_perpendicular_vector(n, xi)
    xZ = random_perpendicular_vector(n, xi)

    VX1 = check_perpendicular(n, xi, xV)
    VX2 = check_perpendicular(n, xi, xZ)
    return xi, xV, xZ


def random_perpendicular_vector(n, vec):
    res = np.random.randint(1, 10, size=n)
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


def H_function(h, inputGT):
    equ1 = H.hashToZn(inputGT)
    equ2 = H.hashToZr(equ1)
    res = h ** equ2
    return res


def sk1_function(n, u0, u2n, y, r, u1, R):
    temp = 1
    for i in range(n):
        equ1 = g_exp(u2n[i], y[i] * r)
        temp = temp * equ1
    sk1 = u0 * g_exp(u1, R) * temp
    return sk1


def g_exp_n(g1Val, arrayInput):
    array = []
    for i in range(len(arrayInput)):
        val = g1Val ** arrayInput[i]
        array.append(val)
    return array


def g_exp(g1Val, arrayInput):
    val = g1Val ** arrayInput
    return val


def random_array(n):
    array = []
    for i in range(n):
        a = group.random(ZR)
        array.append(a)
    return array


def c2_function(n, g0, x, z, g2n):
    res = [0 for i in range(n)]
    for i in range(n):
        equ1 = g_exp(g0, x[i] * z)
        equ2 = g_exp(g2n[i], z)
        res[i] = equ1 * equ2
    return res


def d2n_function(n, g0, wn, t, g2n):
    res = [0 for i in range(n)]
    for i in range(n):
        equ1 = g_exp(g0, wn[i] * t)
        equ2 = g_exp(g2n[i], t)
        res[i] = equ1 * equ2
    return res


def d7_function(n, t, h2n, y, r1, pp):
    egubyt = pp['eguby'] ** t
    temp = 1
    for i in range(n):
        temp = temp * g_exp(h2n[i], y[i] * r1)
    res = H_function(h, egubyt) / temp
    return res


def d8_function(n, y, q):
    res = [0 for i in range(n)]

    for i in range(n):
        res[i] = y[i] / (q * ele1)
    return res


def C6_function(n, c0, c2n, d8n, d5, c3, d6, c1, d4, d9, y):
    # temp = 1
    # for i in range(n):
    #     temp = temp * g_exp(c2n[i], d8n[i])
    # res = c0 * pair(temp, d5) * pair(c3, d6) / pair(c1, d4)
    temp = 1
    for i in range(n):
        temp = temp * g_exp(c2n[i], y[i] * ele1)
    res = c0 * pair(temp, d9) * pair(c3, d6) / pair(c1, d4)
    return res


def main():
    groupObj = PairingGroup('SS512')
    n_array = np.arange(5, 30, 5)
    output_txt = './PPMRBPRE.txt'

    with open(output_txt, 'w+', encoding='utf-8') as f:
        f.write(
            "Seq SetupAveTime       RegisterAveTime    EncAveTime         Dec1AVeTime        AuthorizeAveTime   TransformAveTime   Dec2AveTime   " + '\n')
        for i in range(len(n_array)):
            seq = 5
            sttot, rgtot, enctot, dec1tot, autot, trtot, dec2tot = 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0
            for j in range(seq):
                ahnipe = MJ18(groupObj)
                n = n_array[i]
                pp, msk, setuptime = ahnipe.setup_ibbpre(n)
                sk, x, registertime = ahnipe.register_ibbpre(n, msk)
                sk1, x1, register1time = ahnipe.register_ibbpre(n, msk)
                ct, M, enctime = ahnipe.enc_ibbpre(n, x, pp, msk)
                atyw, authorizetime = ahnipe.authorize_ibbpre(n, pp, msk, sk, x1)
                ctxw, transformtime = ahnipe.transform_ibbpre(n, ct, atyw, sk)
                M_output_1, dec1time = ahnipe.dec1_ibbpre(n, sk, ct)
                M_output_2, dec2time = ahnipe.dec2_ibbpre(n, pp, sk1, ctxw)

                print("\nn, seq:    ", n, j)
                print("M_input:     ", M)
                print("M_output_1:  ", M_output_1)
                print("M_output_2:  ", M_output_2)
                m_inputkey = group.serialize(M).decode("utf-8")
                m_outputkey = group.serialize(M_output_1).decode("utf-8")
                encrypt(m_inputkey)
                decrypt(m_outputkey)

                sttot, rgtot, enctot, dec1tot, autot, trtot, dec2tot = sttot + setuptime, rgtot + registertime + register1time, enctot + enctime, dec1tot + dec1time, autot + authorizetime, trtot + transformtime, dec2tot + dec2time

            out0 = str(n).zfill(2)
            out1 = str(format(sttot / float(seq), '.16f'))
            out2 = str(format(rgtot / float(seq), '.16f'))
            out3 = str(format(enctot / float(seq), '.16f'))
            out4 = str(format(dec1tot / float(seq), '.16f'))
            out5 = str(format(autot / float(seq), '.16f'))
            out6 = str(format(trtot / float(seq), '.16f'))
            out7 = str(format(dec2tot / float(seq), '.16f'))
            f.write(out0 + '  ' + out1 + ' ' + out2 + ' ' + out3 + ' ' + out4 + ' ' + out5 + ' ' + out6 + ' ' + out7)
            f.write('\n')


if __name__ == "__main__":
    main()
