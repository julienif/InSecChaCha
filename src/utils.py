import os
import array

def gen_32bit_arr(k):
    '''
    Generate an array of length k of random 32-bit unsigned integers

    Args:
        k: length of the array

    Returns:
        An array of length k of 32-bit unsigned integers
    '''

    random_bytes = os.urandom(k*4)
    blocks = array.array('I')
    blocks.frombytes(random_bytes)

    return blocks

def bytes_to_32bit(byte_string):
    '''
    Take some bytes and return an array of 32-bit unsigned integers

    Args:
        byte_string: string of bytes to reduce in blocks

    Returns:
        An array of length len(byte_string)/4 of 32-bit unsigned integers

    Raises:
        AssertionError: if length is not divisble by 4
    '''

    assert len(byte_string) % 4 == 0

    blocks = array.array('I')
    blocks.frombytes(byte_string)

    return blocks

def read_in_chunks(filename, block_size=64):
    '''
    Reads a binary file in fixed-size blocks.

    Opens a file in binary mode and yields fixed-size blocks. If the final block is
    shorter than the block size, it is padded with null bytes (b'\\x00').

    Args:
        filename: Path to the input file.
        block_size: Size of each block in bytes. Defaults to 64.

    Yields:
        bytes: A block of data of length `block_size`.
    '''
    with open(filename, 'rb') as f:
        while chunk := f.read(block_size):
            if len(chunk) < block_size:
                chunk += b'\x00' * (block_size - len(chunk))
            yield chunk



