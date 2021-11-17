import sancty
import germstore.crypt as crypt
import germstore.six_bit as six
import germstore.five_bit as five
import germstore.words as wrd
import argparse
import time

replace_dict = {
    "gamma": "γ",  # greek lowercase gamma
    "Delta": "Δ",  # greek uppercase delta
    "theta": "θ",  # greek lowercase theta
    "lambda": "λ",  # greek lowercase lambda
    "phi": "φ",  # greek lowercase phi
    "psi": "ψ",  # greek lowercase psi
    "omega": "Ω",  # greek omega
    "Sigma": "Σ",  # greek uppercase sigma
    "hggo": "고",  # hangul (hg) ㄱ/'g (RR)' + ㅗ/'o (RR)'
    "hgguu": "구",  # hangul (hg) ㄱ/'g (RR)' + ㅜ/'u (RR)'
    "hggui": "긔",  # hangul (hg) ㄱ/'g (RR)' + ㅢ/'ui (RR)'
    "hgbyo": "뵤",  # hangul (hg) ㅂ/'b (RR)' + ㅛ/'yo (RR)'
    "hgbeu": "브",  # hangul (hg) ㅂ/'b (RR)' + ㅡ/'eu (RR)'
    "bmp": "ㄆ",  # bopomofo (bm) 'p (pinyin)'
    "bmg": "ㄍ",  # bopomofo (bm) 'g (pinyin)'
    "bmr": "ㄖ",  # bopomofo (bm) 'ri/r- (pinyin)'
    "bmang": "ㄤ",  # bopomofo (bm) 'ang (pinyin)'
    "bmao": "ㄠ",  # bopomofo (bm) 'ao (pinyin)'
    "dgka": "क",  # devanagari (dg) sparśa-aghoṣa-alpaprāṇa-kaṇṭhya 'ka (IAST)'
    "dgja": "ज",  # devanagari (dg) sparśa-saghoṣa-alpaprāṇa-tālavya 'ja (IAST)'
    "dgtha": "थ",  # devanagari (dg) sparśa-aghoṣa-mahāprāṇa-dantya 'tha (IAST)'
    "dgena": "ञ",  # devanagari (dg) anunāsika-saghoṣa-alpaprāṇa-tālavya 'ña (IAST)'
    "dgnga": "ण",  # devanagari (dg) anunāsika-saghoṣa-alpaprāṇa-mūrdhanya 'ṇa (IAST)'
    "hrchi": "ち",  # hiragana (hr) 'chi (Hepburn)'
    "hrma": "ま",  # hiragana (hr) 'ma (Hepburn)'
    "hryo": "よ",  # hiragana (hr) 'yo (Hepburn)'
    "hru": "う",  # hiragana (hr) 'u (Hepburn)'
    "hrno": "の",  # hiragana (hr) 'no (Hepburn)'
    "bbda": "ᜇ",  # baybayin (bb) 'da'
    "bbsa": "ᜐ",  # baybayin (bb) 'sa'
    "bbpa": "ᜉ",  # baybayin (bb) 'pa'
    "bbga": "ᜄ",  # baybayin (bb) 'ga'
    "bbma": "ᜋ",  # baybayin (bb) 'ma'
    "encrypt": (0, "Encrypt each line"),
    "decrypt": (1, "Decrypt the current line")
}


def base_slash_fn(control_num, render_copy, paragraphs_copy, key, nonce, en_enc, en_dec, de_enc, de_dec) -> tuple[list, list]:
    new_render = render_copy
    new_paragraphs = paragraphs_copy
    if control_num == 0:
        new_paragraphs = []
        full_lines = [line for line in render_copy if line != '']
        words = ' '.join(full_lines).split(' ')
        try:
            encr = crypt.encryption(words, en_enc, [key], [nonce], en_dec)
        except crypt.EncodingError as vle:
            raise sancty.ExternalError(vle)
        new_render = [str(encr)]

        return new_render, new_paragraphs
    elif control_num == 1:
        if render_copy:
            last_line = render_copy[-1].strip()
            try:
                decr = crypt.decryption(last_line, de_enc, [key], [nonce], de_dec)
            except crypt.EncodingError as vle:
                raise sancty.ExternalError(vle)
            new_render = decr
            new_paragraphs = [i for i in range(len(new_render))]

        return new_render, new_paragraphs
    else:
        return render_copy, paragraphs_copy


def run():
    cli_name = 'germ-sancty'
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description="Editor to perform encrypt or decrypt.\n\n"
                                                 "examples:\n"
                                                 f"{cli_name} -k 3cae1de10109cfeae4bca578778fccf9a6c3a93a29f87fffc51356a7d6d48394 -n 0c2a835b3e41521f358c83a1f3135bbf -ee bip39\n")

    key_nm = 'key'
    key_help = "Key (as hex)"
    parser.add_argument('-k', f'--{key_nm}', help=key_help, required=True)

    nonce_nm = 'nonce'
    nonce_help = "Nonce (as hex)"
    parser.add_argument('-n', f'--{nonce_nm}', help=nonce_help, required=True)

    en_enc_nm = 'encryptplainencoding'
    en_enc_help = "Encoding of the plaintext that is inputted to encrypt."
    parser.add_argument('-ee', f'--{en_enc_nm}', help=en_enc_help, required=True)

    en_dec_nm = 'encryptcipherdecoding'
    en_dec_default = '6bcecc'
    en_dec_help = f"Encoding of the ciphertext that the encryption generates. (default: {en_dec_default})."
    parser.add_argument('-ed', f'--{en_dec_nm}', help=en_dec_help, default=en_dec_default, required=False)

    de_enc_nm = 'decryptcipherencoding'
    de_dec_default = en_dec_default
    de_enc_help = f"Encoding of the ciphertext that is inputted to decrypt. (default: {de_dec_default})."
    parser.add_argument('-de', f'--{de_enc_nm}', help=de_enc_help, default=de_dec_default, required=False)

    de_dec_nm = 'decryptplaindecoding'
    de_dec_help = f"Decoding of the plaintext that the decryption generates (default: same as {en_enc_nm})."
    parser.add_argument('-dd', f'--{de_dec_nm}', help=de_dec_help, default=None, required=False)

    config = vars(parser.parse_args())

    if config[de_dec_nm] is None:
        config[de_dec_nm] = config[en_enc_nm]

    #nonce = six.encode('cㄤथhजt@ᜋbψeabg8γγ%rजकθよdqadᜉ')
    nonce = bytes.fromhex(config[nonce_nm])
    #key = bytes.fromhex("3cae1de10109cfeae4bca578778fccf9a6c3a93a29f87fffc51356a7d6d48394")
    key = bytes.fromhex(config[key_nm])

    def slash_fn(control_num, render_copy, paragraphs_copy):
        return base_slash_fn(control_num, render_copy, paragraphs_copy,
                             key, nonce, config[en_enc_nm], config[en_dec_nm], config[de_enc_nm], config[de_dec_nm])

    sancty.start_terminal(replace_dict=replace_dict, special_slash_fn=slash_fn)