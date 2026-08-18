import sys
from security import hash_password,verify_password
from storage import load_vault, save_vault
from getpass import getpass
from models import PasswordEntry
from authentication import require_master_password, AuthenticationError

# ---- Vault formation when the file runs --- #
def initialize_vault(path: str) -> dict:
    
# ---- Loads an existing vault if present ---- #
    data = load_vault(path)
    
# ---- Password entry for new vault ---- #   
    if data == {}:
        password = getpass("Enter a Password: ")

# ---- Password hashing ---- #
        hashed_pass = hash_password(password)

# ---- Bytes -> Strings ---- #
        hashed_strings = hashed_pass.decode()
        
# ---- User data dictionary ---- #       
        vault ={
            "master_hash": hashed_strings,
            "entries"    : {}
        }

# ---- Saving vault as JSON ---- #      
        save_vault(vault, path)
    
# ---- Returning signals as bool with vault dict for better authenticaion practices later shown in code ---- #    
        return vault, True
    
    else:
        return data, False

def add_entry(vault: dict, path: str) -> None:

# ---- Obtaining paramters from user for entry --- #
    service = input("Enter the name of service: ").lower()

# ---- Service override prevention logic ---- #    
    if service in vault["entries"]:
        user_response = input(f"A {service} entry in the vault already exists. Do you want to overwrite it? y/n: ")
        if user_response.lower() != "y":
            print("Keeping current entry.")
            return
        
    user = input("Enter your username: ")
    password = getpass("Enter your password: ")
    vault["entries"][service] = {"username": user, "password": password}
     
    save_vault(vault, path)

# ---- Displaying existing entries in CLI ---- #    
def list_entry(vault: dict) -> None:
    
    if vault["entries"] == {}:
         print("No entries stored yet!") 
         
    else:
        for service, credentials in vault["entries"].items():
            username = credentials["username"]
            print(f"Service: {service} | Username: {username} | Password: [hidden]")
            

# ---- Decorator for vault's password authentication ---- #
@require_master_password
def reveal_password(service: str, vault: dict, master_hash: bytes, entered_password: str) -> str:
    if service not in vault["entries"]:
        raise KeyError(f"No entry for that service")
    return vault["entries"][service]["password"] 
    
# ---- Main file run ---- #    
if __name__ == "__main__":
    vault, is_new = initialize_vault("new_data.json")
    
# ---- Asking user for the master password in case of pre-existing vault ---- #
    if not is_new:
        entered = getpass("Enter master password: ")
        if not verify_password(entered, vault["master_hash"].encode()):
            sys.exit("Access denied to the vault!")
    
# ---- OPTION MENU ----
    while True:
        print("Select your desried option!")
        print("1) Add")
        print("2) List")
        print("3) Reveal")
        print("4) Quit")
        
        choice = input("Enter your choice: ")
        
        if choice == "1":
            add_entry(vault, "new_data.json")
            
        elif choice == "2":
            list_entry(vault)
            
        elif choice == "3":
            entered_pass = getpass("Enter the vault's password: ")
            service = input("Specify name of the service you want to reveal password for: ").lower()
            
            try:
                password = reveal_password(
                   service=service,
                   vault=vault,
                   master_hash=vault["master_hash"].encode(), 
                   entered_password=entered_pass
                )
                print(f'Password: {password}')
            except AuthenticationError:
                print("Authentication failed - cannot reveal password!")
            except KeyError:
                print("No entry found for that service!")
                
                
        elif choice == "4":
            print("quit choosen")
            break
        else:
            print("Invalid option, try again")
            continue
            