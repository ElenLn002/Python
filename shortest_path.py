'''
from collections import deque

def printGameBoard(board):
    for r, row in enumerate(board):
        for c, cell in enumerate(row):
            cellValue = ' ' if cell == '-' else cell
            print(f' {cellValue} |', end='')
        print()
        if r < len(board) - 1:
            print('----' * len(row) + '----')

def getBoardInput():
    board = []
    line_length = None
    while True:
        line = input("Enter line/stop: ").strip()
        if line.lower() == 'stop':
            break
        if not all(c in 'bx-' for c in line):
            print("Error: Invalid input. Only 'b', 'x', or '-'.")
            continue
        if line_length is None:
            line_length = len(line)
        elif len(line) != line_length:
            print(f"Error: Line length is {line_length}.")
            continue
        board.append(list(line))
    return board


def get_points(board):
    points = []
    while len(points) < 2:
        try:
            row = int(input(f"Row index {len(points) + 1}: ")) - 1
            col = int(input(f"Column index {len(points) + 1}: ")) - 1
            if row < 0 or col < 0 or row >= len(board) or col >= len(board[0]):
                print("Error: The coords are out of bounds. Try again.")
                continue
            if board[row][col] != 'x':
                print("Error: The cell does'nt contain x. Try again.")
                continue
            points.append((row, col))
        except ValueError:
            print("Error: Invalid input. Numerical values only.")
    return points

def bfs(board, start, dest):
    validDirects = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    queue = deque([(start, [start])])
    visited = set([start])
    
    while queue:
        (currentRow, currentColumn), path = queue.popleft()
        print(f"Current position: ({currentRow}, {currentColumn}), Path: {path}")
        
        # Print queue and visited sets after each iteration
        print("Queue:", list(queue))
        print("Visited:", visited)
        
        if (currentRow, currentColumn) == dest:
            return path
        
        for direct in validDirects:
            neighborRow = currentRow + direct[0]
            neighborColumn = currentColumn + direct[1]
            if 0 <= neighborRow < len(board) and 0 <= neighborColumn < len(board[0]) and (board[neighborRow][neighborColumn] == '-' 
                                      or board[neighborRow][neighborColumn] == 'x') and (neighborRow, neighborColumn) not in visited:

                visited.add((neighborRow, neighborColumn))
                queue.append(((neighborRow, neighborColumn), path + [(neighborRow, neighborColumn)]))
    
    return None


def drawPath(board, path):
    for row, col in path:
        board[row][col] = '*'
        
    return board

def main():
    board = getBoardInput()
    print("\nGame Board:")
    printGameBoard(board)
    
    points = get_points(board)
    startPoint, endPoint = points
    
    shortest_path = bfs(board, startPoint, endPoint)
    
    if shortest_path:
        drawPath(board, shortest_path)
        
        print("\nShortest Path:")
        printGameBoard(board)
       
    else:
        print("\nNo path found.")

if __name__ == '__main__':
    main()
    '''

import os

