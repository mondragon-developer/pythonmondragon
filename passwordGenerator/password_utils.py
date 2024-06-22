import random
import string

# Define the path for the password file
PASSWORD_FILE_PATH = r"C:\Users\jmond\OneDrive\Escritorio\test_folder\passwords.txt"

# Function to generate a random password
def generate_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(length))
    return password

# Function to save the password to a file
def save_password(site_name, password, file_path):
    with open(file_path, 'a') as file:
        file.write(f"{site_name}: {password}\n")

# Function to create and save a password for a site
def create_and_save_password(site_name, length=12, file_path=PASSWORD_FILE_PATH):
    password = generate_password(length)
    save_password(site_name, password, file_path)
    print(f"Password for {site_name} saved successfully.")
