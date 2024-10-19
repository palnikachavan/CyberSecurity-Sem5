import hashlib

def sha1_hash(data):
    sha1 = hashlib.sha1()
    sha1.update(data.encode('utf-8'))
    return sha1.hexdigest()

if __name__ == "__main__":
    input_data = input("Enter the data to hash using SHA-1: ")
    print(f"SHA-1 hash of '{input_data}': {sha1_hash(input_data)}")
