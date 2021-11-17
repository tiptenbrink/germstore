import argparse

from Crypto.Cipher import AES
from typing import Optional, Iterable
import germstore.words as wrd
import germstore.six_bit as six
import germstore.five_bit as five


def encrypt(d_keys: list[bytes], d_data: bytes, g_nonces: Optional[list[bytes]] = None) -> tuple[bytes, list[bytes]]:
    """
    General purpose AES EAX encryption function for any binary data. Can optionally take a nonce.

    :param d_keys: List of 16 byte encryption keys.
    :param d_data:
    :param g_nonces: List of nonces corresponding to keys. If not provided, a random 16 byte nonce is generated.
    :return: Returns the ciphertext and nonce.
    """
    given_nonces = True
    # If nonces are not given, this makes an empty iterable so nonces are auto-generated
    if g_nonces is None:
        g_nonces = [b''] * len(d_keys)
        given_nonces = False
    d_nonces = []
    d_ciphertext = d_data
    for i_key, i_nonce in zip(d_keys, g_nonces):
        if given_nonces:
            cipher = AES.new(i_key, AES.MODE_EAX, nonce=i_nonce)
        else:
            cipher = AES.new(i_key, AES.MODE_EAX)
        d_ciphertext = cipher.encrypt(d_ciphertext)
        d_nonces.append(cipher.nonce)
    return d_ciphertext, d_nonces


def decrypt(d_keys: list[bytes], d_nonces: list[bytes], d_ciphertext: bytes) -> bytes:
    """
    General purpose AES EAX decryption function for binary ciphertext. Requires the correct nonces and keys.

    :param d_keys: List of 16 byte encryption keys.
    :param d_nonces: List of nonces corresponding to keys.
    :param d_ciphertext:
    :return: Returns the decrypted data.
    """
    d_data = d_ciphertext
    for i_key, i_nonce in zip(d_keys, d_nonces):
        cipher = AES.new(i_key, AES.MODE_EAX, i_nonce)
        d_data = cipher.decrypt(d_data)
    return d_data


def bytes_to_bits(btes: bytes):
    bit_string = ''
    for byte in btes:
        bit_string += format(int.from_bytes([byte], byteorder='big'), '08b')
    return bit_string


class EncodingError(ValueError):
    pass


def encryption(plaintext: str | Iterable[str] | bytes | bytearray | memoryview, encoding: Optional[str] = None,
               keys: list[str] | list[bytes] | None = None, nonces: list[str] | list[bytes] | None = None,
               cipher_decoding: Optional[str] = None) -> str | bytes:
    try:
        if isinstance(plaintext, str):
            if encoding is None:
                raise ValueError("A string was supplied, please denote which encoding to use to convert the string to a"
                                 "binary format. All Python standard encodings are supported, such as 'utf-8'. Custom"
                                 "encodings include '5BC, '6BC' and 'bip39. The latter accepts a joined string of words"
                                 "or list of words.")
            if encoding == '5bc' or encoding == '5BC' or encoding == '5-bit code':
                b_data = five.encode(plaintext)
            elif encoding == '6bc' or encoding == '6BC' or encoding == '6-bit code':
                b_data = six.encode(plaintext)
            elif encoding == 'bip39':
                word_list = wrd.find_words(plaintext)
                b_data = wrd.enc_plain(word_list)
            else:
                b_data = plaintext.encode(encoding)
        elif encoding == 'bip39':
            word_list = list(plaintext)
            b_data = wrd.enc_plain(word_list)
        elif encoding == '5bcwords' or encoding == '5bc_words':
            plaintext = wrd.get_word_space_string(plaintext)
            b_data = five.encode(plaintext)
        else:
            b_data = plaintext
    except (ValueError, LookupError) as e:
        raise EncodingError(f"{e}\nFailed to encode plaintext as binary data...")

    b_ciphertext, b_nonces = encrypt(keys, b_data, nonces)

    try:
        if cipher_decoding is not None:
            if cipher_decoding == '5bc' or cipher_decoding == '5BC' or cipher_decoding == '5-bit code':
                ciphertext = five.decode(b_ciphertext)
            elif cipher_decoding == '6bc' or cipher_decoding == '6BC' or cipher_decoding == '6-bit code':
                ciphertext = six.decode(b_ciphertext)
            elif cipher_decoding == '6bcecc' or cipher_decoding == '6BCECC' or cipher_decoding == '6BC_ECC':
                ciphertext = six.decode_with_gf64(b_ciphertext)
            elif cipher_decoding == 'hex':
                ciphertext = b_ciphertext.hex()
            else:
                ciphertext = b_ciphertext.decode(cipher_decoding)
        else:
            return b_ciphertext
    except (ValueError, LookupError) as e:
        raise EncodingError(f"{e}\nFailed to decode binary ciphertext as string...")

    return ciphertext


def decryption(ciphertext: str | bytes | bytearray | memoryview, cipher_encoding, keys, nonces,
               decoding) -> str | list[str] | bytes:
    if isinstance(ciphertext, str):
        if cipher_encoding is None:
            raise ValueError("A string was supplied, please denote which encoding to use to convert the string to a"
                             "binary format. All Python standard encodings are supported, such as 'utf-8'. Custom"
                             "encodings include '5BC, '6BC' and 'bip39. The latter accepts a joined string of words"
                             "or list of words. 'hex' is also supported.")
        if cipher_encoding == '5bc' or cipher_encoding == '5BC' or cipher_encoding == '5-bit code':
            b_cipher = five.encode(ciphertext)
        elif cipher_encoding == '6bc' or cipher_encoding == '6BC' or cipher_encoding == '6-bit code':
            b_cipher = six.encode(ciphertext)
        elif cipher_encoding == '6bcecc' or cipher_encoding == '6BCECC' or cipher_encoding == '6BC_ECC':
            b_cipher = six.encode_with_gf64(ciphertext)
        elif cipher_encoding == 'hex':
            b_cipher = bytes.fromhex(ciphertext)
        else:
            b_cipher = ciphertext.encode(cipher_encoding)
    else:
        b_cipher = ciphertext

    b_plaintext = decrypt(keys, nonces, b_cipher)

    if decoding is None:
        return b_plaintext
    if decoding == '5bc' or decoding == '5BC' or decoding == '5-bit code':
        plaintext = five.decode(b_plaintext)
    elif decoding == '6bc' or decoding == '6BC' or decoding == '6-bit code':
        plaintext = six.decode(b_plaintext)
    elif decoding == '6bcecc' or decoding == '6BCECC' or decoding == '6BC_ECC':
        plaintext = six.decode_with_gf64(b_plaintext)
    elif decoding == 'bip39':
        plaintext = wrd.dec_plain(b_plaintext)
    elif decoding == 'hex':
        plaintext = b_plaintext.hex()
    else:
        plaintext = b_plaintext.decode(decoding)

    return plaintext
