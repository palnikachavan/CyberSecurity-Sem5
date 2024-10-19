# Helper functions and tables for DES (same as before)
import random

IP = [58, 50, 42, 34, 26, 18, 10, 2, 60, 52, 44, 36, 28, 20, 12, 4, 62, 54, 46, 38, 30, 22, 14, 6, 
      64, 56, 48, 40, 32, 24, 16, 8, 57, 49, 41, 33, 25, 17, 9, 1, 59, 51, 43, 35, 27, 19, 11, 3, 
      61, 53, 45, 37, 29, 21, 13, 5, 63, 55, 47, 39, 31, 23, 15, 7]
FP = [40, 8, 48, 16, 56, 24, 64, 32, 39, 7, 47, 15, 55, 23, 63, 31, 38, 6, 46, 14, 54, 22, 62, 30, 
      37, 5, 45, 13, 53, 21, 61, 29, 36, 4, 44, 12, 52, 20, 60, 28, 35, 3, 43, 11, 51, 19, 59, 27, 
      34, 2, 42, 10, 50, 18, 58, 26, 33, 1, 41, 9, 49, 17, 57, 25]

E = [32, 1, 2, 3, 4, 5, 4, 5, 6, 7, 8, 9, 8, 9, 10, 11, 12, 13, 12, 13, 14, 15, 16, 17, 16, 17, 18, 19, 
     20, 21, 20, 21, 22, 23, 24, 25, 24, 25, 26, 27, 28, 29, 28, 29, 30, 31, 32, 1]

P = [16, 7, 20, 21, 29, 12, 28, 17, 1, 15, 23, 26, 5, 18, 31, 10, 2, 8, 24, 14, 32, 27, 3, 9, 19, 13, 
     30, 6, 22, 11, 4, 25]

# Simplified S-box for demo purposes
S1 = [[random.randint(0, 15) for _ in range(16)] for _ in range(4)]

# Helper Functions
def string_to_bit_array(text):
    """Convert string into list of bits"""
    array = list()
    for char in text:
        binval = bin(ord(char))[2:].rjust(8, '0')
        array.extend([int(x) for x in list(binval)])
    return array

def bit_array_to_string(array):
    """Convert list of bits back into string"""
    return ''.join([chr(int(''.join(map(str, array[i:i+8])), 2)) for i in range(0, len(array), 8)])

def nsplit(s, n):
    """Split a list into sublists of size n"""
    return [s[k:k+n] for k in range(0, len(s), n)]

def permute(bits, table):
    return [bits[x-1] for x in table]

def xor(bits1, bits2):
    return [b1 ^ b2 for b1, b2 in zip(bits1, bits2)]

def s_box(bits):
    """Substitute using S-box (simplified version for demonstration)"""
    row = (bits[0] << 1) + bits[5]
    col = (bits[1] << 3) + (bits[2] << 2) + (bits[3] << 1) + bits[4]
    return [int(x) for x in format(S1[row][col], '04b')]

def feistel(right, subkey):
    expanded_right = permute(right, E)
    temp = xor(expanded_right, subkey)
    sbox_output = []
    for i in range(0, len(temp), 6):
        sbox_output.extend(s_box(temp[i:i+6]))
    return permute(sbox_output, P)

def des_encrypt(plain_bits, key_bits):
    permuted_text = permute(plain_bits, IP)
    left, right = permuted_text[:32], permuted_text[32:]
    for _ in range(16):
        temp_right = feistel(right, key_bits)
        left, right = right, xor(left, temp_right)
    return permute(left + right, FP)

def des_decrypt(cipher_bits, key_bits):
    permuted_text = permute(cipher_bits, IP)
    left, right = permuted_text[:32], permuted_text[32:]
    for _ in range(16):
        temp_right = feistel(right, key_bits)
        left, right = right, xor(left, temp_right)
    return permute(left + right, FP)

def map_to_printable(cipher_bits):
    """Map bit result to printable ASCII range"""
    result = []
    for i in range(0, len(cipher_bits), 8):
        byte = cipher_bits[i:i+8]
        decimal = int(''.join(map(str, byte)), 2)
        printable_char = chr(32 + decimal % 95)  # ASCII printable range from 32 to 126
        result.append(printable_char)
    return ''.join(result)

# Main Program
if __name__ == "__main__":
    plaintext = input("Enter Plaintext :")
    key = input("Enter Key :")
    
    plain_bits = string_to_bit_array(plaintext)
    key_bits = string_to_bit_array(key)
    
    # Ensure both plaintext and key are 64 bits long (8 chars = 64 bits)
    if len(plain_bits) != 64:
        plain_bits += [0] * (64 - len(plain_bits))
    if len(key_bits) != 64:
        key_bits += [0] * (64 - len(key_bits))
    
    # Encrypt
    encrypted_bits = des_encrypt(plain_bits, key_bits)
    
    # Map to printable characters
    encrypted_text = map_to_printable(encrypted_bits)
    print("Encrypted output:", encrypted_text)
