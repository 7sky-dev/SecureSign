# SecureSign

SecureSign is a command-line tool for creating and verifying digital signatures of files. It was created as a project for a Cryptography course.

It supports two signature schemes, both built on the Python [`cryptography`](https://cryptography.io/) library:

| Algorithm | Key | Hash | Details |
|-----------|-----|------|---------|
| RSA | 3072 bits, public exponent 65537 | SHA-256 | PSS padding with MGF1 (SHA-256) and maximum salt length |
| ECDSA | P-256 (SECP256R1) | SHA-256 | Signature stored in DER format |

## How it works

A digital signature shows that a file was signed by the holder of a specific private key and has not changed since.

1. **Key generation:** `keygen` creates a key pair. The private key stays with the signer, and the public key can be shared.
2. **Signing:** `sign` reads the file, hashes it with SHA-256 and signs the hash with the private key. The result is saved next to the file as `FILE.sig`.
3. **Verification:** `verify` uses the public key to check the signature against the file. Changing the file or the signature, or using a different key, makes the signature invalid.

You only choose the algorithm during key generation. `sign` and `verify` detect it from the key they load.

Both schemes are randomized, so signing the same file twice gives different signatures, and both of them verify correctly.

## Installation

Python 3 is required. From the project root:

```bash
python -m venv .venv
```

Activate the environment on Windows:

```bash
.venv\Scripts\activate
```

Or on Linux and macOS:

```bash
source .venv/bin/activate
```

Then install the dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Run all commands from the project root.

Generate a key pair (`--algo` is `rsa` or `ecdsa`). This writes `mykey.pem` (private) and `mykey.pub.pem` (public):

```bash
python -m securesign.cli keygen --algo ecdsa --out mykey
```

Sign a file. This writes `document.pdf.sig`:

```bash
python -m securesign.cli sign --key mykey.pem --file document.pdf
```

Verify a signature:

```bash
python -m securesign.cli verify --pubkey mykey.pub.pem --file document.pdf --sig document.pdf.sig
```

`verify` prints `Signature is VALID` or `Signature is INVALID`.

### Exit codes

| Code | Meaning |
|------|---------|
| 0 | The command succeeded and, for `verify`, the signature is valid |
| 1 | The signature is invalid, or a file or key could not be read or written |
| 2 | The command-line arguments are invalid |

## Project structure

| File | Purpose |
|------|---------|
| `securesign/cli.py` | Command-line interface |
| `securesign/rsa_sign.py` | RSA-3072 key generation, signing and verification |
| `securesign/ecdsa_sign.py` | ECDSA P-256 key generation, signing and verification |
| `securesign/keys.py` | Saving and loading PEM keys, detecting the key algorithm |
| `securesign/files.py` | Reading files, reading and writing signatures |

## Limitations

This is an educational project and has not been audited for production use.

- Private keys are saved unencrypted, and password-protected keys cannot be loaded.
- `keygen` and `sign` overwrite existing output files without asking, so a mistake in `--out` can destroy a private key.
- Any RSA or elliptic-curve key can be loaded, so key size and curve are only guaranteed for keys created by `keygen`.
- A signature does not prove who owns a public key. You must get the public key from a source you trust.
- Files are read into memory in full, so very large files need a lot of RAM.

## Authors

- Piotr Kapeluszny
- Mateusz Bano

## AI assistance

We used AI tools to help us while creating this application.
