"""
#  H: {0,1} -> G1       H(0) only use H(0)
# from charm.toolbox.hash_module import Hash
# H = Hash(group)
# H1: GT -> {0,1}^2l    H.hashToZn(equ1)
# H2: {0,1} -> Zp       H.hashToZr(psi)  eg. H2(psi)         z = group.hash((m, k), ZR)
"""
import random

from charm.toolbox.pairinggroup import PairingGroup, ZR, G1, G2, GT, pair
from charm.toolbox.ABEncMultiAuth import ABEncMultiAuth
import time
import numpy as np
from charm.toolbox.hash_module import Hash
from charm.core.math.integer import integer, int2Bytes
from sympy import *
import sys
sys.path.append('../')
from common.image import *
from common.msp import *


class MJ18(ABEncMultiAuth):
    def __init__(self, groupObj, verbose=False):
        ABEncMultiAuth.__init__(self)
        global group, g, u, h, gamma, beta, theta, p, mu, sigma, H, uby, ele1, psi, H2psi, t, H1

        group = groupObj
        g = group.random(G1)
        u = group.random(G2)
        h = group.random(G2)
        gamma = group.random(ZR)
        beta = group.random(ZR)
        theta = group.random(ZR)
        p = group.random(ZR)
        mu = group.random(ZR)
        sigma = group.random(ZR)
        H = Hash(group)
        uby = g_exp(u, beta * gamma)
        ele = group.random(ZR)
        ele1 = ele / ele
        psi = group.random(GT)
        H2psi = H.hashToZr(psi)
        t = group.random(ZR)

        inputGT = group.random(GT)
        H1 = H_function(h, inputGT)

    def setup_vfippre(self, n):
        start = time.time()

        alphan = random_array(n)
        g0 = g ** p
        g1 = g ** theta
        g2n = g_exp_n(g, alphan)
        u0 = u ** (beta * gamma)
        u1 = u ** theta
        u2n = g_exp_n(u, alphan)

        h0 = h
        h1 = h ** theta
        h2n = g_exp_n(h, alphan)
        eguby = pair(g, uby)
        pp = {'g0': g0, 'g1': g1, 'g2n': g2n, 'h0': h0, 'h1': h1, 'h2n': h2n, 'eguby': eguby}
        msk = {'uby': uby, 'u0': u0, 'u1': u1, 'u2n': u2n}

        end = time.time()
        rt = end - start
        return pp, msk, rt

    def register_vfippre(self, n, msk):
        start = time.time()
        sk, x, registertime1 = register_function(n, msk)
        sk1, x1, registertime2 = register_function(n, msk)

        end = time.time()
        rt = end - start
        return sk, sk1, x, x1, rt

    def enc_vfippre(self, n, x, rm, rk, pp):
        start = time.time()

        m = rm
        k = rk

        z = group.hash((m, k), ZR)
        c0m = integer(m) ^ H.hashToZn(pair(g, uby) ** z)
        c0k = integer(k) ^ H.hashToZn(pair(g, uby) ** z)
        c1 = g ** z

        g0 = pp['g0']
        g1 = pp['g1']
        g2n = pp['g2n']
        c2n = c2_function(n, g0, x, z, g2n)
        c3 = g1 ** z
        c = c_function(m, k)
        ct = {'c': c, 'c0m': c0m, 'c0k': c0k, 'c1': c1, 'c2n': c2n, 'c3': c3}

        end = time.time()
        rt = end - start
        return ct, m, k, rt

    def authorize_vfippre(self, n, x1, pp, sk, ct):
        start = time.time()

        wn = x1
        r1 = group.random(ZR)
        R1 = group.random(ZR)
        q = group.random(ZR)

        d0 = psi * (pair(g, u) ** (beta * gamma * t))
        d1 = g ** t
        g0 = pp['g0']
        g1 = pp['g1']
        g2n = pp['g2n']
        d2n = d2n_function(n, g0, wn, t, g2n)
        d3 = g1 ** t

        sk1 = sk['sk1']
        sk2 = sk['sk2']
        sk3 = sk['sk3']
        y = sk['y']
        h1 = pp['h1']
        h2n = pp['h2n']
        c2n = ct['c2n']
        d4 = (sk1 ** H2psi) * (h1 ** R1)
        d5 = ((sk2 ** H2psi) * (h ** r1)) ** q
        d6 = (sk3 ** H2psi) * (h ** R1)

        H = Hash_function(n)
        egubyt = pp['eguby'] ** t
        d7 = H_function(h, egubyt) / (g2nyn(n, h2n, y) ** r1)
        # inputarray = [1,2,3,4,5]
        # coeffs_value, coeffs_array = coeffs_function(len(inputarray), inputarray)
        d8n = d8_function(n, y, q)
        d9 = pair(g, h) ** (beta * gamma * H2psi)
        d10 = g2nyn(n, g2n, y) ** r1
        d11 = d11_function(n, c2n, y)
        d12 = (sk2 ** H2psi) * (h ** r1)
        atyw = {'d0': d0, 'd1': d1, 'd2n': d2n, 'd3': d3, 'd4': d4, 'd5': d5, 'd6': d6, 'd7': d7, 'd8n': d8n, 'd9': d9,
                'd10': d10, 'd11': d11, 'd12': d12}

        end = time.time()
        rt = end - start
        return atyw, rt

    def transform_vfippre(self, ct, atyw):
        start = time.time()

        c1 = ct['c1']
        c3 = ct['c3']
        d4 = atyw['d4']
        d6 = atyw['d6']

        C = ct['c']
        C0m = ct['c0m']
        C0k = ct['c0k']
        C1 = atyw['d1']
        C2n = atyw['d2n']
        C3 = atyw['d3']
        C4 = ct['c1']
        C5 = atyw['d7']
        C6 = atyw['d9']
        C7 = atyw['d0']
        C9 = atyw['d10']
        d11 = atyw['d11']
        d12 = atyw['d12']
        C8 = 1 / (pair(d11, d12)) * (1 / (pair(c3, d6))) * pair(c1, d4)
        ctxw = {'C': C, 'C0m': C0m, 'C0k': C0k, 'C1': C1, 'C2n': C2n, 'C3': C3, 'C4': C4, 'C5': C5, 'C6': C6, 'C7': C7,
                'C8': C8, 'C9': C9}

        end = time.time()
        rt = end - start
        return ctxw, rt

    def dec1_function(self, n, sk, ct):
        start = time.time()

        c0m = ct['c0m']
        c0k = ct['c0k']
        c1 = ct['c1']
        c2n = ct['c2n']
        c3 = ct['c3']
        sk1 = sk['sk1']
        sk2 = sk['sk2']
        sk3 = sk['sk3']
        y = sk['y']
        A = pair(c1, sk1) * (1 / pair(c3, sk3)) * (1 / pair(g2nyn(n, c2n, y), sk2))
        mnum = c0m ^ H.hashToZn(A)
        knum = c0k ^ H.hashToZn(A)

        c = ct['c']
        test = (sigma ** H.hashToZr(mnum)) * (mu ** H.hashToZr(knum))
        if (c / test == ele1):
            m = int2Bytes(mnum).decode("utf-8")
            k = int2Bytes(knum)

        end = time.time()
        rt = end - start
        return m, rt

    def dec2_function(self, n, sk1, ct, ctxw):
        start = time.time()

        C1 = ctxw['C1']
        C2n = ctxw['C2n']
        C3 = ctxw['C3']
        C4 = ctxw['C4']
        C5 = ctxw['C5']
        C7 = ctxw['C7']
        C8 = ctxw['C8']

        c0m = ct['c0m']
        c0k = ct['c0k']
        sk11 = sk1['sk1']
        sk21 = sk1['sk2']
        sk31 = sk1['sk3']
        y1 = sk1['y']

        A = pair(C1, sk11) * (1 / pair(C3, sk31)) * (1 / pair(g2nyn(n, C2n, y1), sk21))
        A1 = C8 * pair(H_function(h, A) / C5, C4)
        psi_output1 = C7 / A  # check psi value

        mnum = c0m ^ H.hashToZn(A1 ** (1 / H2psi))
        knum = c0k ^ H.hashToZn(A1 ** (1 / H2psi))

        m = int2Bytes(mnum)
        k = int2Bytes(knum)

        c = ct['c']
        test = (sigma ** H.hashToZr(mnum)) * (mu ** H.hashToZr(knum))
        if (c / test == ele1):
            m = int2Bytes(mnum).decode("utf-8")
            k = int2Bytes(knum)

        end = time.time()
        rt = end - start
        return m, k, rt


