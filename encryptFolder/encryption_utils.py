import os
import base64
import hashlib
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes

# Function to derive a key from a password and salt
def derive_key(password, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    return kdf.derive(password.encode())

# Encrypt or decrypt a file
def process_file(file_path, key, encrypt=True):
    with open(file_path, 'rb') as f:
        data = f.read()
    iv = os.urandom(16)  # Initialization vector for encryption
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    cryptor = cipher.encryptor() if encrypt else cipher.decryptor()
    if encrypt:
        processed_data = iv + cryptor.update(data) + cryptor.finalize()
    else:
        iv = data[:16]  # Extract the IV from the beginning of the file
        data = data[16:]  # The rest is the actual encrypted data
        cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
        cryptor = cipher.decryptor()
        processed_data = cryptor.update(data) + cryptor.finalize()
    with open(file_path, 'wb') as f:
        f.write(processed_data)

# Encrypt or decrypt all files in a folder
def process_folder(folder_path, password, encrypt=True):
    salt_path = os.path.join(folder_path, 'salt')  # Path to save the salt
    salt = os.urandom(16) if encrypt else open(salt_path, 'rb').read()
    key = derive_key(password, salt)  # Derive key from password and salt
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file == 'salt': continue  # Skip the salt file
            process_file(os.path.join(root, file), key, encrypt)
    if encrypt:
        with open(salt_path, 'wb') as f:
            f.write(salt)  # Save the salt for decryption
    print(f"{'Encrypted' if encrypt else 'Decrypted'} all files in {folder_path}")
