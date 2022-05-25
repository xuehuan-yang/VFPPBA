# -*- coding: utf-8 -*-
"""
Policy-based Broadcast Access Authorization for Flexible Data Sharing in Clouds
https://ieeexplore.ieee.org/document/9431697
"""
import random

from charm.toolbox.pairinggroup import PairingGroup, ZR, G1, G2, GT, pair
from charm.toolbox.ABEncMultiAuth import ABEncMultiAuth
import time
import numpy as np
from charm.toolbox.hash_module import Hash
from charm.core.math.integer import integer, bitsize, int2Bytes, randomBits
from msp import MSP
import image


class MJ18(ABEncMultiAuth):
    def __init__(self, groupObj, verbose=False):
        ABEncMultiAuth.__init__(self)
        global group, ahnipe, util, alpha, H

        group = groupObj
        util = MSP(group, verbose=False)
        alpha = group.random(ZR)
        H = Hash(group)

    def setup_ibpre(self, n):
        start = time.time()
        alpha = group.random(ZR)
        g, w, u, h = group.random(G1), group.random(G1), group.random(G1), group.random(G1)
        miu, v = group.random(G2), group.random(G2)
        miu1 = miu ** alpha
        gN = gN_function(n, g, alpha)
        wN = gN_function(n, w, alpha)
        vN = gN_function(n, v, alpha)
        e_gu = pair(g, miu)

        pp = {'g': g, 'gN': gN, 'w': w, 'wN': wN, 'vN': vN, 'miu1': miu1, 'u': u, 'h': h, 'e_gu': e_gu, 'v': v}
        msk = {'miu': miu, 'alpha': alpha}

        end = time.time()
        rt = end - start
        return pp, msk, rt

    def keygen_ibpre(self, ID, msk):
        start = time.time()

        SKID = msk['miu'] * (1 / (alpha + (H.hashToZr(ID))))
        sk = {'SKID': SKID, 'ID': ID}

        end = time.time()
        rt = end - start
        return sk, rt

    def enc_ibpre(self, n, pp, msk):
        start = time.time()

        m = group.random(GT)
        s = group.random(ZR)
        s_test = s
        C0 = m * ((pp['e_gu']) ** s)
        C2 = pp['miu1'] ** (-s)
        C2prime = msk['miu'] ** (-s)

        IDn = []
        for i in range(n):
            IDn.append('hello' + str(i))

        LJn = []
        for i in range(n):
            LJn.append('world' + str(i))

        temp = 1
        temp2 = 1
        for i in range(n):
            temp = temp * (alpha + H.hashToZr(IDn[i]))
            temp2 = temp2 * ((alpha + H.hashToZr(IDn[i])) / (H.hashToZr(IDn[i])))

        C1 = pp['g'] ** (s * temp)
        C3 = pp['v'] ** (s * temp2)
        rn = random_array(n)

        C4n = []
        for i in range(n):
            C4n.append(pp['g'] ** (rn[i]))

        C5n = []
        for i in range(n):
            equ1 = ((pp['u'] ** (H.hashToZr(LJn[i]))) * pp['h']) ** rn[i]
            equ2 = pp['w'] * (-s * temp)
            C5n.append(equ1 * equ2)

        ct = {'C0': C0, 'C1': C1, 'C2': C2, "C3": C3, "C4n": C4n, 'C5n': C5n, 'IDn': IDn, 'LJn': LJn, 's_test': s_test,
              'C2prime': C2prime}

        end = time.time()
        rt = end - start
        return ct, m, rt

    def dec_ibpre(self, pp, ct, sk):
        start = time.time()

        S = ct['IDn']
        ID1 = sk['ID']

        Snew = []
        for i in range(len(S)):
            if ID1 == S[i]:
                test111 = 0
            if ID1 != S[i]:
                Snew.append(S[i])

        temp1, temp2 = temp_function(Snew, alpha)

        D = (pair(sk['SKID'], ct['C1']) * pair(pp['g'] ** (temp1 - temp2), ct['C2prime'])) ** (1 / temp2)
        rec_msg = ct['C0'] / D

        end = time.time()
        rt = end - start
        return rec_msg, rt

    def rkgen_ibpre(self, n, pp, ct, msk):
        start = time.time()
        sigma = group.random(ZR)

        inputGT = group.random(GT)
        sprime = group.random(ZR)
        d0 = (pp['g'] ** sigma) + FHash_function(pp, pp['e_gu'] ** sprime)
        # nprime = random.randint(0,9)

        tempn = n
        IDnprime = []
        for i in range(tempn):
            IDnprime.append('hello' + str(i + tempn))

        temp = 1
        temp2 = 1
        for i in range(n):
            temp = temp * (alpha + H.hashToZr(IDnprime[i]))
            temp2 = temp2 * ((alpha + H.hashToZr(IDnprime[i])) / (H.hashToZr(IDnprime[i])))

        d1 = pp['g'] ** (sprime * temp)
        d2 = pp['miu1'] ** (-sprime)
        d2prime = msk['miu'] ** (-sprime)

        DK = {'d0': d0, 'd1': d1, 'd2': d2, 'd2prime': d2prime, 'sigma': sigma, 'IDnprime': IDnprime}

        end = time.time()
        ct = end - start
        return DK, ct

    def reenc_ibpre(self, n, pp, ct, DK):
        start = time.time()

        IDn = ct['IDn']
        temp2 = 1
        for i in range(n):
            temp2 = temp2 * ((alpha + H.hashToZr(IDn[i])) / (H.hashToZr(IDn[i])))

        equ1 = pp['g'] ** (ct['s_test'] * temp2)
        equ2 = pair(pp['v'] ** DK['sigma'], equ1)
        equ3 = (pp['e_gu'] ** (-ct['s_test']))

        C3prime = ct['C0'] * equ2 * equ3
        C0prime = DK['d0']
        C1prime = DK['d1']
        C2prime = DK['d2']
        C2prime_s = DK['d2prime']
        C4prime = ct['C3']

        ctprime = {'C0prime': C0prime, 'C1prime': C1prime, 'C2prime': C2prime, 'C2prime_s': C2prime_s,
                   'C3prime': C3prime, 'C4prime': C4prime, 'IDnprime': DK['IDnprime']}

        end = time.time()
        rt = end - start
        return ctprime, rt

    def dec2_ibpre(self, n, pp, sk1, ct, ctprime):
        start = time.time()

        Sprime = ctprime['IDnprime']
        ID = sk1['ID']
        Snew = []
        for i in range(len(Sprime)):
            if ID == Sprime[i]:
                test111 = 0
            if ID != Sprime[i]:
                Snew.append(Sprime[i])

        temp1, temp2 = temp_function(Snew, alpha)
        equ1 = (pair(sk1['SKID'], ctprime['C1prime']) * pair(pp['g'] ** (temp1 - temp2), ctprime['C2prime_s'])) ** (
                    1 / temp2)

        # equ1_test = pp['e_gu'] ** (ct['s_test'])
        equ2 = FHash_function(pp, equ1)
        equ3 = ctprime['C0prime'] / equ2
        rec_msg2 = ctprime['C3prime'] / pair(equ3, ctprime['C4prime'])

        end = time.time()
        rt = end - start
        return rec_msg2, rt


