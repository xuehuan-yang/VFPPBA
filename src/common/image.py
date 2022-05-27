import hashlib
import os
from Crypto.Cipher import AES
import cv2
from matplotlib import pyplot as plt
from PIL import Image

dir = '../common/image/'
def encrypt(inputkey):
    global keyenc
    # input_file = dir + 'input_lenna.png'
    input_file = dir + 'input_lennagrey.png'
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
    # enc2pngcolor(input_data)
    enc2pnggrey(input_data)
    histogram_image(dir +'encrypted_lenna.png',  dir + 'encrypted_histogram.png')


def decrypt(outputkey):
    output_file = dir+ 'encrypted.enc'
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

    output_file = open(filepath + "/output_lenna.png", "wb")
    output_file.write(plain_data)
    output_file.close()
    output_file_histogram = dir +  'output_lenna.png'
    histogram_image(output_file_histogram, dir + 'output_histogram.png')


def histogram_image(input_data, output_dir):
    img = cv2.imread(input_data)
    plt.hist(img.ravel(), 256, [0, 256])
    plt.savefig(output_dir)
    plt.close()


def enc2pngcolor(input_data):
    img = Image.frombuffer('RGB', (960, 960), input_data)
    img.save(dir + "encrypted_lenna.png")


def enc2pnggrey(input_data):
    img = Image.frombuffer('RGB', (100, 100), input_data)
    img.save(dir + "encrypted_lenna.png")
