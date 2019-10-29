from battleship import User


class AuthException(Exception):
    def __init__(self, username, user = None):
        super().__init__(username, user)
        self.username = username
        self.user = user
class UsernameAlreadyExist(AuthException):
    print('Hello')
    pass
class PasswordTooShort(AuthException):
    pass
class InvalidUsername(AuthException):
    pass
class InvalidPassword(AuthException):
    pass
class PermissionError(AuthException):
    pass
class NotLoggedInError(AuthException):
    pass
class NotPermittedError(AuthException):
    pass
class ContainUsernameError(AuthException):
    pass
class NoSpecialCharacterError(AuthException):
    pass


class Authenticator:
    '''Authenticator holds a list of usernames and password to be checked during login'''
    def __init__(self):
        self.users = {'user1': User('user1', 'password')}
    
    def add_user(self, username, password):
        SpecialSym =['$', '@', '#', '%','ˆ','&','*', ')']
        if username in self.users:
            print('Username already in use')
            return False
        if len(password) < 8:
            print('Password is too short')
            return False
        
        if not any(char in SpecialSym for char in password):
            print('Password does not contain special character')
            return False
            
        if not any(char.isdigit() for char in password): 
            print('Password should have at least one numeral') 
            return False
          
        if not any(char.isupper() for char in password): 
            print('Password should have at least one uppercase letter')
            return False
        if username in password:
            print('Password contains username')
            return False

        if not any(char.islower() for char in password): 
            print('Password should have at least one lowercase letter')
            return False
            
        
        self.users[username] = User(username, password)
        return True
    
    def login(self, username, password):
        try:
            user = self.users[username]
        except KeyError:
            print('Username not found.')
            return False
        
        if not user.check_password(password):
            print('Password is wrong.')
            return False
        
        user.is_logged_in = True
        print('Welcome',username)
        print('''
              _____________________________________________
                      Entering into battle area...
              _____________________________________________
           |        |
         |-|-|      |
           |        |
           | {O}    |
           '--|     |
             .|]_   |
       _.-=.' |     |
      |    |  |]_   |
      |_.-='  |   __|__
       _.-='  |\   /|\\
      |    |  |-'-'-'-'-.
      |_.-='  '========='
           `   |     |
            `. |    / \\
              ||   /   \____.
              ||_.'--=='    |       //  //   / /
              ||  |    |    |\\    //  //   / /                      ___
 ____         ||__|____|____| \||_/ |_/ |__/  \ __________________/|   |
|    |______  |===.---. .---.========''=-./// |     |     |     / |   |
|    ||     |\| |||   | |   |      '===' ||  \|_____|_____|____/__|___|
|-.._||_____|_\___'---' '---'______....---===''======//=//////========|
|--------------\------------------/-----------------//-//////---------/
|               \                /                 // //////         /
|                \______________/                 // //////         /
|                                        _____===//=//////=========/
|==============================================================   /
'----------------------------------------------------------------`
            Remember, you just need to provide row and colum number
            as coordinate for your missle to hit the hidden aship.              
              ''')
        input('Press ENTER to continue.....')
        return True
    
    def is_logged_in(self, username):
        if username in self.users:
            return self.users[username].is_logged_in
        return False
            