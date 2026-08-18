from security import verify_password, hash_password

# ---- Custom exception for handling authentication errors ---- #
class AuthenticationError(Exception):
    pass

# ---- Raw decorator for checking password ---- #
def require_master_password(func):
    def wrapper(*args, **kwargs):
        entered_password = kwargs['entered_password']
        master_hash = kwargs['master_hash']
        if verify_password(entered_password, master_hash):
            return func(*args, **kwargs)
        else:
            raise AuthenticationError('Authentication Failed')
    return wrapper

# ---- Testing the decorator works ---- #
if __name__ == "__main__":
    master_hash = hash_password('Haziq_18')

    @require_master_password
    def _demo(**kwargs) -> str:
        return "gate opened"

    # correct password → gate opens
    print(_demo(entered_password='Haziq_18', master_hash=master_hash))

    # wrong password → AuthenticationError
    try:
        _demo(entered_password='wrong', master_hash=master_hash)
    except AuthenticationError as e:
        print("Rejected:", e)
       
     