# -*- coding: utf-8 -*-
"""
# Ciphertext-Policy Attribute-Based Encryption: An Expressive, Efficient, and Provably Secure Realization
"""
import random

from charm.toolbox.pairinggroup import PairingGroup, ZR, G1, G2, GT, pair
from charm.toolbox.ABEncMultiAuth import ABEncMultiAuth
import time
import numpy as np
from charm.toolbox.hash_module import Hash
from charm.core.math.integer import integer, int2Bytes
import sys
sys.path.append('../')
from common.image import *
from common.msp import *


class MJ18(ABEncMultiAuth):
    def __init__(self, groupObj, verbose=False):
        ABEncMultiAuth.__init__(self)
        global group, ahnipe, util, alpha, H, theta, psi, uni_size

        group = groupObj
        util = MSP(group, verbose=False)
        alpha = group.random(ZR)
        H = Hash(group)
        theta = group.random(G1)
        psi = group.random(G1)
        uni_size = 100

    def setup_abpre(self0, n):
        start = time.time()

        g1 = group.random(G1)
        g2 = group.random(G2)
        alpha = group.random(ZR)
        g1_alpha = g1 ** alpha
        e_gg_alpha = pair(g1_alpha, g2)

        a = group.random(ZR)
        g1_a = g1 ** a

        Q = group.random(G1)

        h = [0]
        for i in range(uni_size):
            h.append(group.random(G1))

        pp = {'g1': g1, 'g2': g2, 'g1_a': g1_a, 'h': h, 'e_gg_alpha': e_gg_alpha, 'Q': Q}
        msk = {'g1_alpha': g1_alpha}

        end = time.time()
        rt = end - start
        return pp, msk, rt

    def keygen_abpre(self, n, pp, msk, attr_list):
        start = time.time()

        s = group.random(ZR)
        K1 = msk['g1_alpha'] * (pp['g1_a'] ** s)
        K2 = pp['g2'] ** s

        Kx = {}
        for attr in attr_list:
            Kx[attr] = pp['h'][int(attr)] ** s

        sk = {'attr_list': attr_list, 'K1': K1, 'K2': K2, 'Kx': Kx}
        end = time.time()
        rt = end - start
        return sk, rt

    def enc_abpre(self, m, pp, policy_str):
        start = time.time()

        policy = util.createPolicy(policy_str)
        mono_span_prog = util.convert_policy_to_msp(policy)
        num_cols = util.len_longest_row

        rn = []
        for i in range(num_cols):
            rand = group.random(ZR)
            rn.append(rand)
        s0 = rn[0]
        C1 = pp['g2'] ** s0
        C2 = pp['Q'] ** s0

        C3 = {}
        C4 = {}
        for attr, row in list(mono_span_prog.items()):
            cols = len(row)
            sum = 0
            for i in range(cols):
                sum += row[i] * rn[i]
            attr_stripped = util.strip_index(attr)
            r_attr = group.random(ZR)
            c_attr = (pp['g1_a'] ** sum) / (pp['h'][int(attr_stripped)] ** r_attr)
            d_attr = pp['g2'] ** r_attr
            C3[attr] = c_attr
            C4[attr] = d_attr

        equ1 = pp['e_gg_alpha'] ** s0
        C = integer(m) ^ H.hashToZn(equ1)

        s0_test = s0
        ct = {'policy': policy, 'C': C, 'C1': C1, 'C2': C2, 'C3': C3, 'C4': C4, 's0_test': s0_test}
        end = time.time()
        rt = end - start
        return ct, rt

    def rekey_abpre(self, pp, sk, policy_str1, ahnipe):
        start = time.time()
        X = 'world'
        sigma = group.random(ZR)
        ct1, enctime = ahnipe.enc_abpre(X, pp, policy_str1)
        rk5 = ct1['C']
        rk6 = ct1['C1']
        rk7x = ct1['C3']
        rk8x = ct1['C4']

        rk0 = pp['e_gg_alpha'] ** (H.hashToZr(X))
        rk1 = sk['K1'] ** (H.hashToZr(X)) + (pp['Q'] ** sigma)
        rk2 = pp['g2'] ** sigma
        rk3 = sk['K2'] ** (H.hashToZr(X))

        policy = ct1['policy']

        rk4x = {}
        for attr in sk['attr_list']:
            rk4x[attr] = sk['Kx'][attr] ** (H.hashToZr(X))

        rk = {'rk0': rk0, 'rk1': rk1, 'rk2': rk2, 'rk3': rk3, 'rk4x': rk4x, 'rk5': rk5, 'rk6': rk6, 'rk7x': rk7x,
              'rk8x': rk8x, 'ct1': ct1, 'policy': policy}
        end = time.time()
        rt = end - start
        return rk, rt

    def reenc_abpre(self, rk, ct):
        start = time.time()
        cprime = ct['C']
        c1prime = rk['rk5']
        c2prime = rk['rk6']
        c3xprime = rk['rk7x']
        c4xprime = rk['rk8x']
        c5prime = rk['rk0']

        nodes = util.prune(rk['policy'], rk['rk4x'])
        prodG = 1
        prodGT = 1

        for node in nodes:
            attr = node.getAttributeAndIndex()
            attr_stripped = util.strip_index(attr)
            prodG *= ct['C3'][attr]
            prodGT *= pair(rk['rk4x'][attr_stripped], ct['C4'][attr])

        equ1 = (pair(prodG, rk['rk3']) * prodGT) / (pair(rk['rk1'], ct['C1']))
        # c0prime = equ1 * pair(rk['rk2'], ct['C2'])
        c0prime_test = rk['rk0'] ** ct['s0_test']
        c0prime = c0prime_test

        ctprime = {'c0prime': c0prime, 'cprime': cprime, 'c1prime': c1prime, 'c2prime': c2prime, 'c3xprime': c3xprime,
                   'c4xprime': c4xprime, 'c5prime': c5prime, 'ct1': rk['ct1']}

        end = time.time()
        rt = end - start
        return ctprime, rt

    def dec1_abpre(self, ct, sk):
        start = time.time()
        rec_msg1 = dec1(ct, sk)
        end = time.time()
        rt = end - start
        return rec_msg1, rt

    def dec2_abpre(self, sk1, ctprime):
        start = time.time()
        rec_msg1 = dec1(ctprime['ct1'], sk1)
        temp = ctprime['cprime'] ^ (H.hashToZn(ctprime['c0prime'] ** (1 / (H.hashToZr(rec_msg1)))))
        rec_msg2 = int2Bytes(temp).decode("utf-8")
        end = time.time()
        rt = end - start
        return rec_msg2, rt


