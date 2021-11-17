import germstore.gf64 as gf64


def character_n(character):
    match character:
        case 'a':
            n = 0
        case 'b':
            n = 1
        case 'c':
            n = 2
        case 'd':
            n = 3
        case 'e':
            n = 4
        case 'f':
            n = 5
        case 'g':
            n = 6
        case 'h':
            n = 7
        case 'i':
            n = 8
        case 'k':
            n = 9
        case 'm':
            n = 10
        case 'p':
            n = 11
        case 'q':
            n = 12
        case 'r':
            n = 13
        case 's':
            n = 14
        case 't':
            n = 15
        case 'u':
            n = 16
        case 'w':
            n = 17
        case 'x':
            n = 18
        case 'y':
            n = 19
        case 'z':
            n = 20
        case '2':
            n = 21
        case '3':
            n = 22
        case '4':
            n = 23
        case '7':
            n = 24
        case '8':
            n = 25
        case 'γ':
            n = 26
        case 'Δ':
            n = 27
        case 'θ':
            n = 28
        case 'λ':
            n = 29
        case 'φ':
            n = 30
        case 'ψ':
            n = 31
        case 'Ω':
            n = 32
        case 'Σ':
            n = 33
        case '고':
            n = 34
        case '구':
            n = 35
        case '긔':
            n = 36
        case '브':
            n = 37
        case '뵤':
            n = 38
        case 'ㄆ':
            n = 39
        case 'ㄍ':
            n = 40
        case 'ㄖ':
            n = 41
        case 'ㄤ':
            n = 42
        case 'ㄠ':
            n = 43
        case 'क':
            n = 44
        case 'ज':
            n = 45
        case 'थ':
            n = 46
        case 'ञ':
            n = 47
        case 'ण':
            n = 48
        case 'ち':
            n = 49
        case 'ま':
            n = 50
        case 'よ':
            n = 51
        case 'う':
            n = 52
        case 'の':
            n = 53
        case '@':
            n = 54
        case '%':
            n = 55
        case '?':
            n = 56
        case '*':
            n = 57
        case '}':
            n = 58
        case 'ᜇ':
            n = 59
        case 'ᜐ':
            n = 60
        case 'ᜉ':
            n = 61
        case 'ᜄ':
            n = 62
        case 'ᜋ':
            n = 63
        case _:
            raise ValueError("Invalid input character!")
    return n


def n_character(n: int):
    match n:
        case 0:
            c = 'a'
        case 1:
            c = 'b'
        case 2:
            c = 'c'
        case 3:
            c = 'd'
        case 4:
            c = 'e'
        case 5:
            c = 'f'
        case 6:
            c = 'g'
        case 7:
            c = 'h'
        case 8:
            c = 'i'
        case 9:
            c = 'k'
        case 10:
            c = 'm'
        case 11:
            c = 'p'
        case 12:
            c = 'q'
        case 13:
            c = 'r'
        case 14:
            c = 's'
        case 15:
            c = 't'
        case 16:
            c = 'u'
        case 17:
            c = 'w'
        case 18:
            c = 'x'
        case 19:
            c = 'y'
        case 20:
            c = 'z'
        case 21:
            c = '2'
        case 22:
            c = '3'
        case 23:
            c = '4'
        case 24:
            c = '7'
        case 25:
            c = '8'
        case 26:
            c = 'γ'
        case 27:
            c = 'Δ'
        case 28:
            c = 'θ'
        case 29:
            c = 'λ'
        case 30:
            c = 'φ'
        case 31:
            c = 'ψ'
        case 32:
            c = 'Ω'
        case 33:
            c = 'Σ'
        case 34:
            c = '고'
        case 35:
            c = '구'
        case 36:
            c = '긔'
        case 37:
            c = '브'
        case 38:
            c = '뵤'
        case 39:
            c = 'ㄆ'
        case 40:
            c = 'ㄍ'
        case 41:
            c = 'ㄖ'
        case 42:
            c = 'ㄤ'
        case 43:
            c = 'ㄠ'
        case 44:
            c = 'क'
        case 45:
            c = 'ज'
        case 46:
            c = 'थ'
        case 47:
            c = 'ञ'
        case 48:
            c = 'ण'
        case 49:
            c = 'ち'
        case 50:
            c = 'ま'
        case 51:
            c = 'よ'
        case 52:
            c = 'う'
        case 53:
            c = 'の'
        case 54:
            c = '@'
        case 55:
            c = '%'
        case 56:
            c = '?'
        case 57:
            c = '*'
        case 58:
            c = '}'
        case 59:
            c = 'ᜇ'
        case 60:
            c = 'ᜐ'
        case 61:
            c = 'ᜉ'
        case 62:
            c = 'ᜄ'
        case 63:
            c = 'ᜋ'
        case _:
            raise ValueError("n must follow: 0<=n<=63")
    return c