def testcase_generate(n):
    xi = np.random.randint(1, 10, size=n)
    xi[n - 1] = 1
    xV = random_perpendicular_vector(n, xi)
    xZ = random_perpendicular_vector(n, xi)

    check_perpendicular(n, xi, xV)
    check_perpendicular(n, xi, xZ)
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


def Hash_function(n):
    res = [0 for i in range(n)]
    for i in range(n):
        res[i] = u ** 1
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
    array = []
    val = g1Val ** arrayInput
    array.append(val)
    return array[0]


def random_array(n):
    array = []
    for i in range(n):
        a = group.random(ZR)
        array.append(a)
    return array


def c_function(m, k):
    equ1 = H.hashToZr(m)
    equ2 = H.hashToZr(k)
    res = (sigma ** equ1) * (mu ** equ2)
    return res


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


def g2nyn(n, g2n, y):
    temp = 1
    for i in range(n):
        temp = temp * g_exp(g2n[i], y[i] * ele1)
    return temp


def d11_function(n, c2n, y):
    temp = 1
    for i in range(n):
        temp = temp * (c2n[i] ** (y[i] * ele1))
    return temp


def d8_function(n, y, q):
    res = [0 for i in range(n)]
    for i in range(n):
        res[i] = y[i] / q
    return res


