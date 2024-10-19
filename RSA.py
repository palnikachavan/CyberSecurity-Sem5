def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y

def mod_inverse(e, phi):
    gcd, x, y = extended_gcd(e, phi)
    if gcd != 1:
        raise Exception("Modular inverse doesn't exist")
    else:
        return x % phi

def is_prime(num):
    if num <= 1:
        return False
    for i in range(2, int(num ** 0.5) + 1):
        if num % i == 0:
            return False
    return True

def generate_keys():
    p = 11
    q = 3
    n = p * q
    phi = (p - 1) * (q - 1)
    e = 17
    d = mod_inverse(e, phi)
    return (e, n), (d, n)

def encrypt(message, public_key):
    e, n = public_key
    message_bytes = message.encode()
    message_int = int.from_bytes(message_bytes, 'big')
    cipher_int = pow(message_int, e, n)
    return cipher_int

def decrypt(ciphertext, private_key):
    d, n = private_key
    message_int = pow(ciphertext, d, n)
    num_bytes = (message_int.bit_length() + 7) // 8
    decrypted_bytes = message_int.to_bytes(num_bytes, 'big')
    return decrypted_bytes.decode('utf-8', errors='ignore')

if __name__ == "__main__":
    public_key, private_key = generate_keys()
    message = input("Enter Plaintext :")
    print(f"Original Message: {message}")
    print(f"Public Key: {public_key}")
    print(f"Private Key: {private_key}")
    cipher = encrypt(message, public_key)
    print(f"Encrypted Message: {cipher}")
    decrypted_message = decrypt(cipher, private_key)
    print(f"Decrypted Message: {message}")
