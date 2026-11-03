from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec


def generate_keys() -> ec.EllipticCurvePrivateKey:
    return ec.generate_private_key(ec.SECP256R1())


def sign(data: bytes, private_key: ec.EllipticCurvePrivateKey) -> bytes:
    return private_key.sign(data, ec.ECDSA(hashes.SHA256()))


def verify(data: bytes, signature: bytes, public_key: ec.EllipticCurvePublicKey) -> bool:
    try:
        public_key.verify(signature, data, ec.ECDSA(hashes.SHA256()))
        return True
    except InvalidSignature:
        return False
