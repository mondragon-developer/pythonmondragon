from cryptography.fernet import Fernet

# Generate an encryption key
key = Fernet.generate_key()

# Save the generated key to a file (simulating secure sharing with Person B)
with open("secret.key", "wb") as key_file:
    key_file.write(key)

# Create a Fernet cipher suite using the generated key
cipher_suite = Fernet(key)

# Message to encrypt
message = b"my bank account is 123456789"

# Encrypt the message
cipher_text = cipher_suite.encrypt(message)
print(f"Encrypted message: {cipher_text}")


