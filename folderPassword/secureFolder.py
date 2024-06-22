from encryption_utils import process_folder

# Path to the folder you want to encrypt
folder_path = r"C:\Users\jmond\OneDrive\Escritorio\test_folder"  # Use raw string literal for Windows paths
# Password for encryption
password = '12345'  # Change this to your desired password

# Encrypt the folder
print("Encrypting the folder...")
process_folder(folder_path, password, encrypt=True)
print("Folder encrypted. Check the contents to verify encryption.")


