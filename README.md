# germstore

> Store your seed words safely

Do you also have the obssessive need to secure your [BIP-0039](https://github.com/bitcoin/bips/blob/master/bip-0039.mediawiki) mnmemonic seed beyond all necessity? Then this program is for you.

## Steps

There are two steps in ensuring that your mnemonic seed is safe. All manuals will tell you to *never* store information about this seed on a computer, as you never know what kind of attacker might be watching. So how can a computer program ever be of assistance?

#### One-time pad

That depends on a step that you must manually perform, a one-time pad. Get some pen and paper and generate a sequence of 24 numbers using `germstore.modulo.sequence` (CLI script `germ-opt`). Also, take a look at the alphabetically sorted BIP-0039 word list and write down the numbers (in order!) associated with the words of your mnemonic seed (so if 'avocado' is one of the words on your list, write down 128, we start at 1). Be sure to not make it obvious which word you pick, scroll through the list and do not select it or copy it, just look at the line numbers.

Then, add the generated numbers to the numbers associated with your words, _modulo 2048_. So if you have 2048 and 10, you get 2058->10, if you have 243 and 400 you get 643, if you have 1724 and 922 you get 598, etc.

Be sure to save the generated numbers somewhere safe and in a physical location, because they are the only way to recover your original words, it is mathematically impossible to decrypt them without the one-time key.

Now, you will have a new series of words/numbers that you can safely input into the computer, as an attacker can do nothing with them without your physical one-time pad!

#### Encryption

Of course, just using the one-time pad is not enough, we want at least two layers of security. For that reason, we will also encrypt the resulting string of numbers using AES, which will require the use of a nonce (a random input) and a key. Since we don't want to write down an extremely long key, we will generate it from a short string using a key derivation function and a random input salt (which you can store digitally, just be sure not to lose it!). You can do this using `germstore.key_derivation` (CLI script `germ-derive`).

Be sure you can have both the key and nonce in binary form. Once you do, we can use `germstore.crypt` (see terminal interface below for CLI script) to actually encrypt it, which will produce a binary output.

Now, writing down binary is not very efficient. We will want to use an encoding. Unicode is not usable for arbitrary binary code and hexadecimal is just a tad bit inefficient. For that reason we can use `six-bit code` (hexadecimal would be 'four bits', i.e. you can store four bits with one character, but we can store six). This requires 64 unique characters, significantly more than most alphabets, which sometimes have difficult to distinguish letters.

#### Six-bit code

The standad `six-bit code (6bc/6BC)` uses the following characters, sourced from various visually very distinct alphabetic/syllabic writing system:.

```
abcdefghikmpqrstuwxyz

23478

γΔθλφψΩΣ

고구긔브뵤

ㄆㄍㄖㄤㄠ

कजथञण

ちまようの

@%?*}

ᜇᜐᜉᜄᜋ

    "gamma": "γ ",  # greek lowercase gamma
    "Delta": "Δ ",  # greek uppercase delta
    "theta": "θ ",  # greek lowercase theta
    "lambda": "λ ",  # greek lowercase lambda
    "phi": "φ ",  # greek lowercase phi
    "psi": "ψ ",  # greek lowercase psi
    "omega": "Ω ",  # greek omega
    "Sigma": "Σ ",  # greek uppercase sigma
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
    "dgka": "क ",  # devanagari (dg) sparśa-aghoṣa-alpaprāṇa-kaṇṭhya 'ka (IAST)'
    "dgja": "ज ",  # devanagari (dg) sparśa-saghoṣa-alpaprāṇa-tālavya 'ja (IAST)'
    "dgtha": "थ ",  # devanagari (dg) sparśa-aghoṣa-mahāprāṇa-dantya 'tha (IAST)'
    "dgena": "ञ ",  # devanagari (dg) anunāsika-saghoṣa-alpaprāṇa-tālavya 'ña (IAST)'
    "dgnga": "ण ",  # devanagari (dg) anunāsika-saghoṣa-alpaprāṇa-mūrdhanya 'ṇa (IAST)'
    "hrchi": "ち",  # hiragana (hr) 'chi (Hepburn)'
    "hrma": "ま",  # hiragana (hr) 'ma (Hepburn)'
    "hryo": "よ",  # hiragana (hr) 'yo (Hepburn)'
    "hru": "う",  # hiragana (hr) 'u (Hepburn)'
    "hrno": "の",  # hiragana (hr) 'no (Hepburn)'
    "bbda": "ᜇ ",  # baybayin (bb) 'da'
    "bbsa": "ᜐ ",  # baybayin (bb) 'sa'
    "bbpa": "ᜉ ",  # baybayin (bb) 'pa'
    "bbga": "ᜄ ",  # baybayin (bb) 'ga'
    "bbma": "ᜋ ",  # baybayin (bb) 'ma'
```

#### Error-correcting code

If you are afraid of making errors, worry not as `germstore.six_bit` uses a finite field, GF(64) to be exact, to correct one arbitrary character per eleven characters. This is the same math that is used in RAID 6. 


#### Conclusion

All in all, this allows us to represent 33 bytes of information (24 eleven-bit words) using just 52 characters. Writing out the first four letters of each word (which are unique), would take 96 characters, while writing out the entire words takes up a maximum of 192 characters.

## Terminal interface

This program uses [tiptenbrink/sancty](https://github.com/tiptenbrink/sancty) as an interface to easily perform all the required functions in a scripted terminal text editor. It allows writing all the non-ASCII characters using the control sequences above (i.e. gamma, dgja, bbda).

Run `germ-sancty -h` for instructions, also pasted below:

```
usage: germ-sancty [-h] -k KEY -n NONCE -ee ENCRYPTPLAINENCODING [-ed ENCRYPTCIPHERDECODING] [-de DECRYPTCIPHERENCODING]
                   [-dd DECRYPTPLAINDECODING]

Editor to perform encrypt or decrypt.

examples:
germ-sancty -k 3cae1de10109cfeae4bca578778fccf9a6c3a93a29f87fffc51356a7d6d48394 -n 0c2a835b3e41521f358c83a1f3135bbf -ee bip39

options:
  -h, --help            show this help message and exit
  -k KEY, --key KEY     Key (as hex)
  -n NONCE, --nonce NONCE
                        Nonce (as hex)
  -ee ENCRYPTPLAINENCODING, --encryptplainencoding ENCRYPTPLAINENCODING
                        Encoding of the plaintext that is inputted to encrypt.
  -ed ENCRYPTCIPHERDECODING, --encryptcipherdecoding ENCRYPTCIPHERDECODING
                        Encoding of the ciphertext that the encryption generates. (default: 6bcecc).
  -de DECRYPTCIPHERENCODING, --decryptcipherencoding DECRYPTCIPHERENCODING
                        Encoding of the ciphertext that is inputted to decrypt. (default: 6bcecc).
  -dd DECRYPTPLAINDECODING, --decryptplaindecoding DECRYPTPLAINDECODING
                        Decoding of the plaintext that the decryption generates (default: same as encryptplainencoding).
```

### Usage

Paste in the words transformed using the one-time pad, one word per line and write `\encrypt`. Decrypt using `\decrypt` (expects all characters on one line).

The other two scripts, `germ-derive` and `germ-opt`, also have help functions.