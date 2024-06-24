Instructions:

Ensure you have the following files in your project directory:

password_utils.py (contains the logic for generating and saving passwords)
addPassword.py (the main script to run)


Create a .env file in the same directory with the following content:
PASSWORD_FILE_PATH=your/path/to/passwords.txt
Replace 'your/path/to/passwords.txt' with the actual path where you want to save the passwords.

Install the required dependencies:
pip install python-dotenv

Navigate to the directory containing password_utils.py and addPassword.py in your terminal or command prompt.
Execute the addPassword.py script using the following command:
python addPassword.py

The script will:
Display the path where passwords will be saved.
Prompt you to enter the site name.
Prompt you to enter the desired password length.
Generate a password, save it to the specified file, and display a success message.


You can repeat the process for multiple sites or type 'exit' to quit the program.
Create a .gitignore file in your project root directory and add the following lines:
__pycache__/
*.pyc
.env

NOTE: For added security, you can use this script in combination with the folderPassword scripts to encrypt the folder containing your passwords.txt file after you've finished saving passwords.