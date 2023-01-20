# A command-line 2048 game

import random
import sys

board: list = []  # a 2-D list to keep current status of the game board


def init() -> None:  # Use as is
    """ 
        initializes the board variable
        and displays the initial board
        and prints a welcome message
    """

    for _ in range(4):     # initialize the board cells with ''
        rowList = []
        for _ in range(4):
            rowList.append('')
        board.append(rowList)

    # add two starting 2's at random cells:
    countOfTwosPlacedAtTheBeginning = 0
    while countOfTwosPlacedAtTheBeginning < 2:
        row = random.randint(0, 3)
        column = random.randint(0, 3)
        if board[row][column] == '':  # if not already taken
            board[row][column] = 2
            countOfTwosPlacedAtTheBeginning += 1

    print()
    print("Welcome! Let's play the 2048 game.")
    print()


def displayGame() -> None:  # Use as is
    """ displays the current board on the console """

    print("+-----+-----+-----+-----+")
    for row in range(4):
        for column in range(4):
            cell = board[row][column]
            print(f"|{str(cell).center(5)}", end="")
        print("|")
        print("+-----+-----+-----+-----+")


def promptGamerForTheNextMove() -> str:  # Use as is
    """
        prompts the gamer to select the next move or Q (to quit)
        valid move direction: one of 'W', 'A', 'S' or 'D'.
        either returns a valid move direction or terminates the game
    """
    print("Enter one of WASD (move direction) or Q (to quit)")
    while True:  # prompt until a valid input is entered
        move = input('> ').upper()
        if move in ('W', 'A', 'S', 'D'):  # a valid move direction
            return move
        if move == 'Q':  # for quit
            print("Exiting the game. Thanks for playing!")
            sys.exit()
        # otherwise inform the user about valid input
        print('Enter one of "W", "A", "S", "D", or "Q"')


def addANewTwoToBoard() -> None:
    """ 
        adds a new 2 at a random available cell
    """

    # flag to deterine whether the cell was placed or not
    placed = False

    while not placed:
        row = random.randint(0, 3)
        column = random.randint(0, 3)
        if board[row][column] == '':  # if not already taken
            board[row][column] = 2

            # switch the flag to exit the loop
            placed = True

    pass


def isFull() -> bool:
    """ returns True if no empty cell is left, False otherwise """

    # this was an original implementation(current implementation line 102)
    # loop through the 2d list
    # for row in range(4):
    #     for column in range(4):
    #         # if null value found
    #         if board[row][column] == "":
    #             return False
    # return True

    # checks whether an "" still contains withing the matrix
    return not any("" in subl for subl in board)
    pass


def getCurrentScore() -> int:
    """ 
        calculates and returns the score
        the score is the sum of all the numbers currently on the board
    """

    # initialize sum
    sum = 0

    # loop through the 2d list
    for row in range(4):
        for column in range(4):
            if board[row][column] != "":
                sum += board[row][column]
    return sum

    # return list(map(sum, board)) #does not work because of the inconsistency within the types

    pass


def updateTheBoardBasedOnTheUserMove(move: str) -> None:
    """
        updates the board variable based on the move argument
        the move argument is either 'W', 'A', 'S', or 'D'
        directions: W for up; A for left; S for down, and D for right
    """

    # copies the content of one 2d array into the other(might be used instead of equating the matrices)
    # global is dropped if this function is used
    # def copy(list1, list2):
    #     for row in range(4):
    #         for column in range(4):
    #             list1[row][column] = list2[row][column]

    # compresses the numbers ignoring ""
    def compress():

        # telling the program that board is the same global board according to(https://vbsreddy1.medium.com/unboundlocalerror-when-the-variable-has-a-value-in-python-e34e097547d6)
        global board

        # creates a list builder 4x4 to work with the actual list board
        builder = [[""] * 4 for i in range(4)]

        for row in range(4):
            pos = 0
            for column in range(4):
                if board[row][column] != "":
                    builder[row][pos] = board[row][column]
                    pos += 1

        # method to creates a shallow copy - be careful using it
        board = builder

        # copy(board, builder)
        # print(board == board1)

    # adds the numbers if they are the same
    def adder():
        for row in range(4):
            for column in range(3):
                if board[row][column] == board[row][column+1] and board[row][column] != "":
                    board[row][column] *= 2
                    board[row][column+1] = ""

    # flip the matrix horizontally over y axis
    def flip():

        # telling the program that board is the same global board according to(https://vbsreddy1.medium.com/unboundlocalerror-when-the-variable-has-a-value-in-python-e34e097547d6)
        global board

        # creates a builder again
        builder = [[""]*4 for _ in range(4)]

        for row in range(4):
            for column in range(4):
                builder[row][column] = (board[row][3-column])

        # copy(board, builder)
        board = builder

    # shift the matrix vertically
    def shift():

        # telling the program that board is the same global board according to(https://vbsreddy1.medium.com/unboundlocalerror-when-the-variable-has-a-value-in-python-e34e097547d6)
        global board

        # creates a builder again
        builder = [[""]*4 for _ in range(4)]

        for row in range(4):
            for column in range(4):
                # reverse the column and row
                builder[column][row] = board[row][column]

        # copy(board, builder)
        board = builder

    # indicate the moves
    if move == "a" or move == "A":
        compress()
        adder()
        compress()

    if move == "d" or move == "D":

        flip()
        compress()
        adder()
        compress()
        flip()

    if move == "w" or move == "W":

        shift()
        compress()
        adder()
        compress()
        shift()

    if move == "s" or move == "S":

        shift()
        flip()
        compress()
        adder()
        compress()
        flip()
        shift()

    pass


if __name__ == "__main__":  # Use as is

    init()  # initialize a game
    while True:  # Super-loop for the game
        displayGame()
        print(f"Score: {getCurrentScore()}")
        updateTheBoardBasedOnTheUserMove(promptGamerForTheNextMove())
        addANewTwoToBoard()

        if isFull():
            displayGame()
            print("Game is Over. Check out your score.")
            print("Thanks for playing!")
            break
