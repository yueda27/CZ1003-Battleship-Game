from battleship import User, Computer
from authenticate import Authenticator
import sys

class LoginMenu:
    '''First layer of menu user will see.
    Class to display and manage login & create account methods'''
    
    def __init__(self):
        self.choices = {'1': self.login,
                        '2': self.create_account,
                        '3': self.quit}
        #Create an authenticator object to manage creating Users and login
        self.auth = Authenticator()
        
    def display_menu(self):
        '''Display this menu when login is called'''
        print('''
                                                   ,:
                                                 ,' |
                                                /   :
                                             --'   /
                                             \/   />
                                             /  <//
                                          __/   /
                                          )'-. /
                                         ./   //
                                         /.' '
                                         '/' ,
                                         +
                                        '
                                      `.
                                  .-"-
                                 (    |
                              . .-'  '.
                             ( (.   )8:
                         .'    / (_  )
                          _. :(.   )8P  `
                      .  (  `-' (  `.   .
                       .  :  (   .a8a)
                      /_`( "a `a. )"'  '
                  (  (/  .  ' )=='') ` a `
                 (   (    )  .8"   +)) `) ` `
______       _   _   _        _____ _     _         _____  _____  __  _____
| ___ \     | | | | | |      /  ___| |   (_)       / __  \|  _  |/  ||  _  |
| |_/ / __ _| |_| |_| | ___  \ `--.| |__  _ _ __   `' / /'| |/' |`| || |_| |
| ___ \/ _` | __| __| |/ _ \  `--. \ '_ \| | '_ \    / /  |  /| | | ||____ |
| |_/ / (_| | |_| |_| |  __/ /\__/ / | | | | |_) | ./ /___\ |_/ /_| |    | |
\____/ \__,_|\__|\__|_|\___| \____/|_| |_|_| .__/  \_____/ \___/ \___/   |_|
                                           | |
                                           |_| ''') 
           
        print('1. Login\n2. Create new account\n3. Quit')

    def run(self):
        '''Display menu and respond to choices'''
        while True:
            self.display_menu()
            choice = input('Enter your choice: ')
            action = self.choices.get(choice)
            if action:
                action()
            else:
                print('{0} is not a valid choice'.format(choice))
            
    def login(self, username = '', password = ''):
        '''Login method.
        First part is for auto-login after creating account.'''
        if len(username) >= 1:
            self.auth.login(username, password)
            GameMenu(self.auth.users.get(username)).run()
            return
        while True:
            try:
                username = input('Username: ')
                password = input('Password: ')
                if self.auth.login(username, password) == True:
                    GameMenu(self.auth.users.get(username)).run()
                break
            except:
                print('Error logging in')                    
    def quit(self):
        '''Entering this method quits the game'''
        print('Thank you for playing')
        sys.exit(0)
        
    def create_account(self):
        '''Method to create account.
         Asks user to enter username and password . Uses authentication module to check for username and password requirement. 
         self.auth.users holds the list of username and password of all users.'''
         
        while True:
            username = input('Enter your username: ')
            print('\nPassword should be have at least 8 letters\nIt should contain a special character like \'!@#$% etc... \'')
            print('It should contain at least 1 upper and lower case letter, at least 1 digit.\nIt cannot contain username')
            password = input('Enter your password: ')
            if self.auth.add_user(username, password) == True:
                #After signing up, automatically logs in
                print('Account created! Welcome')
                self.login(username, password)
                return
class GameMenu:
    def __init__(self, user):
        self.user = user
        self.computer_opponent = Computer()
    
    def run(self):
        #self.user.game_board.print_board()
        self.computer_opponent.load_ship_auto()  #Automatically load enemy vessels by calling load_ship_auto()
        self.load_ship(self.user)
        self.gameplay()
        
            
    def load_ship(self, player):
        '''Try to load ship checking for overlap. If overlap, Exception is raised.'''
        player.game_board.print_board(hide = False)
        for ship in player.ships:
            while True:
                #While block for x
                while True:
                    try:
                        x = int(input('Enter the x co-ordinates to place your %s:'%ship.name))
                        break
                    except ValueError:
                        print('Please enter a number!')
                #While block for y
                while True:
                    try:    
                        y = int(input('Enter the y co-ordinates to place your %s:'%ship.name))
                        break
                    except ValueError:
                        print('Please enter a number!')
                orientation = input('Enter the orientation of %s (vertical/ horizontal): '%ship.name)
                #Try except catch for error while loading
                try:
                    player.game_board.load_ship(ship, x, y, orientation.lower())
                    player.game_board.print_board(hide = False)
                    break
                except Exception as e:
                    print(e)
        #Update ship map for checking of game status
        player._get_ship_map()
        print('Commander, all your ships have been deployed.\n Ready for war!')
        #player.game_board.print_board(hide = True)
        
    
    def gameplay(self):
        
        def ask_input(location, upper_limit):
            '''Function to try to get valid input'''
            while True:
                try:
                    x = int(input('Enter the {} to attack(1 to {}):'.format(location, upper_limit)))
                    if x < 1 or x > upper_limit:
                        raise Exception('Coordinate exceeded boundary!')
                    break
                except ValueError:
                    print('Please enter a number!')
                except Exception as e:
                    print(e)
            return x
        
        while True:
            #Ask for attack coordinates using ask_input function
            layer = ask_input('layer', self.user.game_board.layers)
            x = ask_input('x-coordinates', self.user.game_board.x_size)
            y = ask_input('y-coordinates', self.user.game_board.y_size)
            #Attacking enemy
            self.user.attack_enemy(self.computer_opponent, [layer, x, y])
            #Check if gain is won by user
            if self.user.point == self.computer_opponent.total_point:
                print('''
                      
    Congratilations, you Win!
                                       |__
                                       |\/
          [[     *********       ]]    |--
          [[ We are proud of you!]]--/ |
          [[ *****         ***** ]]   | ||
                              _/|     _/|-++'
                          +  +--|    |--|--|_ |-
                       { /|__|  |/\__|  |--- |||__/
                      +---------------___[}-_===_.'____                 /
                  ____`-' ||___-{]_| _[}-  |     |_[___\==--            \/   _
   __..._____--==/___]_|__|_____________________________[___\==--____,------' .7
  |                       WINNER WINNER CHICKEN DINNER                        /
   \_________________________________________________________________________|
    wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww
  wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww
     wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww
      ''')
                break
            input('Enemy\'s Turn (Press Enter)')
            self.computer_opponent.auto_attack(self.user)
            #Check if game is won by computer
            if self.computer_opponent.point == self.user.total_point:
                print('''                      
  ______                       _____
 / _____)                     / ___ \\
| /  ___  ____ ____   ____   | |   | |_   _ ____  ____
| | (___)/ _  |    \ / _  )  | |   | | | | / _  )/ ___)
| \____/( ( | | | | ( (/ /   | |___| |\ V ( (/ /| |
 \_____/ \_||_|_|_|_|\____)   \_____/  \_/ \____)_|''')
                break
        
        
        
if __name__ == '__main__':
    LoginMenu().run()