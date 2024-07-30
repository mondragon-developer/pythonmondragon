import tkinter as tk
from tkinter import filedialog, messagebox
from folderEncryptor import FolderEncryptor
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

class FolderProtectorApp:
    def __init__(self, root):
        """
        Initializes the GUI application.
        Sets up the main window, labels, entry fields, and buttons.
        """
        self.root = root
        self.root.title("Folder Protector")
        self.style = ttk.Style("superhero")

        # Main Frame
        main_frame = ttk.Frame(root, padding=30)
        main_frame.pack(fill=BOTH, expand=True)

        # Password Frame
        password_frame = ttk.Frame(main_frame, padding=(0, 10))
        password_frame.pack(fill=X)
        
        self.password_label = ttk.Label(password_frame, text="Password:")
        self.password_label.pack(side=LEFT, padx=(0, 10))

        self.password_entry = ttk.Entry(password_frame, show="*")
        self.password_entry.pack(side=LEFT, fill=X, expand=True)

        # Button Frame
        button_frame = ttk.Frame(main_frame, padding=(0, 10))
        button_frame.pack(fill=X)

        self.encrypt_button = ttk.Button(button_frame, text="Encrypt Folder", command=self.select_folder_to_encrypt, bootstyle=SUCCESS)
        self.encrypt_button.pack(side=LEFT, fill=X, expand=True, padx=(0, 5))

        self.decrypt_button = ttk.Button(button_frame, text="Open Folder", command=self.select_folder_to_decrypt, bootstyle=PRIMARY)
        self.decrypt_button.pack(side=LEFT, fill=X, expand=True, padx=(5, 0))

        # Info icon with instructions
        self.info_button = ttk.Button(main_frame, text="i", command=self.show_instructions, bootstyle=INFO)
        self.info_button.pack(side=RIGHT, padx=(10, 0))

        self.instructions_label = ttk.Label(main_frame, text="Instructions:", bootstyle=INFO)
        self.instructions_label.pack(side=RIGHT, padx=(5, 10))

    def select_folder_to_encrypt(self):
        """
        Opens a file dialog to select a folder to encrypt.
        Encrypts all files in the selected folder using the provided password.
        """
        folder_path = filedialog.askdirectory()
        if folder_path:
            password = self.password_entry.get()
            if password:
                FolderEncryptor.encrypt_folder(folder_path, password)
                messagebox.showinfo("Success", "Folder encrypted successfully.")
            else:
                messagebox.showerror("Error", "Please enter a password.")

    def select_folder_to_decrypt(self):
        """
        Opens a file dialog to select a folder to decrypt.
        Decrypts all encrypted files in the selected folder using the provided password.
        """
        folder_path = filedialog.askdirectory()
        if folder_path:
            password = self.password_entry.get()
            if password:
                try:
                    FolderEncryptor.decrypt_folder(folder_path, password)
                    messagebox.showinfo("Success", "Folder decrypted successfully.")
                except ValueError as e:
                    messagebox.showerror("Error", str(e))
            else:
                messagebox.showerror("Error", "Please enter a password.")

    def show_instructions(self):
        """
        Show a message box with simple instructions for the user.
        """
        instructions = (
            "1. Enter a password.\n"
            "2. Click 'Encrypt Folder' to encrypt a folder.\n"
            "3. Click 'Open Folder' to decrypt a folder.\n"
            "4. Ensure you use the same password for both encryption and decryption."
        )
        messagebox.showinfo("Instructions", instructions)            

def main():
    """
    Main function to run the GUI application.
    Initializes the main window and starts the event loop.
    """
    root = ttk.Window(themename="superhero")  # Using ttkbootstrap's Window
    app = FolderProtectorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
