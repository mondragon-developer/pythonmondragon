from password_utils import create_and_save_password, PASSWORD_FILE_PATH

def main():
    print(f"Passwords will be saved in: {PASSWORD_FILE_PATH}")
    while True:
        site_and_username = input("Enter the site name and username (or type 'exit' to quit): ")
        if site_and_username.lower() == 'exit':
            break
        try:
            password_length = int(input("Enter the desired password length: "))
        except ValueError:
            print("Please enter a valid number for the password length.")
            continue
        create_and_save_password(site_and_username, password_length)

if __name__ == "__main__":
    main()