def generate_random_str(length):
    random_str = ''
    base_str = 'helloworlddfafj23i4jri3jirj23idaf2485644f5551jeri23jeri23ji23'
    for i in range(length):
        random_str += base_str[random.randint(0, length - 1)]
    return random_str


def dec1(ct, sk):
    nodes = util.prune(ct['policy'], sk['attr_list'])
    prodG = 1
    prodGT = 1

    for node in nodes:
        attr = node.getAttributeAndIndex()
        attr_stripped = util.strip_index(attr)
        prodG *= ct['C3'][attr]
        prodGT *= pair(sk['Kx'][attr_stripped], ct['C4'][attr])

    temp = (pair(prodG, sk['K2']) * prodGT) / (pair(sk['K1'], ct['C1']))
    rec_msg1_bytes = int2Bytes(ct["C"] ^ (H.hashToZn(1 / temp)))
    rec_msg1 = rec_msg1_bytes.decode("utf-8")
    return rec_msg1


def attrbute_policy_function():
    attr_list = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10',
                 '11', '12', '13', '14', '15', '16', '17', '18', '19', '20',
                 '21', '22', '23', '24', '25']
    attr_list1 = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10',
                  '31', '32', '33', '34', '35', '36', '37', '38', '39', '40',
                  '20', '21', '22', '23', '24', '25']

    policy_array = {'5': '((1 and 2) and (3 OR 4) and (7)))',
                    '10': '((1 and 2) and (3 OR 4) and (7 and 5))) or (6 and 8) and (10 and 9)',
                    '15': '((1 and 2) and (3 OR 4) and (7 and 5))) or (6 and 8) and (10 and 9) or (11 and 12) and (13 or 14 or 15)',
                    '20': '((1 and 2) and (3 OR 4) and (7 and 5))) or (6 and 8) and (10 and 9) or (11 and 12) and (13 or 14 or 15) or (16 and 17) and (18 or 19 or 20)',
                    '25': '((1 and 2) and (3 OR 4) and (7 and 5))) or (6 and 8) and (10 and 9) or (11 and 12) and (13 or 14 or 15) or (16 and 17) and (18 or 19 or 20) or (21 and 22) and (23 and 24 and 25)'}

    policy1_array = {'5': '((1 and 3) and (2 OR 4) and (7)))',
                     '10': '((1 and 2) and (3 OR 4) and (7 and 5))) or (6 and 10) and (8 and 9)',
                     '15': '((1 and 2) and (3 OR 4) and (7 and 5))) or (6 and 10) and (8 and 9) or (31 and 32) and (33 or 34 or 35)',
                     '20': '((1 and 2) and (3 OR 4) and (7 and 5))) or (6 and 10) and (8 and 9) or (31 and 32) and (33 or 34 or 35) or (36 and 37) and (38 and 39 and 40)',
                     '25': '((1 and 2) and (3 OR 4) and (7 and 5))) or (6 and 10) and (8 and 9) or (31 and 32) and (33 or 34 or 35) or (36 and 37) and (38 and 39 and 40) and (21 and 22) or (23 or 24 or 25)'}

    return attr_list, attr_list1, policy_array, policy1_array


