"""
 Rock Paper Scissors Lizard Spock!
 Joe Deller
 March 2017
 From Big Bang:
 "Scissors cuts paper, paper covers rock, rock crushes lizard,
 lizard poisons Spock, Spock smashes scissors, scissors decapitates lizard,
 lizard eats paper, paper disproves Spock, Spock vaporizes rock,
 and as it always has, rock crushes scissors." 
 """


import random
# Define a set of variables to hold the valid moves
rock     = "Rock"
paper    = "Paper"
scissors = "Scissors"
lizard   = "Lizard"
spock    = "Spock"

# Now store the moves in a list
moves = [rock, paper, scissors, lizard, spock]
# A dictionary of each move and what it beats
winmoves = {rock:[scissors,lizard], paper:[rock,spock], scissors:[paper,lizard], lizard:[paper,spock], spock:[scissors,rock]}


def findwinner(playermove, computermove):
    # Note this does not handle invalid moves
    # So a game that had an invalid player input would declare the computer the winner
    # The moves are also Captital cased, so player input needs to be lower cased then first letter cap

    if playermove == computermove:
        return "Draw!"

    # Find the player move, which will show us what that move beats
    # If the computer move is in that list, players wins, otherwise player loses    
    if computermove in winmoves[playermove]:        
        return "Player wins!"
    
    return "Computer wins!"

maxmove = len(moves) -1

# Play 10 matches to check rules are working
for a in range (10):
    playermove = moves[random.randint(0, maxmove)]
    computermove = moves[random.randint(0, maxmove)]
    result = findwinner(playermove, computermove)
    print ("Round ", a, ":  Computer =",computermove.ljust(10) , " Player =", playermove.ljust(10), " Result:" ,result)