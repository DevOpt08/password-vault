import json

class CorruptVaultError(Exception):
    pass

def save_vault(vault: dict, path: str) -> None:
    with open(path, 'w') as f:
        json.dump(vault, f)
        
def load_vault(path: str) -> dict:
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
           return {}
    except json.JSONDecodeError:
        raise CorruptVaultError(f'The contents of file {path} contain invalid JSON')
        
if __name__ == "__main__":
    
    test_dict = {
        'service' : 'Rockstar Games',
       'username' : 'haziq.18',
       'password' : 'set'
    }
    
    save_vault(test_dict, 'valid.json')
    print('Correct File:', load_vault('valid.json')) 
    
    print("Missing File", load_vault('not_exist.json'))
    
    try:
        load_vault('data.json')
    except CorruptVaultError as e:
        print("Corrupt File Identified:", e)
    
    print("End of the Script!")