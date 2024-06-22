from encryption_utils import process_folder

# Path to the folder you want to decrypt
folder_path = r"C:\Users\jmond\OneDrive\Escritorio\test_folder"  # Use raw string literal for Windows paths
# Password for decryption
password = '12345'  # Change this to your desired password

# Decrypt the folder
print("Decrypting the folder...")
process_folder(folder_path, password, encrypt=False)
print("Folder decrypted. Check the contents to verify decryption.")


