import random
import time

def welcome():
    print('\nWelcome to the "Rock, Paper, Scissors, Lizard, Spock" game by @RoberHerraiz\n')

def player():
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
        rules()

    # elif player_choice == "rock" or "paper" or "scissors" or "lizard" or "spock":  #### POR QUÉ NO FUNCIONA SI EL INPUT ES ASDOJIHAJSD????
    #     print(f'\n\nYou selected: {player_choice}\n')
    #     return player_choice

    elif player_choice == "rock":
        print(f'\n\nYou selected {player_choice}\n')
        return player_choice

    elif player_choice == "paper":
        print(f'\n\nYou selected {player_choice}\n')
        return player_choice

    elif player_choice == "scissors":
        print(f'\n\nYou selected {player_choice}\n')
        return player_choice

    elif player_choice == "lizard":
        print(f'\n\nYou selected {player_choice}\n')
        return player_choice

    elif player_choice == "spock":
        print(f'\n\nYou selected {player_choice}\n')
        return player_choice

    else:
        print('\nSorry, your answer is not correct. Please try again.\n')
        return player()

def opponent():
    print("\nWaiting for your opponent's play...\n")
    time.sleep(1)
    choices = ["rock", "paper", "scissors", "lizard", "spock"]
    opponent_choice = random.choice(choices)
    print(f'\nYour opponent played: {opponent_choice.capitalize()}.\n\n')
    return opponent_choice

def resolution(player_choice, opponent_choice):
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
    elif opponent_choice in winmoves[player_choice]:
        return print("You win!!\n")
    else:
        return print("You lose!\n")

def retry():
    retry_choice = input('\nType "y" for playing more! ').lower()
    if retry_choice == "y":
        return main()
    else:
        quit

def rules():
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
    return player()

def main():
    player_move = player()
    opponent_move = opponent()
    resolution(player_move, opponent_move)
    retry()

if __name__ == "__main__":
    welcome()
    main()