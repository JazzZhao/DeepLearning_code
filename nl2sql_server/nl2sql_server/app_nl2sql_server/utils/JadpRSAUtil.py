from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import binascii
import time
import json

def get_public_key(modulus_str, exponent_str):
    modulus = int(modulus_str)
    exponent = int(exponent_str)
    return rsa.RSAPublicNumbers(e=exponent, n=modulus).public_key(default_backend())

def do_encrypt(message, public_key):
    return binascii.hexlify(public_key.encrypt(
        message.encode(),
        padding.PKCS1v15()
    )).decode()

def main():
    date_time = time.time()
    time_a = (int)(date_time*1000)
    param = {
        "account": "dawate@csg.cn",
        "systemName": "TOP",
        "dateTime": time_a
    }
    param_str = json.dumps(param)
 
if __name__ == "__main__":
    main()