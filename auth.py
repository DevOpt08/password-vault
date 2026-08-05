from security import verify_password, hash_password

class AuthenticationError(Exception):
    pass

def require_master_password(func):
    def wrapper(*args, **kwargs):
        entered_password = kwargs['entered_password']
        master_hash = kwargs['master_hash']
        if verify_password(entered_password, master_hash):
            return func(*args, **kwargs)
        else:
            raise AuthenticationError('Authentication Failed')
    return wrapper

@require_master_password
def reveal_password(entered_password: str, master_hash: bytes) ->str :
    return 'Sensitive data revealed'

if __name__ == '__main__':
    
    master_hash = hash_password('Haziq_18')
    
    print(reveal_password(entered_password = 'Haziq_18', master_hash = master_hash))
    
    try:
        reveal_password(entered_password = 'haziq_18', master_hash = master_hash)
        
    except AuthenticationError as e:
        print(e)
       
     