class UltimateTicTacToe:
    def __init__(self):
        self.board = [[' ']*9 for _ in range(9)]
        self.currentPlayer = 'X'
        self.winner = None
        self.gameOver = False
        self.nextSmallSquare = None

    def printBoard(self):
        # Clear the console (this might not work in some environments)
        os.system('cls' if os.name == 'nt' else 'clear')
        self.printIndices()
        for i in range(9):
            if i % 3 == 0 and i != 0:
                print('-' * 21)
            for j in range(9):
                if j % 3 == 0 and j != 0:
                    print('|', end=' ')
                print(self.board[i][j], end=' ')
            print()

    def printIndices(self):
        print("1 2 3   1 2 3   1 2 3")

    def checkWinner(self):
        # Check rows and columns in big board
        for i in range(0, 9, 3):
            for j in range(0, 9, 3):
                sub_board = [self.board[i + k][j:j + 3] for k in range(3)]
                # Check rows and columns in small square
                for k in range(3):
                    if all([self.board[i + k][j + m] == self.currentPlayer for m in range(3)]):
                        self.winner = self.currentPlayer
                        return True
                    if all([self.board[i + m][j + k] == self.currentPlayer for m in range(3)]):
                        self.winner = self.currentPlayer
                        return True
                # Check diagonals in small square
                if all([self.board[i + k][j + k] == self.currentPlayer for k in range(3)]):
                    self.winner = self.currentPlayer
                    return True
                if all([self.board[i + k][j + 2 - k] == self.currentPlayer for k in range(3)]):
                    self.winner = self.currentPlayer
                    return True

        # Check rows and columns in big board
        for i in range(9):
            # Check rows
            if all([self.board[i][j] == self.currentPlayer for j in range(9)]):
                self.winner = self.currentPlayer
                return True
            # Check columns
            if all([self.board[j][i] == self.currentPlayer for j in range(9)]):
                self.winner = self.currentPlayer
                return True

        # Check diagonals in big board
        if all([self.board[i][i] == self.currentPlayer for i in range(9)]):
            self.winner = self.currentPlayer
            return True
        if all([self.board[i][8 - i] == self.currentPlayer for i in range(9)]):
            self.winner = self.currentPlayer
            return True

        return False

    def makeMove(self, bigRow, bigCol, smallRow, smallCol):
        if self.gameOver:
            print("Game Over!")
            return

        # Calculate actual board indices
        bigRow = bigRow * 3
        bigCol = bigCol * 3
        actualRow = bigRow + smallRow
        actualCol = bigCol + smallCol

        # Check if the cell is already occupied
        if self.board[actualRow][actualCol] != ' ':
            print("Invalid move! Square is already occupied.")
            return

        # Make the move
        self.board[actualRow][actualCol] = self.currentPlayer

        # Check if the move results in a win
        if self.checkWinner():
            self.gameOver = True

        # Switch players
        if self.currentPlayer == 'X':
            self.currentPlayer = 'O'
        else:
            self.currentPlayer = 'X'

    def play(self):
        while not self.gameOver:
            self.printBoard()
            print("Player", self.currentPlayer, "turn.")

            if self.nextSmallSquare is None:  # First move
                bigRow, bigCol = self.get_big_square_input()
                smallRow, smallCol = self.get_small_square_input()
            else:  # Subsequent moves
                print(f"Player must play in small square at ({self.nextSmallSquare[0] + 1}, {self.nextSmallSquare[1] + 1}).")
                smallRow, smallCol = self.get_small_square_input()
                bigRow, bigCol = self.nextSmallSquare

            self.makeMove(bigRow, bigCol, smallRow, smallCol)
            
            # If the game is not over, update the nextSmallSquare
            if not self.gameOver:
                self.nextSmallSquare = (smallRow, smallCol)

        self.printBoard()
        if self.winner:
            print("Player", self.winner, "wins!")
        else:
            print("It's a tie!")

    def get_big_square_input(self):
        while True:
            try:
                bigRow = int(input("Enter big row (1-3): ").strip()) - 1
                bigCol = int(input("Enter big col (1-3): ").strip()) - 1
                if bigRow not in range(3) or bigCol not in range(3):
                    raise ValueError("Invalid input. Indices must be between 1 and 3.")
                return bigRow, bigCol
            except ValueError as e:
                print("Invalid input:", e)

    def get_small_square_input(self):
        while True:
            try:
                smallRow = int(input("Enter small row (1-3): ").strip()) - 1
                smallCol = int(input("Enter small col (1-3): ").strip()) - 1
                if smallRow not in range(3) or smallCol not in range(3):
                    raise ValueError("Invalid input. Indices must be between 1 and 3.")
                return smallRow, smallCol
            except ValueError as e:
                print("Invalid input:", e)


# Create a game instance and start the game
game = UltimateTicTacToe()
game.play()
