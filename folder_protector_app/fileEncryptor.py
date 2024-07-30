import os
import ctypes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import shutil

class FileEncryptor:
    @staticmethod
    def derive_key(password, salt):
        """
        Derives a cryptographic key from a password and salt using PBKDF2HMAC with SHA-256.
        This ensures that the same password will generate different keys when used with different salts.
        """
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        return kdf.derive(password.encode())

    @staticmethod
    def ensure_writable(file_path):
        """
        Ensures the file is writable by modifying its attributes.
        """
        if os.name == 'nt':
            ctypes.windll.kernel32.SetFileAttributesW(file_path, 0)  # 0 to reset all attributes
        else:
           os.chmod(file_path, 0o644)  # Restore write permissions
       
    @staticmethod
    def set_read_only(file_path):
        """
        Sets the file attribute to read-only.
        """
        if os.name == 'nt':
                ctypes.windll.kernel32.SetFileAttributesW(file_path, 1)  # 1 is the attribute value for read-only files
        else:
            os.chmod(file_path, 0o444)  # Read-only for all users
        
    @staticmethod
    def encrypt_file(file_path, password):
        """
        Encrypts a file using AES encryption with a password-derived key.
        The encrypted file is saved with a .enc extension, and the original file is deleted.
        """
        try:
            FileEncryptor.ensure_writable(file_path)
            salt = os.urandom(16)  # Generate a random salt for key derivation
            key = FileEncryptor.derive_key(password, salt)  # Derive the encryption key
            iv = os.urandom(16)  # Generate a random initialization vector (IV)
            cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
            encryptor = cipher.encryptor()

            with open(file_path, 'rb') as f:
                data = f.read()  # Read the original file content

            encrypted_data = encryptor.update(data) + encryptor.finalize()  # Encrypt the data

            # Write the salt, IV, and encrypted data to a new file with .enc extension
            encrypted_file_path = file_path + '.enc'
            with open(encrypted_file_path, 'wb') as f:
                f.write(salt + iv + encrypted_data)

            # Only remove the original file if encryption was successful
            if os.path.exists(encrypted_file_path):
                os.remove(file_path)  # Remove the original unencrypted file
                FileEncryptor.set_read_only(encrypted_file_path)  # Set the encrypted file to read-only
            
        except Exception:
            pass

    @staticmethod
    def decrypt_file(file_path, password):
        """
        Decrypts an encrypted file using AES decryption with a password-derived key.
        The decrypted file is saved without the .enc extension, and the encrypted file is deleted.
        Raises an exception if the decryption fails.
        """
        try:
            FileEncryptor.ensure_writable(file_path)

            with open(file_path, 'rb') as f:
                data = f.read()  # Read the encrypted file content

            salt = data[:16]  # Extract the salt from the file
            iv = data[16:32]  # Extract the IV from the file
            encrypted_data = data[32:]  # The rest is the encrypted data

            key = FileEncryptor.derive_key(password, salt)  # Derive the decryption key
            cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
            decryptor = cipher.decryptor()

            decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()  # Decrypt the data

            # Only write the decrypted data to the file if decryption was successful
            decrypted_file_path = file_path[:-4]  # Remove .enc extension from the file name
            with open(decrypted_file_path, 'wb') as f:
                f.write(decrypted_data)

            # Only remove the encrypted file if decryption was successful
            if os.path.exists(decrypted_file_path):
                os.remove(file_path)  # Remove the encrypted file
        except Exception:
            raise ValueError("Invalid password or corrupted file")

    @staticmethod
    def save_password(password, folder_path):
        """
        Saves the password to an encrypted file in the folder path for later verification.
        """
        password_path = os.path.join(folder_path, 'password.txt')
        try:
            with open(password_path, 'w') as f:
                f.write(password)
            FileEncryptor.encrypt_file(password_path, password)
        except Exception :
            pass

    @staticmethod
    def validate_password(password, folder_path):
        """
        Validates the provided password against the saved password.
        """
        encrypted_password_path = os.path.join(folder_path, 'password.txt.enc')
        backup_encrypted_password_path = os.path.join(folder_path, 'password_backup.txt.enc')

        if not os.path.exists(encrypted_password_path):
            raise FileNotFoundError("Encrypted password file not found")

        # Create a backup of the encrypted password file
        shutil.copyfile(encrypted_password_path, backup_encrypted_password_path)

        # Path to the temporary decrypted password file
        decrypted_password_path = encrypted_password_path[:-4]  # Remove .enc extension from the file name

        # Attempt to decrypt the password file
        try:
            FileEncryptor.decrypt_file(encrypted_password_path, password)
        except ValueError as e:
            # Ensure the decrypted password file is removed if it exists
            if os.path.exists(decrypted_password_path):
                os.remove(decrypted_password_path)
            # Restore the backup to the original encrypted password file name
            os.rename(backup_encrypted_password_path, encrypted_password_path)
            raise ValueError("Invalid password")

        # Read the decrypted password file
        try:
            with open(decrypted_password_path, 'r') as f:
                saved_password = f.read()
        except Exception as e:
            # Ensure the decrypted password file is removed if it exists
            if os.path.exists(decrypted_password_path):
                os.remove(decrypted_password_path)
            # Restore the backup to the original encrypted password file name
            os.rename(backup_encrypted_password_path, encrypted_password_path)
            raise ValueError("Could not read decrypted password file")

        # Compare the provided password with the saved password
        if password != saved_password:
            # Ensure the decrypted password file is removed if it exists
            if os.path.exists(decrypted_password_path):
                os.remove(decrypted_password_path)
            # Restore the backup to the original encrypted password file name
            os.rename(backup_encrypted_password_path, encrypted_password_path)
            raise ValueError("Invalid password")

        # Remove the backup file after successful password validation
            os.remove(backup_encrypted_password_path)  # Remove the backup file
       
        # Remove the decrypted password file after successful password validation
            os.remove(decrypted_password_path)  # Remove the decrypted password file