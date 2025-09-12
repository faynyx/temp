from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from Crypto.Cipher import AES
import os
import sys


def aes_gcm_simple(plain_text):
    key = AESGCM.generate_key(bit_length=128) # 128, 192, 256 -> Key Size
    aes_gcm = AESGCM(key)
    nonce = os.urandom(12)
    data = plain_text
    aad = b""

    ct = aes_gcm.encrypt(nonce, data, aad)
    pt = aes_gcm.decrypt(nonce, ct, aad)

    print("Cipher Text + Tag : ", ct.hex())
    print("Plain Text : ", pt)

# detail
def b2hex(b): return b.hex()

def inc32(block16):
    prefix = block16[:12]
    ctr = int.from_bytes(block16[12:], "big")
    ctr = (ctr + 1) & 0xffffffff
    return prefix + ctr.to_bytes(4, "big")

def aes_ecb_enc(key, block16):  # AES Mode ECB
    return AES.new(key, AES.MODE_ECB).encrypt(block16)

def aes_gcm_debug(plaintext): # Detail
    key = AESGCM.generate_key(bit_length=128) # 128
    nonce = os.urandom(12)

    # 1) Hash Subkey
    H = aes_ecb_enc(key, b"\x00"*16)
    print ("[+] Hash Subkey H = E_K(0^128) : ", b2hex(H))

    # 2) J0 -> Init Value
    if len(nonce) != 12:
        raise ValueError("Only Support 12 bytes Nonce")
    J0 = nonce + b"\x00\x00\x00\x01"
    print ("[+] J0 : ", b2hex(J0))

    # 3) CTR Encryption
    ciphertext = b""
    block_count = (len(plaintext) + 15) // 16
    for i in range(1, block_count + 1):
        ctr_block = inc32(J0) if i == 1 else inc32(ctr_block)
        S = aes_ecb_enc(key, ctr_block)
        P_block = plaintext[(i-1)*16:i*16]
        C_block = bytes(p ^ s for p, s in zip(P_block, S[:len(P_block)]))
        ciphertext += C_block

        print (f"[+] Counter Block {i} : ", b2hex(ctr_block))
        print (f"[+]        S{i} = E_K(CB{i}) : ", b2hex(S))
        print (f"[+]        P{i} : ", b2hex(P_block))
        print (f"[+]        C{i} : ", b2hex(C_block))
        print ()

    print ("[+] Cipher Text = ", b2hex(ciphertext))
    return ciphertext

if __name__ == "__main__":
    plain = sys.argv[1].encode("utf-8")

    print ("[+] Simple Version")
    aes_gcm_simple(plain)

    print ("[+] Detail Version")
    aes_gcm_debug(plain)