def random_array(n):
    array = []
    for i in range(n):
        temp = group.random(ZR)
        array.append(temp)
    return array


def gN_function(n, g, alpha):
    res = []
    for i in range(n):
        res.append(g ** (alpha ** i))
    return res


def generate_random_str(length):
    random_str = ''
    base_str = 'helloworlddfafj23i4jri3jirj23idaf2485644f5551jeri23jeri23ji23'
    for i in range(length):
        random_str += base_str[random.randint(0, length - 1)]
    return random_str


def FHash_function(pp, inputGT):
    equ1 = H.hashToZn(inputGT)
    equ2 = H.hashToZr(equ1)
    res = pp['g'] ** equ2
    return res


def dec1(pp, ct, sk):
    nodes = util.prune(ct['policy'], sk['attr_list'])
    prodG = 1
    prodGT = 1

    for node in nodes:
        attr = node.getAttributeAndIndex()
        attr_stripped = util.strip_index(attr)
        prodG *= ct['C3'][attr]
        prodGT *= pair(sk['Kx'][attr_stripped], ct['C4'][attr])

    temp = (pair(prodG, sk['K2']) * prodGT) / (pair(sk['K1'], ct['C1']))
    rec_msg = int2Bytes(ct["C"] ^ (H.hashToZn(1 / temp)))
    return rec_msg


def temp_function(Snew, alpha):
    temp1 = 1
    temp2 = 1
    for i in range(len(Snew)):
        temp1 = temp1 * (alpha + H.hashToZr(Snew[i]))
        temp2 = temp2 * (H.hashToZr(Snew[i]))

    return temp1, temp2


def main():
    groupObj = PairingGroup('SS512')
    n_array = np.arange(5, 30, 5)
    output_txt = '../doc/15_ibpre.txt'
    ahnipe = MJ18(groupObj)

    with open(output_txt, 'w+', encoding='utf-8') as f:
        f.write(
            "Seq SetupAveTime       KeygenAveTime      EncAveTime         Dec1AVeTime        RekeygenAveTime    ReencAveTime       Dec2AveTime   " + '\n')

        for i in range(len(n_array)):
            seq = 5
            sttot, kgtot, enctot, dec1tot, rktot, retot, dec2tot = 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0
            for j in range(seq):
                n = n_array[i]
                ID1 = 'hello0'

                pp, msk, setuptime = ahnipe.setup_ibpre(n)
                sk, keygen1time = ahnipe.keygen_ibpre(ID1, msk)
                ct, m, enctime = ahnipe.enc_ibpre(n, pp, msk)
                rec_msg1, dec1time = ahnipe.dec_ibpre(pp, ct, sk)
                DK, rkgentime = ahnipe.rkgen_ibpre(n, pp, ct, msk)
                ID2 = DK['IDnprime'][1]
                sk1, keygen2time = ahnipe.keygen_ibpre(ID2, msk)
                ctprime, reenctime = ahnipe.reenc_ibpre(n, pp, ct, DK)
                rec_msg2, dec2time = ahnipe.dec2_ibpre(n, pp, sk1, ct, ctprime)

                print("\nn:      ", n)
                print("m:        ", m)
                print("rec_msg1: ", rec_msg1)
                print("rec_msg2: ", rec_msg2)

                m_inputkey = group.serialize(m).decode("utf-8")
                m_outputkey = group.serialize(rec_msg1).decode("utf-8")
                image.encrypt(m_inputkey)
                image.decrypt(m_outputkey)

                sttot, kgtot, enctot, dec1tot, rktot, retot, dec2tot = sttot + setuptime, kgtot + keygen1time + keygen2time, enctot + enctime, dec1tot + dec1time, rktot + rkgentime, retot + reenctime, dec2tot + dec2time

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
