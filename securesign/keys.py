from cryptography.exceptions import UnsupportedAlgorithm
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec, rsa


def save_private_key(private_key, path: str) -> None:
    pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )
    with open(path, "wb") as f:
        f.write(pem)


def save_public_key(public_key, path: str) -> None:
    pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    with open(path, "wb") as f:
        f.write(pem)


def load_private_key(path: str):
    with open(path, "rb") as f:
        data = f.read()
    try:
        key = serialization.load_pem_private_key(data, password=None)
    except (ValueError, TypeError, UnsupportedAlgorithm) as e:
        # TypeError: the key is password-protected
        raise ValueError(f"cannot load private key from {path}: {e}") from e
    algorithm_of(key)
    return key


def load_public_key(path: str):
    with open(path, "rb") as f:
        data = f.read()
    try:
        key = serialization.load_pem_public_key(data)
    except (ValueError, UnsupportedAlgorithm) as e:
        raise ValueError(f"cannot load public key from {path}: {e}") from e
    algorithm_of(key)
    return key


def algorithm_of(key) -> str:
    if isinstance(key, (rsa.RSAPrivateKey, rsa.RSAPublicKey)):
        return "rsa"
    if isinstance(key, (ec.EllipticCurvePrivateKey, ec.EllipticCurvePublicKey)):
        return "ecdsa"
    raise ValueError(f"unsupported key type: {type(key).__name__}")
