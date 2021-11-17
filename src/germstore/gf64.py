"""
Inspired by "The mathematics of RAID-6" by H. Peter Anvin (version 20 December 2011)
"""

# GF(64), each D is a single 6-bit element

# We use generator x = 2 = 10

# Irreducible x^6 + x^4 +x^3 + x + 1 = 91

generator = 2


def xor_list(xorable_list):
    xor = xorable_list[0]
    for i in xorable_list[1:]:
        xor = xor ^ i
    return xor


def calc_p_syndrome(d_list: list[int]):
    return xor_list(d_list)


def gf64_mult(a: int, b: int):
    p = 0
    while a and b:
        if b & 1:
            p = p ^ a
        if a & 32:
            a = (a << 1) ^ 91  # 91 is irreducible polynomial
        else:
            a = a << 1
        b = b >> 1

    return p


def gf64_pow(base: int, exponent: int) -> int:
    if exponent < 0:
        exponent = 63 + exponent
    if exponent == 0:
        return 1
    result = base
    for _i in range(exponent - 1):
        result = gf64_mult(result, base)
    return result


def gf64_inverse(a: int):
    if a == 0:
        raise ValueError("0 has no inverse!")

    # It holds that the inverse is equal to a^(p^n - 2). We have p=2 and n=6, so a^(64-2)=a^62
    return gf64_pow(a, 62)


def gf64_log_tables():
    log_dict = {}
    for n in range(1, 64):
        lg = 0
        g_val = generator
        while True:
            if n == g_val:
                break
            g_val = gf64_mult(g_val, generator)
            lg += 1
            if lg > 1000:
                raise ValueError("Could not find log after 1000 iterations!")
        log_dict[n] = lg
    return log_dict


gf64_log_table = gf64_log_tables()


def gf64_log_g(a: int):
    if a == 0:
        raise ValueError("Log for 0 undefined!")
    return gf64_log_table[a]


def calc_q_syndrome(d_list):
    xorable_list = []
    generators = [gf64_pow(generator, p) for p in range(len(d_list))]
    for g, d in zip(d_list, generators):
        xorable_list.append(gf64_mult(g, d))
    return xor_list(xorable_list)


def recalculate_data(d_list, p_val, chunk_i: int):
    if chunk_i != 0:
        pre = xor_list(d_list[:chunk_i])
    else:
        pre = 0
    if chunk_i != len(d_list) - 1:
        post = xor_list(d_list[chunk_i + 1:]) ^ p_val
    else:
        post = p_val
    correct_val = pre ^ post
    correct_d_list = d_list.copy()
    correct_d_list[chunk_i] = correct_val
    return correct_d_list


def lost_p_syndrome(d_list: list[int], q_val, chunk_i):
    d_i = d_list.copy()
    d_i[chunk_i] = 0
    q_i = calc_q_syndrome(d_i)
    g_min_i = gf64_pow(generator, -chunk_i)
    d_correct = gf64_mult((q_val ^ q_i), g_min_i)
    d_list_correct = d_list.copy()
    d_list_correct[chunk_i] = d_correct
    p_correct = calc_p_syndrome(d_list_correct)
    return d_list_correct, p_correct


def correct_corruption(d_list, p_val, q_val):
    p_prime = calc_p_syndrome(d_list)
    q_prime = calc_q_syndrome(d_list)
    p_star = p_val ^ p_prime
    q_star = q_val ^ q_prime
    if p_star != 0 and q_star != 0:
        # Data corruption
        corrupted_i = (gf64_log_g(q_star) - gf64_log_g(p_star)) % 63
        if corrupted_i >= len(d_list):
            raise ValueError("There are most likely multiple errors, could not reconstruct!")
        print("Value {} was corrupted! Correcting.".format(corrupted_i))
        d_list_correct = recalculate_data(d_list, p_val, corrupted_i)
        return d_list_correct, p_val, q_val
    else:
        return d_list, p_prime, q_prime
