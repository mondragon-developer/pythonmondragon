import random
import string
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Define the path for the password file
PASSWORD_FILE_PATH = os.getenv("PASSWORD_FILE_PATH")

# Function to generate a random password
def generate_password(length=20):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(length))
    return password

# Function to save the password to a file
def save_password(site_and_username, password, file_path):
    with open(file_path, 'a') as file:
        file.write(f"{site_and_username}: {password}\n")

# Function to create and save a password for a site
def create_and_save_password(site_and_username, length=20, file_path=PASSWORD_FILE_PATH):
    password = generate_password(length)
    save_password(site_and_username, password, file_path)
    print(f"Password for {site_and_username} saved successfully.")
