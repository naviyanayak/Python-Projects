from cryptography.fernet import Fernet 

class PasswordManager:

    def __init__(self):
        self.key = None
        self.password_file = None
        self.password_dict = {}

    def create_key(self, path):
        self.key = Fernet.generate_key()
        with open(path, 'wb') as f:
            f.write(self.key)

    def load_key(self, path):
        with open(path, 'rd') as f:
            self.key = f.read()

    def create_password_file(self, path, initial_value=None):
        self.password_file = path

        if initial_value is not None:
            for key, value in initial_value.items():
                self.add_password(key, value)

    def load_password_file(self, path):
        self.password_file = path

        with open(path, 'r') as f:
            for line in f:
                site, encrypt = line.split(" : ")
                self.password_dict[site] = Fernet(self.key).decrypt(encrypt.encode()).decode()
                
    def add_password (self, site, password):
        self.password_dict[site] = password

        if self.password_file is not None:
            with open(self.password_file, 'a+') as f:
                encrypt = Fernet(self.key).encrypt(password.encode())
                f.write(site + " : " + encrypt.decode() + "\n")

    def get_password (self, site):
        return self.password_dict[site]
    


def main():
    pm = PasswordManager()

    print("""Please select one of the following options:
    1. Create a new key
    2. Load an existing key
    3. Create a new password file
    4. Load an existing password file
    5. Add a new password
    6. Get a password
    7. Quit
    """)

    done = False

    while not done:
      choice = input("Enter your choice: ")
      if choice == "1":
        path = input("Enter path: ")
        pm.create_key(path)
      elif choice == "2":
        path = input("Enter path:")
        pm.load_key(path)
      elif choice == "3":
        path = input("Enter path: ")
        password = {
        "gmail" : "naviya_mail",
        "instagram" : "naviya_insta",
        "snapchat" : "naviya_snap",
        "testweb" : "naviya_test"
        }
        pm.create_password_file(path, password)
      elif choice == "4":
        path = input("Enter path: ")
        pm.load_password_file(path)
      elif choice == "5":
        site = input("Enter the site: ")
        password = input("Enter the password: ")
        pm.add_password(site, password)
      elif choice == "6":
        site = input("Which site do you want? ")
        print(f"Password for {site} is {pm.get_password(site)}")
      elif choice == "7":
        done = True
        print("Bye")
      else:
        print("Invalid Choice!")