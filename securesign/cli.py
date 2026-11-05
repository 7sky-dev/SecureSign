import argparse
import sys

from securesign import ecdsa_sign, files, keys, rsa_sign

ALGORITHMS = {"rsa": rsa_sign, "ecdsa": ecdsa_sign}


def keygen(args) -> int:
    private_key = ALGORITHMS[args.algo].generate_keys()
    keys.save_private_key(private_key, f"{args.out}.pem")
    keys.save_public_key(private_key.public_key(), f"{args.out}.pub.pem")
    print(f"Keys saved: {args.out}.pem (private), {args.out}.pub.pem (public)")
    return 0


def sign(args) -> int:
    private_key = keys.load_private_key(args.key)
    signature = ALGORITHMS[keys.algorithm_of(private_key)].sign(files.read_file(args.file), private_key)
    files.write_signature(signature, f"{args.file}.sig")
    print(f"Signature saved: {args.file}.sig")
    return 0


def verify(args) -> int:
    public_key = keys.load_public_key(args.pubkey)
    algorithm = ALGORITHMS[keys.algorithm_of(public_key)]
    if algorithm.verify(files.read_file(args.file), files.read_signature(args.sig), public_key):
        print("Signature is VALID")
        return 0
    print("Signature is INVALID")
    return 1


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="securesign", description="RSA-3072 / ECDSA P-256 digital signatures")
    commands = parser.add_subparsers(dest="command", required=True)

    p = commands.add_parser("keygen", help="generate a key pair")
    p.add_argument("--algo", choices=ALGORITHMS, required=True)
    p.add_argument("--out", required=True, help="writes OUT.pem and OUT.pub.pem")
    p.set_defaults(func=keygen)

    p = commands.add_parser("sign", help="sign a file")
    p.add_argument("--key", required=True, help="private key (PEM)")
    p.add_argument("--file", required=True, help="writes FILE.sig")
    p.set_defaults(func=sign)

    p = commands.add_parser("verify", help="verify a signature")
    p.add_argument("--pubkey", required=True, help="public key (PEM)")
    p.add_argument("--file", required=True)
    p.add_argument("--sig", required=True)
    p.set_defaults(func=verify)

    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except (OSError, ValueError) as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
