from ChaChaBlock import ChaChaBlock
import utils

BLOCK_SIZE = 64 # 512 bits = 64 bytes
NONCE_SIZE = 3 # 3 * 32 bits = 12 bytes

nonce = utils.gen_32bit_arr(3)

with open('../key/very_secret_key.bin') as f:
    key_bytes = f.read().encode('ascii')

key = utils.bytes_to_32bit(key_bytes)

chacha_alice = ChaChaBlock(key, nonce)
chacha_bob = ChaChaBlock(key, nonce)

chacha_alice.encrypt_plaintext()

chacha_bob.decrypt_ciphertext()
