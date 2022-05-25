'''
:Authors:         Shashank Agrawal
:Date:            5/2016
# FAME: Fast Attribute-based Message Encryption
# https://eprint.iacr.org/2017/807.pdf
# https://github.com/sagrawal87/ABE/blob/master/ABE/ac17/__init__.py
'''

from charm.toolbox.pairinggroup import PairingGroup, GT
from ABE.ac17 import AC17CPABE


def main():
    # instantiate a bilinear pairing map
    pairing_group = PairingGroup('SS512')

    # AC17 CP-ABE under DLIN (2-linear)
    cpabe = AC17CPABE(pairing_group, 2)

    # run the set up
    (pk, msk) = cpabe.setup()

    # generate a key
    attr_list = ['ONE', 'TWO', 'THREE']
    key = cpabe.keygen(pk, msk, attr_list)

    # choose a random message
    msg = pairing_group.random(GT)
    print("msg:     ", msg)

    # generate a ciphertext
    policy_str = '((ONE and THREE) and (TWO OR FOUR))'
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
