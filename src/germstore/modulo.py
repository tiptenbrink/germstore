from Crypto.Random.random import randrange
import argparse


def sequence(max_num_incl=2048, sequence_len=24):
    print(f"Generating sequence of {sequence_len} numbers 1-{max_num_incl}...")
    for i in range(sequence_len):
        print(randrange(1, max_num_incl + 1))


def run():
    cli_name = "germ-otp"
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description="Generate a one-time pad.\n\n"
                                                 "examples:\n"
                                                 f"{cli_name}\n "
                                                 f"{cli_name} -m 2048 -l 24\n")

    max_num_nm = 'maxnumincl'
    default_max = 2048
    max_help = f"Maximum generated number, corresponds to the modulo number (default: {default_max})"
    parser.add_argument('-m', f'--{max_num_nm}', default=2048, help=max_help, required=False)

    seq_len_nm = 'seqlen'
    default_len = 24
    len_help = f"Sequence length, how many numbers should be generated (default: {default_len})."
    parser.add_argument('-l', f'--{seq_len_nm}', default=24, help=len_help, required=False)

    config = vars(parser.parse_args())

    sequence(int(config[max_num_nm]), int(config[seq_len_nm]))