def H_function(h, inputGT):
    equ1 = H.hashToZn(inputGT)
    equ2 = H.hashToZr(equ1)
    res = h ** equ2
    return res


def register_function(n, msk):
    start = time.time()

    r = group.random(ZR)
    R = group.random(ZR)
    y, x, y2 = testcase_generate(n)

    u2n = msk['u2n']
    u0 = msk['u0']
    u1 = msk['u1']
    sk1 = sk1_function(n, u0, u2n, y, r, u1, R)
    sk = {'sk1': sk1, 'sk2': u ** r, 'sk3': u ** R, 'y': y}

    end = time.time()
    rt = format(end - start, '.16f')
    return sk, x, rt


def generate_random_str(length):
    random_str = ''
    base_str = 'helloworlddfafj23i4jri3jirj23idaf2485644f5551jeri23jeri23ji23'
    for i in range(length):
        random_str += base_str[random.randint(0, length - 1)]
    return random_str


def coeffs_function(n, inputarray):
    x = symbols('x')
    res = 1
    xn = []
    for i in range(n):
        xn.append(symbols(str(str(x) + str(i + 1))))
        res = Mul(res, x + xn[i])

    p = Poly(res, x)
    coeffs_array = p.coeffs()
    coeffs_value = []
    for i in range(n + 1):
        res = coeffs_array[i].subs(
            [(xn[0], inputarray[0]), (xn[1], inputarray[1]), (xn[2], inputarray[2]), (xn[3], inputarray[3]),
             (xn[4], inputarray[4])])
        coeffs_value.append(res)
    return coeffs_value, coeffs_array


def main():
    groupObj = PairingGroup('SS512')
    n_array = np.arange(5, 30, 5)
    output_txt = './VFPPBA.txt'

    with open(output_txt, 'w+', encoding='utf-8') as f:
        f.write(
            "Seq SetupAveTime       RegisterAveTime    EncAveTime         Dec1AveTime        AuthorizeAveTime   TransformAveTime   Dec2AveTime   " + '\n')

        for i in range(len(n_array)):
            ahnipe = MJ18(groupObj)
            seq = 5
            sttot, retot, enctot, dec1tot, autot, trtot, dec2tot = 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0
            for j in range(seq):
                n = n_array[i]
                rm = generate_random_str(n)
                rk = generate_random_str(n)
                pp, msk, setuptime = ahnipe.setup_vfippre(n)
                sk, sk1, x, x1, registertime = ahnipe.register_vfippre(n, msk)
                ct, m, k, enctime = ahnipe.enc_vfippre(n, x, rm, rk, pp)
                atyw, authorizetime = ahnipe.authorize_vfippre(n, x1, pp, sk, ct)
                ctxw, transformtime = ahnipe.transform_vfippre(ct, atyw)

                M_output_1, dec1time = ahnipe.dec1_function(n, sk, ct)
                M_output_2, k, dec2time = ahnipe.dec2_function(n, sk1, ct, ctxw)

                print("\nn, seq ", n, j)
                print("M_input:    ", m)
                print("M_output_1: ", M_output_1)
                print("M_output_2: ", M_output_2)
                encrypt(m)
                decrypt(M_output_1)

                sttot, retot, enctot, dec1tot, autot, trtot, dec2tot = sttot + setuptime, retot + registertime, enctot + enctime, dec1tot + dec1time, autot + authorizetime, trtot + transformtime, dec2tot + dec2time
                print("sttot:", sttot)

            out0 = str(n).zfill(2)
            out1 = str(format(sttot / float(seq), '.16f'))
            out2 = str(format(retot / float(seq), '.16f'))
            out3 = str(format(enctot / float(seq), '.16f'))
            out4 = str(format(dec1tot / float(seq), '.16f'))
            out5 = str(format(autot / float(seq), '.16f'))
            out6 = str(format(trtot / float(seq), '.16f'))
            out7 = str(format(dec2tot / float(seq), '.16f'))
            f.write(out0 + '  ' + out1 + ' ' + out2 + ' ' + out3 + ' ' + out4 + ' ' + out5 + ' ' + out6 + ' ' + out7)
            f.write('\n')


if __name__ == "__main__":
    main()
