# Secure Data Sharing With Flexible Cross-Domain Authorization in Autonomous Vehicle Systems

from charm.toolbox.pairinggroup import ZR, G1, pair
from charm.toolbox.hash_module import Hash
import pickle
import base64
import time
import sys

sys.path.append('../')
from common.parse import *

class PDSMFC():
    def __init__(self, groupObj=None):
        if groupObj is None:
            from charm.toolbox.pairinggroup import PairingGroup
            groupObj = PairingGroup('SS512', secparam=512)
        global group, H, r1
        group = groupObj
        mask = 'ed27dbfb02752e0e16bc4502d6c732bc5f1cc92ba19b2d93a4e95c597ca42753e93550b52f82b6c13fb8cc0c2fc64487'
        H = Hash(group)
        self._mask = bytes.fromhex(mask)

    def setup(self, n):
        start = time.time()
        r, s, P = group.random(ZR), group.random(ZR), group.random(G1)
        g, v, u, P, Q = group.random(G1), group.random(G1), group.random(G1), group.random(G1), group.random(G1)
        x, y, theta = group.random(ZR), group.random(ZR), group.random(ZR)

        P0 = P * x
        g1 = g * theta
        v_theta = v * theta
        Q0 = Q * y
        egu = pair(g, u)

        u_thetan = []
        for i in range(n):
            u_thetan.append(u * theta)

        pp = {'g1': g1, 'u': u, 'v': v, 'v_theta': v_theta, 'u_thetan': u_thetan, 'P': P, 'P0': P0, 'Q': Q, 'Q0': Q0,
              'egu': egu}
        msk = {'g': g, 'theta': theta, 'x': x, 'y': y}

        end = time.time()
        rt = format(end - start, '.16f')
        return pp, msk, rt

    def H(self, X):
        return group.hash(X, G1)

    def H_prime(self, X):
        # Both H and H' are computed from the same method group.hash()
        # In order to make them different, we apply a fixed mask to the
        # inputs of H'
        X = bytes([a ^ b for (a, b) in zip(X.encode(), self._mask)])
        return group.hash(X, G1)

    def skgen(self, msk, id2):
        h2id2 = H.hashToZr(id2)
        sk0 = msk['g'] * (1 / (msk['theta'] + h2id2))
        sk1 = group.hash(id2, G1) * msk['x']
        sk2 = group.hash(id2, G1) * msk['y']
        sk3 = group.hash(id2, G1)
        sk = {'sk0': sk0, 'sk1': sk1, 'sk2': sk2, 'sk3': sk3}
        return sk

    def ekgen(self, msk, id1):
        ek = msk['y'] * self.H_prime(id1)
        return ek

    def skgen_function(self, msk, id1, id2, id3, id4, id5):
        start = time.time()
        ek = ME.ekgen(msk, id1)
        sk = ME.skgen(msk, id2)
        sk56 = ME.skgen(msk, id3)
        sk78 = ME.skgen(msk, id4)
        sk910 = ME.skgen(msk, id5)

        end = time.time()
        rt = format(end - start, '.16f')
        return ek, sk, sk56, sk78, sk910, rt

    def rkgen(self, sk, R):
        (r, s) = sk
        H_R = self.H(R)
        dk1 = r * H_R
        dk2 = s * H_R
        dk3 = H_R
        dk = (dk1, dk2, dk3)
        return dk

    def encrypt(self, pp, msk, R, ek, M):
        start = time.time()
        r0 = group.random(ZR)
        r1 = group.random(ZR)

        R0 = pp["P"] * r0
        R1 = pp["P"] * r1

        H_R2 = self.H(id2)
        k_R = pair(H_R2, pp['P0'] * r1)
        k_S = pair(H_R2, R0 + ek)
        egur1 = pp['egu'] * r1
        enc_egur1 = group.serialize(egur1)[2:-1]

        enc_k_R = group.serialize(k_R)[2:-1]
        enc_k_S = group.serialize(k_S)[2:-1]
        c0 = bytes([a ^ b ^ c ^ d for (a, b, c, d) in zip(M, enc_egur1, enc_k_R, enc_k_S)])
        c1 = pp['u_thetan'][0] * r1 + (pp['u'] ** (r1 * H.hashToZr(id2)))
        c2 = pp['v_theta'] * r1 + (pp['v'] ** (r1 * H.hashToZr(id2)))
        # test c1 = c3 ; c2 = c4
        # c3 = pp['u'] * (r1 * (msk['theta'] + H.hashToZr(id2)))
        # c4 = pp['v'] * (r1 * (msk['theta'] + H.hashToZr(id2)))
        ct = {'c0': c0, 'c1': c1, 'c2': c2, 'R1': R1, 'R0': R0, 'r1': r1}

        end = time.time()
        rt = format(end - start, '.16f')
        return ct, rt

    def decrypt(self, ct, sk, pp, ct_prime, sk56):
        start = time.time()

        M_output_1 = ME.decrypt_orignial(ct, sk)
        M_output_2 = ME.decrpt_second_level(pp, ct, ct_prime, sk56)

        end = time.time()
        rt = format(end - start, '.16f')
        return M_output_1, M_output_2, rt

    def decrypt_orignial(self, ct, sk):
        k_R = pair(sk['sk1'], ct['R1'])
        k_S = pair(sk['sk2'], self.H_prime(id1)) * pair(sk['sk3'], ct['R0'])

        egur1 = pair(sk['sk0'], ct['c1'])
        enc_egur1 = group.serialize(egur1)[2:-1]

        enc_k_R = group.serialize(k_R)[2:-1]
        enc_k_S = group.serialize(k_S)[2:-1]
        temp = [a ^ b ^ c ^ d for (a, b, c, d) in zip(ct['c0'], enc_egur1, enc_k_R, enc_k_S)]
        M = bytes(temp)
        return M

    def authorize(self, pp, sk, sk56, msk, id3, id4):
        start = time.time()
        s, t = group.random(ZR), group.random(ZR)
        u = pp['u']
        u0 = pp['u_thetan'][0]
        u1 = pp['u_thetan'][0]
        u2 = pp['u_thetan'][1]
        u3 = pp['u_thetan'][2]

        Hid3 = H.hashToZr(id3)
        Hid4 = H.hashToZr(id4)
        s1 = pp['g1'] * (-s)

        temp_s2 = (u2 + u1 * (Hid3 + Hid4) + u * (Hid3 * Hid4)) * s
        s2 = temp_s2 * (1 / (msk['theta'] + Hid3))

        # todo
        test_s2 = (u3 + u2 * (Hid3 + Hid4) + u1 * (Hid3 * Hid4) + (u2 * Hid3) + (
                u1 * (Hid3 + Hid4) * Hid3) + u0 * (Hid3 * Hid4 * Hid3)) * s

        s3 = group.hash(pp['egu'] * s, G1) + (u * t)
        s4 = sk['sk0'] + (pp['v'] * (-t))
        s5 = sk['sk1']
        s6 = sk['sk2']
        s7 = sk['sk3']

        at = {'s1': s1, 's2': s2, 's3': s3, 's4': s4, 's5': s5, 's6': s6, 's7': s7, 's': s}
        end = time.time()
        rt = format(end - start, '.16f')
        return at, rt

    def transform(self, pp, at, ct):
        start = time.time()
        k_R = pair(at['s5'], ct['R1'])
        k_S = pair(at['s6'], self.H_prime(id1)) * pair(at['s7'], ct['R0'])
        enc_k_R = group.serialize(k_R)[2:-1]
        enc_k_S = group.serialize(k_S)[2:-1]

        c0_prime = bytes([a ^ b ^ c for (a, b, c) in zip(ct['c0'], enc_k_R, enc_k_S)])
        c1_prime = at['s1']
        c2_prime = at['s2']
        c3_prime = at['s3']
        c4_prime = ct['c2']
        c5_prime = pair(ct['c1'], at['s4'])

        ct_prime = {'c0_prime': c0_prime, "c1_prime": c1_prime, "c2_prime": c2_prime, "c3_prime": c3_prime,
                    "c4_prime": c4_prime, "c5_prime": c5_prime}

        end = time.time()
        rt = format(end - start, '.16f')
        return ct_prime, rt

    def decrpt_second_level(self, pp, ct, ct_prime, sk56):
        equ1 = pp['u_thetan'][0] + (pp['u'] * (H.hashToZr(id3) * H.hashToZr(id4)))
        equ2 = pair(equ1, ct_prime['c1_prime'])
        equ3 = pair(sk56['sk0'], ct_prime['c2_prime'])
        euq4 = equ2 * equ3
        equ5 = euq4 * (1 / (H.hashToZr(id3) * H.hashToZr(id4)))
        equ5_test = pp['egu'] * at['s']

        A1 = pp['egu'] * (at['s'] * H.hashToZr(id3) * H.hashToZr(id4))
        A = A1 * (1 / (H.hashToZr(id3) * H.hashToZr(id4)))
        testA = pp['egu'] * (at['s'])

        B = ct_prime['c3_prime'] / (group.hash(A, G1))
        # testB = pp['u'] * (at['t'])

        C = pair(B, ct_prime['c4_prime']) * ct_prime['c5_prime']
        # testC = pp['egu'] * (ct['r1'])

        temp = group.serialize(C)[2:-1]
        msg2 = bytes([a ^ b for (a, b) in zip(ct_prime['c0_prime'], temp)])
        return msg2


