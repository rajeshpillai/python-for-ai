def print_board(board):
    print("\n")
    for row in board:
        print(" | ".join(row))
        print("-" * 9)
    print("\n")

def check_winner(board, player):
    # Check rows, columns, and diagonals
    for i in range(3):
        if all([cell == player for cell in board[i]]):  # Check rows
            return True
        if all([board[j][i] == player for j in range(3)]):  # Check columns
            return True
    if board[0][0] == board[1][1] == board[2][2] == player:  # Check diagonal
        return True
    if board[0][2] == board[1][1] == board[2][0] == player:  # Check other diagonal
        return True
    return False

def is_draw(board):
    return all([cell != " " for row in board for cell in row])

def play_game():
    board = [[" " for _ in range(3)] for _ in range(3)]
    players = ["X", "O"]
    current_player = 0

    while True:
        print_board(board)
        print(f"Player {players[current_player]}'s turn")

        # Input and validation
        try:
            index = int(input("Enter a position (0-8): "))
            if index < 0 or index > 8:
                print("Invalid input. Please enter a number between 0 and 8.")
                continue

            row, col = divmod(index, 3)  # Convert index to row, col
            if board[row][col] != " ":
                print("Cell is already taken. Try again.")
                continue
        except ValueError:
            print("Invalid input. Please enter a valid number.")
            continue

        # Update board and check for winner
        board[row][col] = players[current_player]
        if check_winner(board, players[current_player]):
            print_board(board)
            print(f"Player {players[current_player]} wins!")
            break
        elif is_draw(board):
            print_board(board)
            print("It's a draw!")
            break

        # Switch player
        current_player = 1 - current_player

play_game()

