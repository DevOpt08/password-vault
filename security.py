import bcrypt

def hash_password(password: str) -> bytes:
    
# --- Byte conversion and salt generation --- #    
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()

# --- Storing Hashed password --- #
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed

def verify_password(entered_password: str, stored_password: bytes) -> bool:
        
    encoded_entered = entered_password.encode('utf-8')
    return bcrypt.checkpw(encoded_entered, stored_password)

    
if __name__ == "__main__":
    
    gmail = hash_password('haziq@123')

    correct = verify_password('haziq@123',gmail)
    incorrect = verify_password('Haziq@12321', gmail)

    print(correct)    
    print(incorrect)    

           