def decode_ints(enc_sixbit: bytes) -> list[int]:
    if len(enc_sixbit) % 3 != 0:
        raise ValueError("Bytestring must consist of a multiple of three bytes!")
    sixbits = []
    for three_bytes in [enc_sixbit[i:i + 3] for i in range(0, len(enc_sixbit), 3)]:
        twentyfour_bit = int.from_bytes(three_bytes, byteorder='big')
        twentyfour_bit = format(twentyfour_bit, '024b')
        for sixbit in [twentyfour_bit[i: i + 6] for i in range(0, len(twentyfour_bit), 6)]:
            sixbit_int = int(sixbit, 2)
            sixbits.append(sixbit_int)
    return sixbits


def decode(enc_sixbit: bytes) -> str:
    dec_ints = decode_ints(enc_sixbit)
    return ''.join(map(n_character, dec_ints))


def encode(sixbit_chars: str) -> bytes:
    if len(sixbit_chars) % 4 != 0:
        raise ValueError("String must consist of a multiple of four characters!")
    encoded_bytes = b''
    for four_chars in [sixbit_chars[i:i + 4] for i in range(0, len(sixbit_chars), 4)]:
        four_char_bits = ''
        for char in four_chars:
            four_char_bits += format(character_n(char), '06b')
        four_char_int = int(four_char_bits, 2)
        encoded_bytes += four_char_int.to_bytes(3, byteorder='big')
    return encoded_bytes


def decode_with_gf64(enc_sixbit: bytes):
    dec_ints = decode_ints(enc_sixbit)
    if len(dec_ints) % 44 != 0:
        raise ValueError("Expecting a multiple of 44 characters! (i.e. 264 bits, 33 bytes)")
    final_list = []
    for eleven_ints in [dec_ints[i:i + 11] for i in range(0, len(dec_ints), 11)]:
        p = gf64.calc_p_syndrome(eleven_ints)
        q = gf64.calc_q_syndrome(eleven_ints)
        final_list += eleven_ints + [p, q]
    return ''.join(map(n_character, final_list))


def encode_with_gf64(sixbit_chars: str, check_correction=True):
    if len(sixbit_chars) % 52 != 0:
        raise ValueError("Expecting a multiple of 52 characters! (i.e. 312 bits, 39 bytes)")

    char_bits = ''
    for thirteen_chars in [sixbit_chars[i:i + 13] for i in range(0, len(sixbit_chars), 13)]:

        thirteen_ints = list(map(character_n, thirteen_chars))
        eleven_ints = thirteen_ints[:-2]
        if check_correction:
            p = thirteen_ints[-2]
            q = thirteen_ints[-1]
            eleven_ints, _p, _q = gf64.correct_corruption(eleven_ints, p, q)
        for char_int in eleven_ints:
            char_bits += format(char_int, '06b')

    encoded_bytes = b''
    for twentyfour_bits in [char_bits[i:i + 24] for i in range(0, len(char_bits), 24)]:
        twentyfour_bit_int = int(twentyfour_bits, 2)
        encoded_bytes += twentyfour_bit_int.to_bytes(3, byteorder='big')

    return encoded_bytes
