import hashlib
import os
from Crypto.Cipher import AES


def encrypt(inputkey):
    global keyenc
    input_file = '/home/apollo/xuehuan/charm/avcharm/doc/dog.png'
    input_dir = os.path.dirname(input_file)

    hash = hashlib.sha256(bytes(inputkey, 'utf-8'))
    keyenc = hash.digest()
    iv = hash.digest().ljust(16)[:16]

    input_file = open(input_file, 'rb')
    input_data = input_file.read()
    input_file.close()
    enc_image(input_data, keyenc, iv, input_dir)
    print("Enc ended successfully File Stored as: encrypted.enc")


def decrypt(outputkey):
    output_file = '/home/apollo/xuehuan/charm/avcharm/doc/encrypted.enc'
    output_dir = os.path.dirname(output_file)

    hash = hashlib.sha256(bytes(outputkey, 'utf-8'))
    keydec = hash.digest()
    iv = hash.digest().ljust(16)[:16]

    input_file = open(output_file, 'rb')
    input_data = input_file.read()
    input_file.close()
    if keyenc == keydec:
        print('Same key: keyenc: keydec', keyenc, keydec)
        dec_image(input_data, keydec, iv, output_dir)
        print('Decryption ended successfully File Stored as: output.png')
    else:
        print('\ndifferent key')
        print('Decryption failed')


def enc_image(input_data, key, iv, filepath):
    cfb_cipher = AES.new(key, AES.MODE_CFB, iv)
    enc_data = cfb_cipher.encrypt(input_data)
    enc_file = open(filepath + "/encrypted.enc", "wb")
    enc_file.write(enc_data)
    enc_file.close()


def dec_image(input_data, key, iv, filepath):
    cfb_decipher = AES.new(key, AES.MODE_CFB, iv)
    plain_data = cfb_decipher.decrypt(input_data)

    output_file = open(filepath + "/output.png", "wb")
    output_file.write(plain_data)
    output_file.close()


if __name__ == "__main__":
    encrypt('abcdfg123')
    decrypt('abcdfg123')
