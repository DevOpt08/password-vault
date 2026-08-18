# ---- Written while learning OOP ---- #
class PasswordEntry:
    
    def __init__(self, service: str, username: str, password: str) -> None:
        self.service = service
        self.username = username
        self.password = password
    
    def describe(self) -> str:
        return f'Service: {self.service} | User: {self.username} | Password: Set!'
    
    def get_password(self) -> str:
        return self.password
    
if __name__ == "__main__":
    
    rockstar_entry = PasswordEntry('Rockstar Games', 'Haziq.12', 'ali_12345')
    print(rockstar_entry.describe())
