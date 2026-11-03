from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding, rsa

_PSS = padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH)


def generate_keys():
    return rsa.generate_private_key(public_exponent=65537, key_size=3072)


def sign(data: bytes, private_key) -> bytes:
    return private_key.sign(data, _PSS, hashes.SHA256())


def verify(data: bytes, signature: bytes, public_key) -> bool:
    try:
        public_key.verify(signature, data, _PSS, hashes.SHA256())
    except InvalidSignature:
        return False
    return True