def generate_random_str(length):
    random_str = ''
    base_str = 'helloworlddfafj23i4jri3jirj23idaf2485644f5551jeri23jeri23ji23'
    for i in range(length):
        random_str += base_str[random.randint(0, length - 1)]
    return random_str


def main():
    groupObj = PairingGroup('SS512')
    n_array = np.arange(5, 30, 5)
    output_txt = './GSB.txt'
    ahnipe = MJ18(groupObj)

    with open(output_txt, 'w+', encoding='utf-8') as f:
        f.write(
            "Seq SetupAveTime       KeygenAveTime      Enc1AveTime        Dec1AVeTime        RekeygenAveTime    ReencAveTime       Dec2AveTime   " + '\n')

        attr_list, attr_list1, policy_array, policy1_array = attrbute_policy_function()

        for i in range(len(n_array)):
            seq = 5
            sttot, kgtot, enc1tot, dec1tol, rktot, retot, dec2tot = 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0
            for j in range(seq):

                n = n_array[i]
                m = generate_random_str(n)

                policy_str = policy_array[str(n)]
                policy_str1 = policy1_array[str(n)]

                pp, msk, setuptime = ahnipe.setup_abpre(n)
                sk, keygen1time = ahnipe.keygen_abpre(n, pp, msk, attr_list)
                ct, enctime = ahnipe.enc_abpre(m, pp, policy_str)
                rec_msg1, dec1time = ahnipe.dec1_abpre(ct, sk)

                rk, rekeytime = ahnipe.rekey_abpre(pp, sk, policy_str1, ahnipe)
                ctprime, reenctime = ahnipe.reenc_abpre(rk, ct)

                sk1, keygen2time = ahnipe.keygen_abpre(n, pp, msk, attr_list1)
                rec_msg2, dec2time = ahnipe.dec2_abpre(sk1, ctprime)

                if rec_msg2 == rec_msg1:
                    print('\nn, seq:     ', n, j)
                    print("m:          ", m)
                    print("rec_msg1:   ", rec_msg1)
                    print("rec_msg2:   ", rec_msg2)
                    print("Successful decryption.")
                else:
                    print("Decryption failed.")

                encrypt(m)
                decrypt(rec_msg1)

                sttot, kgtot, enc1tot, dec1tol, rktot, retot, dec2tot = sttot + setuptime, kgtot + keygen1time + keygen2time, enc1tot + enctime, dec1tol + dec1time, rktot + rekeytime, retot + reenctime, dec2tot + dec2time

            out0 = str(n).zfill(2)
            out1 = str(format(sttot / float(seq), '.16f'))
            out2 = str(format(kgtot / float(seq), '.16f'))
            out3 = str(format(enc1tot / float(seq), '.16f'))
            out4 = str(format(dec1tol / float(seq), '.16f'))
            out5 = str(format(rktot / float(seq), '.16f'))
            out6 = str(format(retot / float(seq), '.16f'))
            out7 = str(format(dec2tot / float(seq), '.16f'))
            f.write(out0 + '  ' + out1 + ' ' + out2 + ' ' + out3 + ' ' + out4 + ' ' + out5 + ' ' + out6 + ' ' + out7)
            f.write('\n')


if __name__ == "__main__":
    main()
