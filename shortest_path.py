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
    
