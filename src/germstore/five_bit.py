def encode(five_bit_string: str) -> bytes:
    five_bit_string += ((8 - (len(five_bit_string) % 8)) % 8) * '&'
    encoded_bytes = b''
    for word in [five_bit_string[i:i + 8] for i in range(0, len(five_bit_string), 8)]:
        encoded_bytes += encode_word(word)
    return encoded_bytes


def decode(five_bit_encoded_bytes: bytes) -> str:
    if len(five_bit_encoded_bytes) % 5 != 0:
        raise ValueError('Must be a multiple of 5 bytes!')
    decoded_string = ''
    for encoded_word in [five_bit_encoded_bytes[i:i + 5] for i in range(0, len(five_bit_encoded_bytes), 5)]:
        decoded_string += decode_word(encoded_word, False)
    return decoded_string


def encode_word(word: str) -> bytes:
    if len(word) > 8:
        raise ValueError('Word cannot be longer than 9 characters!')
    binstring = ''
    for letter in word:
        binletter = format(convert_letter(letter), '05b')
        binstring += binletter
    binstring += (8 - len(word)) * format(convert_letter('&'), '05b')
    encoded_int = int(binstring, 2)
    encoded_bytes = encoded_int.to_bytes(5, byteorder='big')
    return encoded_bytes


def decode_word(encoded_5_bytes: bytes, strip_ampersand=True) -> str:
    if len(encoded_5_bytes) != 5:
        raise ValueError('Must consist of exactly 5 bytes!')
    encoded_int = int.from_bytes(encoded_5_bytes, byteorder='big', signed=False)
    binstring = format(encoded_int, '040b')
    decoded_string = ''
    for five_bit in [binstring[i:i + 5] for i in range(0, 40, 5)]:
        number = int(five_bit, 2)
        decoded_string += convert_number(number)
    if strip_ampersand:
        decoded_string = decoded_string.rstrip('&')
    return decoded_string


def convert_number(number: int) -> str:
    if number == 26:
        return '&'
    elif number == 4:
        return 'e'
    elif number == 19:
        return 't'
    elif number == 0:
        return 'a'
    elif number == 14:
        return 'o'
    elif number == 8:
        return 'i'
    elif number == 13:
        return 'n'
    elif number == 18:
        return 's'
    elif number == 7:
        return 'h'
    elif number == 17:
        return 'r'
    elif number == 3:
        return 'd'
    elif number == 11:
        return 'l'
    elif number == 2:
        return 'c'
    elif number == 20:
        return 'u'
    elif number == 12:
        return 'm'
    elif number == 22:
        return 'w'
    elif number == 5:
        return 'f'
    elif number == 6:
        return 'g'
    elif number == 24:
        return 'y'
    elif number == 15:
        return 'p'
    elif number == 1:
        return 'b'
    elif number == 21:
        return 'v'
    elif number == 10:
        return 'k'
    elif number == 9:
        return 'j'
    elif number == 23:
        return 'x'
    elif number == 16:
        return 'q'
    elif number == 25:
        return 'z'
    if number == 27:
        return '2'
    if number == 28:
        return '3'
    if number == 29:
        return '4'
    if number == 30:
        return '7'
    if number == 31:
        return '8'
    else:
        raise ValueError(repr(number) + " is not an int 0-25!")


def convert_letter(letter: str) -> int:
    letter = letter.lower()
    if letter == 'e':
        return 4
    elif letter == 't':
        return 19
    elif letter == 'a':
        return 0
    elif letter == 'o':
        return 14
    elif letter == 'i':
        return 8
    elif letter == 'n':
        return 13
    elif letter == 's':
        return 18
    elif letter == 'h':
        return 7
    elif letter == 'r':
        return 17
    elif letter == 'd':
        return 3
    elif letter == 'l':
        return 11
    elif letter == 'c':
        return 2
    elif letter == 'u':
        return 20
    elif letter == 'm':
        return 12
    elif letter == 'w':
        return 22
    elif letter == 'f':
        return 5
    elif letter == 'g':
        return 6
    elif letter == 'y':
        return 24
    elif letter == 'p':
        return 15
    elif letter == 'b':
        return 1
    elif letter == 'v':
        return 21
    elif letter == 'k':
        return 10
    elif letter == 'j':
        return 9
    elif letter == 'x':
        return 23
    elif letter == 'q':
        return 16
    elif letter == 'z':
        return 25
    elif letter == '&' or letter == ' ':
        return 26
    elif letter == '2':
        return 27
    elif letter == '3':
        return 28
    elif letter == '4':
        return 29
    elif letter == '7':
        return 30
    elif letter == '8':
        return 31
    else:
        raise ValueError(repr(letter) + " is not an alphabetic character!")


def test_allowed_encode(unencoded: str):
    letter = ''
    try:
        for letter in unencoded:
            convert_letter(letter)
    except ValueError:
        raise ValueError(repr(letter) + " is not valid encoding character!")
