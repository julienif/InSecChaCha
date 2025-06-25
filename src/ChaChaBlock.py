import array
import utils
import time

class ChaChaBlock:
    '''
    A class representing one block of the ChaCha algorithm

    Attributes:
        cons: constant string for the block encoded in ASCII
        rounds: Number of rounds while shuffling the block
    '''

    cons = "expand 32-byte k"
    rounds = 20

    def __init__(self, key, nonce):
        '''
        Constructor for a block of the ChaCha algorithm.
        Initialize with counter equals to 0 and some nonces.

        Args:
            key: unsigned 32-bit integers array of length 16 (512 bits)
            nonce: unsigned 96-bit integers
        '''

        self.counter = 0
        self.__key = key
        self.nonce = nonce
        self.cons_blocks = utils.bytes_to_32bit(self.cons.encode('ascii'))

        self.__block = self._construct_block()
        
        self.keystream = self.__block[:]

    def next_keystream(self):
        '''
        Create the next keystream by incrementing the counter
        '''
        self.counter += 1

        self._construct_block()
        self._create_keystream()
        
    def encrypt_plaintext(self, input_path='../res/lorem_ipsum.txt', output_path='../res/ciphertext.bin'):
        '''
        Encrypt the text at input_path and output the ciphertext at output_path

        Args:
            input_path: Path to the file to encrypt 
            output_path: Path to the ciphertext
        '''
        
        print("Encrypting...\n")
        time.sleep(1)
        self._print_keystream(init=True)
        time.sleep(2)
        self._create_keystream()
        with open(output_path, 'wb') as f:
            for chunk in utils.read_in_chunks(input_path):
                keystream = self.keystream.tobytes()
                self._print_keystream()
                ciphertext = bytes([a ^ b for a, b in zip(chunk, keystream)])
                f.write(ciphertext)
                self.next_keystream()
                time.sleep(0.5)
        print("Plaintext encrypted at: " + output_path + "\n")

    def decrypt_ciphertext(self, input_path='../res/ciphertext.bin', output_path='../res/plaintext.txt'):
        '''
        Decrypt the text at input_path and output the plaintext at output_path

        Args:
            input_path: Path to the file to decrypt 
            output_path: Path to the plaintext decrypted
        '''

        print("Decrypting...\n")
        time.sleep(1)

        self._print_keystream(init=True)
        time.sleep(2)
        self._create_keystream()
        with open(output_path, 'wb') as f:
            for chunk in utils.read_in_chunks(input_path):
                keystream = self.keystream.tobytes()
                self._print_keystream()
                plaintext = bytes([a ^ b for a, b in zip(chunk, keystream)])
                f.write(plaintext)
                self.next_keystream()
                time.sleep(0.5)
        print("Ciphertext decrypted at: " + output_path)

    def _construct_block(self):
        '''
        Construct the block from the the constant string, the key,
        the counter and the nonces.

        Returns:
            4x4 block with 32-bit unsigned integers elements

        Raises:
            AssertionError if the components do not have the right length
        '''
        assert len(self.cons_blocks) == 4
        assert len(self.__key) == 8
        assert len(self.nonce) == 3

        block = array.array('I', [0] * 16)

        block[:4] = self.cons_blocks
        block[4:12] = self.__key
        block[12] = self.counter
        block[13:] = self.nonce

        return block

    def _print_keystream(self, init=False):
        '''
        print the current keystream in the terminal in ascii encoding
        '''
        
        if not init:
            print("     -----Keystream number " + str(self.counter) + "-----")
        else:
            print("     -----Initial Block-----")

        for i in range(0, len(self.keystream), 4):
            line = ' '.join(f"{elem:<10x}" for elem in self.keystream[i:i+4])
            print(line)
        
        print("\n")
        
    def _rotate(self, x, k):
        '''
        rotate the bitstring x to the left by k positions

        Args:
            x: Input bitstring
            k: Number of bits to rotate
        
        Returns:
            New bitstring rotated by k
        '''
        return ((x << k) & 0xffffffff) | (x >> (32 - k))


    def _quarter_round(self, ai, bi, ci, di):
        '''
        One quarter round with given indices for the block

        Args:
            a, b, c, d: indices in the block
        '''
        a = self.keystream[ai]
        b = self.keystream[bi]
        c = self.keystream[ci]
        d = self.keystream[di]

        a = (a + b) & 0xffffffff
        d ^= a
        d = self._rotate(d, 16)

        c = (c + d) & 0xffffffff
        b ^= c
        b = self._rotate(b, 12)

        a = (a + b) & 0xffffffff
        d ^= a
        d = self._rotate(d, 8)

        c = (c + d) & 0xffffffff
        b ^= c
        b = self._rotate(b, 7)

        self.keystream[ai] = a
        self.keystream[bi] = b
        self.keystream[ci] = c
        self.keystream[di] = d

    def _shuffle_block(self):
        '''
        Shuffles the block pre-constructed according
        to the ChaCha20 algorithm
        '''
        for i in range(1, self.rounds + 1):
            if i % 2 == 1: # odd round (column)
                self._quarter_round(0, 4, 8, 12)
                self._quarter_round(1, 5, 9, 13)
                self._quarter_round(2, 6, 10, 14)
                self._quarter_round(3, 7, 11, 15)
            if i % 2 == 0: # even round (diagonal)
                self._quarter_round(0, 5, 10, 15)
                self._quarter_round(1, 6, 11, 12)
                self._quarter_round(2, 7, 8, 13)
                self._quarter_round(3, 4, 9, 14)

    def _create_keystream(self):
        '''
        Create the keystream based on the block created
        '''
        self._shuffle_block()

        for i in range(len(self.keystream)):
            self.keystream[i] = (self.keystream[i] + self.__block[i]) & 0xffffffff
