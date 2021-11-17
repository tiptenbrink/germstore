import hashlib
import argparse
from Crypto.Random import get_random_bytes


def get(password: str, salt=None):
    if salt is None:
        salt = get_random_bytes(16)
        print("Generating random salt...")
    else:
        salt = bytes.fromhex(salt)
    pass_bytes = password.encode('utf-8')
    print(f"Using salt hex: {salt.hex()} | Using password hex: {pass_bytes.hex()}")
    print("Generating 256-bit key...")
    m = hashlib.pbkdf2_hmac('sha256', pass_bytes, salt, 1000000)
    print(m.hex())


def run():
    cli_name = "germ-derive"
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description="Derive a key using a random salt and password.\n\n"
                                                 "examples:\n"
                                                 f"{cli_name} -p mypassword -s 0c2a835b3e41521f358c83a1f3135bbf\n"
                                                 f"{cli_name} -p somepassword\n")

    pass_nm = 'password'
    pass_help = "Password, can be any amount of Unicode characters that your terminal can handle."
    parser.add_argument('-p', f'--{pass_nm}', help=pass_help, required=True)

    salt_help = "Salt bytes in hex form, 16 bytes are recommended (32 hex characters). " \
                "Store this somewhere you won't lose it."
    salt_nm = 'salt'
    parser.add_argument('-s', f'--{salt_nm}', default=None, help=salt_help, required=False)

    config = vars(parser.parse_args())

    get(config[pass_nm], config[salt_nm])
