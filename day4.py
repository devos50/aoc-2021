drawn_numbers = []
boards = []
board_eliminated = []

def compute_solution(board, draw):
    s = 0
    for row in range(5):
        for col in range(5):
            if board[row][col] != -1:
                s += board[row][col]
    print(s * draw)
    exit(0)



with open("data/day4.txt") as in_file:
    lines = in_file.read().split("\n")
    drawn_numbers = [int(num) for num in lines[0].strip().split(",")]

    line_ind = 1
    while True:
        if line_ind >= len(lines):
            break

        boards.append([[int(num) for num in line.replace("  ", " ").strip().split(" ")] for line in lines[line_ind+1:line_ind+6]])
        board_eliminated.append(False)

        line_ind += 6

# I know, this can be optimized with some additional bookkeeping...
for draw in drawn_numbers:
    for board_ind in range(len(boards)):
        if board_eliminated[board_ind]:
            continue

        for x in range(5):
            for y in range(5):
                if boards[board_ind][x][y] == draw:
                    boards[board_ind][x][y] = -1

    # Check if there's a winner
    for board_ind in range(len(boards)):
        for row in range(5):
            if all([True if num == -1 else False for num in boards[board_ind][row]]):
                # Board wins
                board_eliminated[board_ind] = True
                if all(board_eliminated):
                    compute_solution(boards[board_ind], draw)

        for col in range(5):
            all_set = True
            for row in range(5):
                if boards[board_ind][row][col] != -1:
                    all_set = False
                    break

            if all_set:
                board_eliminated[board_ind] = True
                if all(board_eliminated):
                    compute_solution(boards[board_ind], draw)



print(drawn_numbers)
print(boards[2])