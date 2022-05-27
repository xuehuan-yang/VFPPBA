import hashlib
import os
from Crypto.Cipher import AES
import cv2
from matplotlib import pyplot as plt
from PIL import Image

def encrypt(inputkey):
    encrypt_color(inputkey,'../common/color/', enc2pngcolor)
    encrypt_grey(inputkey,'../common/grey/', enc2pnggrey)

def encrypt_color(inputkey, dir, f1):
    global keyenc
    input_file = dir + 'input_lenna.png'
    histogram_image(input_file, dir + 'input_histogram.png')

    input_dir = os.path.dirname(input_file)

    hash = hashlib.sha256(bytes(inputkey, 'utf-8'))
    keyenc = hash.digest()
    iv = hash.digest().ljust(16)[:16]

    input_file = open(input_file, 'rb')
    input_data = input_file.read()
    input_file.close()
    enc_image(input_data, keyenc, iv, input_dir)
    print("Enc ended successfully File Stored as: encrypted.enc")
    f1(dir, input_data)
    histogram_image(dir +'encrypted_lenna.png',  dir + 'encrypted_histogram.png')


def encrypt_grey(inputkey, dir, f1):
    global keyenc
    input_file = dir + 'input_lenna.png'
    histogram_image(input_file, dir + 'input_histogram.png')

    input_dir = os.path.dirname(input_file)

    hash = hashlib.sha256(bytes(inputkey, 'utf-8'))
    keyenc = hash.digest()
    iv = hash.digest().ljust(16)[:16]

    input_file = open(input_file, 'rb')
    input_data = input_file.read()
    input_file.close()
    enc_image(input_data, keyenc, iv, input_dir)
    print("Enc ended successfully File Stored as: encrypted.enc")
    f1(dir, input_data)
    histogram_image(dir +'encrypted_lenna.png',  dir + 'encrypted_histogram.png')

def decrypt(outputkey):
    decrypt_color(outputkey,'../common/color/' )
    decrypt_color(outputkey, '../common/grey/')

def decrypt_color(outputkey, dir):
    output_file = dir+ 'encrypted.enc'
    dir = os.path.dirname(output_file)

    hash = hashlib.sha256(bytes(outputkey, 'utf-8'))
    keydec = hash.digest()
    iv = hash.digest().ljust(16)[:16]

    input_file = open(output_file, 'rb')
    input_data = input_file.read()
    input_file.close()
    if keyenc == keydec:
        print('Same key: keyenc: keydec', keyenc, keydec)
        dec_image(input_data, keydec, iv, dir)
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


def dec_image(input_data, key, iv, dir):
    cfb_decipher = AES.new(key, AES.MODE_CFB, iv)
    plain_data = cfb_decipher.decrypt(input_data)

    output_file = open(dir + "/output_lenna.png", "wb")
    output_file.write(plain_data)
    output_file.close()
    output_file_histogram = dir +  '/output_lenna.png'
    histogram_image(output_file_histogram, dir + '/output_histogram.png')


def histogram_image(input_data, dir):
    img = cv2.imread(input_data)
    plt.hist(img.ravel(), 256, [0, 256])
    plt.savefig(dir)
    plt.close()


def enc2pngcolor(dir, input_data):
    img = Image.frombuffer('RGB', (960, 960), input_data)
    img.save(dir + "encrypted_lenna.png")


def enc2pnggrey(dir, input_data):
    img = Image.frombuffer('RGB', (100, 100), input_data)
    img.save(dir + "encrypted_lenna.png")
