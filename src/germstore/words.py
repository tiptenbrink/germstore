import random
from pathlib import Path

here = Path(__file__).parent
word_path = here.joinpath("./word_list.txt")


def word_to_number(word: str):
    with open(word_path) as f:
        words: list[str] = f.read().splitlines()
        return words.index(word)


def number_to_word(n: int):
    with open(word_path) as f:
        words: list[str] = f.read().splitlines()
        return words[n]


def generate_24_words():
    with open(word_path) as f:
        word_list = f.read().splitlines()

    r_indexes = [random.randint(0, len(word_list) - 1) for _i in range(24)]

    words = [word_list[r_index] for r_index in r_indexes]

    return words


def word_newline_to_word_list(word_newline_string):
    word_split = word_newline_string.split('\n')
    word_list = []
    for word in word_split:
        if word:
            word_list.append(word)
    return word_list


def get_word_space_string(word_list, word_length=8):
    word_space_string = ''
    for word in word_list:
        if word_length == 5 and len(word) < 5:
            word = '-' + word
        word_space_string += word + (word_length - len(word)) * ' '
    return word_space_string


def get_spaced_words(word_list, word_length=8):
    spaced_words = []
    for word in word_list:
        spaced_words.append(word + (word_length - len(word)) * ' ')
    return spaced_words


def word_space_to_word_newline(word_space_string, word_length=8, strip_end=True):
    word_newline_string = ''
    for word in [word_space_string[i:i + word_length] for i in range(0, len(word_space_string), word_length)]:
        if strip_end:
            word = word.rstrip(' ')
            word = word.rstrip('&')
        word_newline_string += word + '\n'
    return word_newline_string.rstrip('\n')


def find_words(concat_words):
    with open(word_path) as f:
        words: list[str] = f.read().splitlines()
    char_arr = list(concat_words)
    word_list = []
    while len(char_arr) > 1:
        matching = []
        current_word = char_arr.pop(0)
        while len(matching) != 1:
            current_word += char_arr.pop(0)
            matching = [s for s in words if current_word in s]
            if len(char_arr) == 0 or len(matching) == 0:
                break
        if len(matching) == 0:
            raise ValueError("Could not find unique match for '{}', aborting.".format(current_word))
        else:
            word_list.append(matching[0])
    return word_list


def word_numbers(words_text: list[str]):
    if len(words_text) != 24:
        raise ValueError("Must be list of 24 words exactly!")
    return list(map(word_to_number, words_text))


def word_texts(words_num: list[int]):
    if len(words_num) != 24:
        raise ValueError("Must be list of 24 word numbers exactly!")
    return list(map(number_to_word, words_num))


def num_to_elv_bit(n: int):
    if not n < 2048 and not n >= 0:
        raise ValueError("n must be greater or equal to zero and less than 2048!")
    return format(n, '011b')


def elv_bit_to_num(eleven_bit: str):
    if not len(eleven_bit) == 1 and not all(map(lambda bit: bit == '0' or bit == '1', eleven_bit)):
        raise ValueError("Invalid 11-bit number! Must be 11 long and consist only of ones and zeroes!")
    return int(eleven_bit, 2)


def int_numbers(eleven_bits: list[str]) -> list[int]:
    return list(map(elv_bit_to_num, eleven_bits))


def bit_numbers(ints: list[int]) -> list[str]:
    return list(map(num_to_elv_bit, ints))


def encode(ftn_bits: list[str]) -> bytes:
    # Total bit length must be divisible by eight!
    encoded_bytes = b''
    bit_string = ''.join(ftn_bits)
    for byte in [bit_string[i:i + 8] for i in range(0, len(bit_string), 8)]:
        bte_int = int(byte, 2)
        encoded_bte = bte_int.to_bytes(1, byteorder='big')
        encoded_bytes += encoded_bte
    return encoded_bytes


def decode(enc_bits: bytes) -> list[str]:
    bit_string = ''
    for byte in enc_bits:
        eight_int = int.from_bytes([byte], byteorder='big')
        eight_bit = format(eight_int, '08b')
        bit_string += eight_bit
    eleven_bit_list = []
    for eleven_bits in [bit_string[i:i + 11] for i in range(0, len(bit_string), 11)]:
        eleven_bit_list.append(eleven_bits)

    return eleven_bit_list


def enc_plain(words: list[str]) -> bytes:
    words_n = word_numbers(words)
    bit_nums = bit_numbers(words_n)
    return encode(bit_nums)


def dec_plain(enc_words: bytes) -> list[str]:
    bit_nums = decode(enc_words)
    words_num = int_numbers(bit_nums)
    return word_texts(words_num)
