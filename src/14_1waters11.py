'''
:Authors:         Shashank Agrawal
:Date:            5/2016
# Ciphertext-Policy Attribute-Based Encryption: An Expressive, Efficient, and Provably Secure Realization
# https://eprint.iacr.org/2017/807.pdf
# https://github.com/sagrawal87/ABE/blob/master/ABE/waters11/__init__.py
'''

from charm.toolbox.pairinggroup import PairingGroup, GT
from ABE.ac17 import AC17CPABE
from ABE.waters11 import Waters11

def main():
    pairing_group = PairingGroup('SS512')

    cpabe = Waters11(pairing_group, 4)

    (pk, msk) = cpabe.setup()

    attr_list = ['1', '2', '3']
    key = cpabe.keygen(pk, msk, attr_list)

    msg = pairing_group.random(GT)
    # msg = "hello"
    print("msg:     ", msg)

    # generate a ciphertext
    # policy_str = '((ONE and THREE) and (TWO OR FOUR))'
    policy_str = '((1 and 3) and (2 OR 4))'
    ctxt = cpabe.encrypt(pk, msg, policy_str)

    # decryption
    rec_msg = cpabe.decrypt(pk, ctxt, key)
    print("rec_msg: ", rec_msg)
    if debug:
        if rec_msg == msg:
            print ("Successful decryption.")
        else:
            print ("Decryption failed.")


if __name__ == "__main__":
    debug = True
    main()
