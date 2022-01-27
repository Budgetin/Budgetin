import pyDes
import binascii

def encrypt_3des(password, key):
    triple_des = pyDes.triple_des(
        key, pyDes.ECB, pad=None, padmode=pyDes.PAD_PKCS5)

    encrypted = triple_des.encrypt(password)
    encrypted_password = binascii.hexlify(encrypted).decode('utf-8')

    return encrypted_password