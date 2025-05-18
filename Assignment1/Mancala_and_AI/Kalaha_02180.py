import sys
import matplotlib.pyplot as plt
import matplotlib.animation as animation

from AI import *

#Players pockets
player_1_pockets = ["A1", "A2", "A3", "A4", "A5", "A6"]
player_2_pockets = ["B1", "B2", "B3", "B4", "B5", "B6"]

pockets = ["B6", "B5", "B4", "B3", "B2", "B1", "Man_2", "Man_1", "A1", "A2", "A3", "A4", "A5", "A6"]


#Number of seeds in beginning of game
start_beeds = 4

# Dict with key = pocket and value = next pocket (counterclockwise)
next_pocket = {'A1': 'A2', 'A2': 'A3', 'A3': 'A4', 'A4': 'A5', 'A5': 'A6', 'A6': 'Man_1',
           'Man_1': 'B1', 'B1': 'B2', 'B2': 'B3', 'B3': 'B4', 'B4': 'B5', 'B5': 'B6',
            'B6': 'Man_2', 'Man_2': 'A1'}

# Dict with key = pocket and value = opposit pocket
opposit_pocket = {'A1': 'B6', 'A2': 'B5', 'A3': 'B4', 'A4': 'B3', 'A5': 'B2',
                   'A6': 'B1', 'B1': 'A6', 'B2': 'A5', 'B3': 'A4', 'B4': 'A3',
                   'B5': 'A2', 'B6': 'A1'}


def main():
    b = start_beeds
    gameBoard = {'A1': b, 'A2': b, 'A3': b, 'A4': b, 'A5': b, 'A6': b, 'Man_1': 0, 
            'B6': b, 'B5': b, 'B4': b, 'B3': b, 'B2': b, 'B1': b, 'Man_2': 0}
    turn = '1' 

    while True:
        BoardViz(gameBoard)

        if turn == '1':
            print("Player 1, it's your turn, choose pocket: A1-A6 (or QUIT)")
            move = input('> ').upper().strip()
        elif turn == '2':
            print("AI is making a move...")
            move = ai_move(gameBoard)
            print("AI chose pocket:", move)

        if move == 'QUIT':
           print('\nThanks for playing!')
           sys.exit()

        if (turn == '1' and move not in player_1_pockets) or (
           turn == '2' and move not in player_2_pockets):
            print('You can only play from your side of the board.')
            continue
            

        while True:
            if gameBoard.get(move) == 0:
                print('\nPick a pocket with beads!')
                move = input('> ').upper().strip()
                continue
            break


        turn = Move(gameBoard, turn, move)

        winner = Winner(gameBoard)
        if winner == '1' or winner == '2':
            BoardViz(gameBoard)  
            print('Congratulations Player ' + winner +', you won the game!')
            sys.exit()
        elif winner == 'tie':
            BoardViz(gameBoard) 
            print('It is a tie')
            sys.exit()


def BoardViz(board):
    Number_of_beeds = []
    for pocket in pockets: 
        numBeedsInThisPocket = str(board[pocket]).rjust(2)
        Number_of_beeds.append(numBeedsInThisPocket)

    print("""  
 _____________________________________________________________
  M       |B6    |B5    |B4    |B3    |B2    |B1    |      M
  A       |  {}  |  {}  |  {}  |  {}  |  {}  |  {}  |      A
  N       |      |      |      |      |      |      |      N
  C   {}  | ----------------------------------------|  {}  C
  A       |A1    |A2    |A3    |A4    |A5    |A6    |      A
  L       |  {}  |  {}  |  {}  |  {}  |  {}  |  {}  |      L 
  A 2     |      |      |      |      |      |      |      A 1
 ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
        
          """.format(*Number_of_beeds))
    

def Move(board, turn, pocket):
   RunningBeeds = board[pocket]  
   board[pocket] = 0  
   
   while RunningBeeds > 0: 
        pocket = next_pocket[pocket]  
        if (turn == '1' and pocket == 'Man_2') or (turn == '2' and pocket == 'Man_1'):
            continue  
        board[pocket] += 1
        RunningBeeds -= 1

   if (pocket == 'Man_1' and turn == '1') or (pocket == 'Man_2' and turn == '2'):
        return turn
   
   if turn == '1' and pocket in player_1_pockets and board[pocket] == 1:
        oppositPocket = opposit_pocket[pocket]
        board['Man_1'] += board[oppositPocket]
        board[oppositPocket] = 0

   elif turn == '2' and pocket in player_2_pockets and board[pocket] == 1:
        oppositPocket = opposit_pocket[pocket]
        board['Man_2'] += board[oppositPocket]
        board[oppositPocket] = 0

   if turn == '1':
        return '2'
   elif turn == '2':
        return '1'
 

def Winner(board):
    player1Beeds = 0
    player2Beeds = 0
    for pocket in player_1_pockets: 
        player1Beeds += board[pocket]
    for pocket in player_2_pockets: 
        player2Beeds += board[pocket]

    if player1Beeds == 0:
        board['Man_2'] += player2Beeds
        for pocket in player_2_pockets:
            board[pocket] = 0  
    elif player2Beeds == 0:
        board['Man_1'] += player1Beeds
        for pocket in player_1_pockets:
            board[pocket] = 0  
    else:
        return 'no winner' 

    if board['Man_1'] > board['Man_2']:
        return '1'
    elif board['Man_2'] > board['Man_1']:
        return '2'
    else:
        return 'tie'



if __name__ == '__main__':
    main()

