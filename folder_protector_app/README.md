# Folder Protection App

## Description

The Folder Protection App is a simple and secure tool to encrypt and decrypt files in a folder using a password. Keep your files safe with AES encryption!

## Features

- **Encrypt**: Secure all files in a folder with a password.
- **Decrypt**: Access your encrypted files with the correct password.

## Installation

### Prerequisites

- Python 3.x
- Required libraries: `cryptography`, `tkinter`

### Install Libraries

Open a terminal and run: pip install cryptography

### Running the App
Download the Package: Get the package with the scripts and the executable from the dist folder.
Run the Executable: Find folder_protector_app.exe in the dist folder and double-click to run.

### Usage
# Encrypting a Folder:
Open the App.
Enter Password.
Click "Encrypt Folder".
Select Folder to encrypt.
Done: All files in the folder are now encrypted.
# Decrypting a Folder:
Open the App.
Enter Password.
Click "Open Folder".
Select Folder with encrypted files.
Done: All files in the folder are now decrypted.

### Files and Directories
file_encryptor.py: Handles file encryption/decryption.
folder_encryptor.py: Handles folder encryption/decryption.
folder_protector_app.py: Provides the app GUI.
dist/: Contains the executable file folder_protector_app.exe.

### License
This project is licensed under the MIT License. See the LICENSE file for details.

