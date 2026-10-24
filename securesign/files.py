def read_file(path: str) -> bytes:
    with open(path, "rb") as f:
        return f.read()


def write_signature(signature: bytes, path: str) -> None:
    with open(path, "wb") as f:
        f.write(signature)


def read_signature(path: str) -> bytes:
    with open(path, "rb") as f:
        return f.read()