if __name__ == "__main__":
    from charm.toolbox.pairinggroup import PairingGroup

    group = PairingGroup('SS512', secparam=512)
    ME = PDSMFC(group)
    n = 30
    R = 'attribute 1, attribute 2'
    S = 'attribute 3, attribute 4'
    T = 'attribute 5, attribute 6'
    W = 'attribute 7, attribute 8'

    id1 = S
    id2 = R
    id3 = T
    id4 = W
    id5 = 'attribute 9, attribute 10'
    pp, msk, setuptime = ME.setup(n)
    ek, sk, sk56, sk78, sk910, skgentime = ME.skgen_function(msk, id1, id2, id3, id4, id5)

    M = b"helloworld"
    ct, enctime = ME.encrypt(pp, msk, R, ek, M)

    msg1 = ME.decrypt_orignial(ct, sk)
    S2 = 'attribute 6'
    msg1_prime = ME.decrypt_orignial(ct, sk56)

    at, authorizetime = ME.authorize(pp, sk, sk56, msk, id3, id4)
    ct_prime, transformtime = ME.transform(pp, at, ct)
    msg2 = ME.decrpt_second_level(pp, ct, ct_prime, sk56)
    output_txt= output_func('21_pdsmfc')


    with open(output_txt, 'w+', encoding='utf-8') as f:
        f.write("Seq SetupTime          EncTime            KeyGenTime         DecTime  " + '\n')
        setupTotal, enctimeTotal, authorizetransformTotal, dectimeTotal = 0.0, 0.0, 0.0, 0.0
        for i in range(n):
            pp, msk, setuptime = ME.setup(n)
            ek, sk, sk56, sk78, sk910, skgentime = ME.skgen_function(msk, id1, id2, id3, id4, id5)

            M = b"helloworld"
            ct, enctime = ME.encrypt(pp, msk, R, ek, M)
            at, authorizetime = ME.authorize(pp, sk, sk56, msk, id3, id4)
            ct_prime, transformtime = ME.transform(pp, at, ct)

            M_output_1, M_output_2, dectime = ME.decrypt(ct, sk, pp, ct_prime, sk56)

            M_output_1 = ME.decrypt_orignial(ct, sk)
            M_output_2 = ME.decrpt_second_level(pp, ct, ct_prime, sk56)

            print("\nlength:     ", i)
            print("M_input:    ", M)
            print("M_output_1: ", M_output_1)
            print("M_output_2: ", M_output_2)
            setupTotal = setupTotal + float(setuptime)
            enctimeTotal = enctimeTotal + float(enctime)
            temp = float(authorizetime) + float(transformtime)
            authorizetransformTotal = authorizetransformTotal + temp
            dectimeTotal = dectimeTotal + float(dectime)

            f.write(str(i).zfill(2) + "  " + str(setuptime) + " " + str(enctime) + " " + str(format(temp, '.16f')) + " " + str(dectime))
            f.write('\n')
        f.write(str(n).zfill(2) + "  " + str(format(setupTotal / n, '.16f')) + " " + str(
            format(enctimeTotal / n, '.16f')) + " " + str(format(authorizetransformTotal / n, '.16f')) + " " + str(
            format(dectimeTotal / n, '.16f')))
