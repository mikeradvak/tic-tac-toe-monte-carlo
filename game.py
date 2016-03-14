def board(t_positions):
    for row in t_positions:
        row_output = ""
        for position in row:
            row_output += str(position) + "|"
        print row_output[:-1]
        print "-----"

def register_move(move, positions, symbol):
    row = (move - 1) / 3
    col = (move - 1) % 3

    if (move >= 1 and move <= 9 and positions[row][col] != 'X' and positions[row][col] != 'O'):
        positions[row][col] = symbol
        return True
    else:
        print "Invalid move!"
        return False

def is_filled(positions):
    filled = True

    for row in positions:
        for position in row:
            if (position != 'X' and position != 'O'):
                filled = False

    return filled

def is_won(positions):
    for i in range(3):
        if ((positions[i][0] == positions[i][1] and positions[i][0] == positions[i][2]) or (positions[0][i] == positions[1][i] and positions[0][i] == positions[2][i])):
            return True
        elif((positions[0][0] == positions[1][1] and positions[0][0] == positions[2][2]) or (positions[0][2] == positions[1][1] and positions[0][2] == positions[2][0])):
            return True

def get_free_spaces(positions):
    free_spaces = []

    for row in positions:
        for position in row:
            if position != 'X' and position != 'O':
                free_spaces.append(position)

    return free_spaces

def computer_go(t_positions):
    fuck = t_positions[:]
    computer_move = simulate_computer_move(fuck[:])
    print "@@@"
    board(positions)
    print "###"
    board(t_positions)
    return True

def simulate_computer_move(t_positions):
    free_spaces = get_free_spaces(t_positions[:])
    best_status = [-1, -1]

    for position in free_spaces:
        print "Checking (computer): " + str(position)
        row = (position - 1) / 3
        col = (position - 1) % 3
        #tmp_positions = t_positions[:]
        #tmp_positions[row][col] = 'O'
        print "1"
        board(positions[:])
        print "2"
        board(t_positions[:])
        print "3"
        board(tmp_positions[:])
        print positions is t_positions
        die()
    
        filled = is_filled(tmp_positions[:])
        won    = is_won(tmp_positions[:])

        if won:
            status = [1, position]
        elif not filled:
            print "$$$"
            board(positions)
            print "$$$"
            status = simulate_human_move(tmp_positions[:])
        else:
            status = [-1, position]

        if status[0] >= best_status[0]:
            best_status = status

        if status[0] == 1:
            print "Computer won! Good!"
            return best_status

    return best_status

def simulate_human_move(t_positions):
    free_spaces = get_free_spaces(t_positions[:])
    best_status = [-1, -1]

    for position in free_spaces:
        print "Checking (human): " + str(position)
        row = (position - 1) / 3
        col = (position - 1) % 3
        board(positions)
        tmp_positions = t_positions[:]
        tmp_positions[row][col] = 'X'
        board(tmp_positions)
    
        filled = is_filled(tmp_positions)
        won    = is_won(tmp_positions)

        if won:
            status = [-1, position]
        elif not filled:
            status = simulate_computer_move(tmp_positions[:])
        else:
            status = [0, position]

        if status[0] >= best_status[0]:
            best_status = status

        if status[0] == -1:
            print "Human won! Bad!"
            return best_status

    return best_status


def clear_screen():
    print(chr(27) + "[2J")

positions    = range(3)
positions[0] = range(1,4)
positions[1] = range(4,7)
positions[2] = range(7,10)

game_complete = False

while not game_complete:
    #clear_screen()
    board(positions)

    move_ok = False
    while not move_ok:
        move    = input('Select a move: ')
        move_ok = register_move(move, positions, 'X')

    filled = is_filled(positions)
    won    = is_won(positions)

    #clear_screen()
    board(positions)

    if filled or won:
        game_complete = True
        if filled and not won:
            print "It's a tie!"
        else:
            print "You won!"
    else:
        print "Computer going..."
        computer_go(positions[:])
