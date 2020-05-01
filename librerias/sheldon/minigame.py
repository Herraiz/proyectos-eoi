import random
import time


def player():

    '''Here the player can read the rules of the game and select one of the "moves" for playing '''

    # While bucle for keeping here until the player select a correct move
    finish = False
    while not finish:
        player_choice = input('''
**************************************

Select your choice!

Rock
Paper
Scissors
Lizard
Spock

Type "rules" if you don't know them.

**************************************\n
''').lower()

        if player_choice == "rules":
            print('''
Scissors cuts paper.
Paper covers rock.
Rock crushes lizard.
Lizard poisons Spock.
Spock smashes scissors.
Scissors decapitates lizard.
Lizard eats paper.
Paper disproves Spock.
Spock vaporizes rock.
Rock crushes scissors.

Now... good luck!!

''')
            time.sleep(3)

        elif player_choice in ["rock", "paper", "scissors", "lizard", "spock"]:
            print(f'\n\nYou selected: {player_choice}\n')
            finish = True # bucle finished!
            return player_choice
        else:
            print("\nSorry, your answer is not correct. Please try again.")
            time.sleep(1)

        
def opponent():

    ''' The computer will pick a random move from choices list '''

    print("\nWaiting for your opponent's play...\n")
    time.sleep(1)
    choices = ["rock", "paper", "scissors", "lizard", "spock"]
    opponent_choice = random.choice(choices)
    print(f'\nYour opponent played: {opponent_choice.capitalize()}.\n\n')
    return opponent_choice

def resolution(player_choice, opponent_choice):

    ''' This can be a little tricky. We're using a dictionary: the key will be your move
        and the value is a list with the moves you beat.'''

    time.sleep(1)
    winmoves = {
        "rock": ["scissors", "lizard"],
        "paper": ["rock", "spock"],
        "scissors": ["paper", "lizard"],
        "lizard": ["paper", "spock"],
        "spock": ["scissors", "rock"]
        }

    if player_choice == opponent_choice:
        return print("Draw!\n")

    # Search your choice in the dictionary's keys. Is your oppoment choice on that value list?
    # If positive, you win. If not, you lose.   
    elif opponent_choice in winmoves[player_choice]:
        return print("You win!!\n")
    else:
        return print("You lose!\n")


if __name__ == "__main__":
    print('\nWelcome to the "Rock, Paper, Scissors, Lizard, Spock" game by @RoberHerraiz\n')

    # Bucle for keep playing all the time! :)
    retry_choice = None
    while retry_choice != "q":
        player_move = player()
        opponent_move = opponent()
        resolution(player_move, opponent_move)
        retry_choice = input('\nType "q" for stop or anything else for continue! ').lower()