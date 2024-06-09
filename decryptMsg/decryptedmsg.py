from cryptography.fernet import Fernet

# Load the key (assuming Person B received it securely from Person A)
with open("secret.key", "rb") as key_file:
    key = key_file.read()

# Create a Fernet cipher suite using the loaded key
cipher_suite = Fernet(key)

# Encrypted message received from Person A
cipher_text = b"gAAAAABmXm3MKFm4BHn2MtTEhrYiBCM_6jcYTrNhteKLWlixcUm_gtaHNZ7AvuBndJgPqJPsBYNf7Gp92iC4NqSN_KSWb6X-OiOaaKF4lthSLZbvcOYx1RU="

# Decrypt the message
decrypted_message = cipher_suite.decrypt(cipher_text)
print(f"Decrypted message: {decrypted_message.decode()}")
