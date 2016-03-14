def board(positions):
    for row in positions:
        row_output = ""
        for position in row:
            row_output += str(position) + "|"
        print row_output[:-1]
        print "-----"

def check_move(move, positions, symbol):
    row = (move - 1) / 3
    col = (move - 1) % 3

    if (move >= 1 and move <= 9 and positions[row][col] != 'X' and positions[row][col] != 'O'):
        return True
    else:
        print "Invalid move!"
        return False

def register_move(move, positions, symbol):
    row = (move - 1) / 3
    col = (move - 1) % 3

    positions[row][col] = symbol

def is_filled(positions):
    filled = True

    for row in positions:
        for position in row:
            if (position != 'X' and position != 'O'):
                filled = False

    return filled

def is_won(positions):
    if((positions[0][0] == positions[1][1] and positions[0][0] == positions[2][2]) or (positions[0][2] == positions[1][1] and positions[0][2] == positions[2][0])):
        return True

    for i in range(3):
        if ((positions[i][0] == positions[i][1] and positions[i][0] == positions[i][2]) or (positions[0][i] == positions[1][i] and positions[0][i] == positions[2][i])):
            return True

def get_win_condition(positions):
    if (positions[0][0] == positions[1][1] and positions[0][0] == positions[2][2]):
        return [1, 5, 9]
    elif (positions[0][2] == positions[1][1] and positions[0][2] == positions[2][0]):
        return [3, 5, 7]

    for i in range(3):
        if (positions[i][0] == positions[i][1] and positions[i][0] == positions[i][2]):
            return [positions[i][0], positions[i][1], positions[i][2]]
        elif (positions[0][i] == positions[1][i] and positions[0][i] == positions[2][i]):
            return [positions[0][i], positions[1][i], positions[2][i]]

def get_free_spaces(positions):
    free_spaces = []

    for row in positions:
        for position in row:
            if position != 'X' and position != 'O':
                free_spaces.append(position)

    return free_spaces

def computer_go(positions):
    free_spaces = get_free_spaces(positions)
    scores = []
    for index, position in enumerate(free_spaces):
        scores.append([0, position, []])
        computer_move = simulate_computer_move(positions, scores, index)

    #print scores

    high_score = 0
    computer_move = 0
    for score in scores:
        if score[0] >= high_score:
            high_score = score[0]
            computer_move = score[1]

    row = (computer_move - 1) / 3
    col = (computer_move - 1) % 3

    print "Computer picked: " + str(positions[row][col])
    positions[row][col] = 'O'

def simulate_computer_move(positions, scores, index):
    free_spaces = get_free_spaces(positions)

    #print "Free spaces: " + str(free_spaces)

    for position in free_spaces:
        #print "Checking (computer): " + str(position)
        row = (position - 1) / 3
        col = (position - 1) % 3

        tmp_positions = get_tmp_positions(positions)
        tmp_positions[row][col] = 'O'

        #board(tmp_positions)
    
        filled        = is_filled(tmp_positions)
        won           = is_won(tmp_positions)
        win_condition = get_win_condition(tmp_positions)

        if won:
            if win_condition not in scores[index][2]:
                scores[index][0] = scores[index][0] + 1
                scores[index][2].append(win_condition)

            return
        elif not filled:
            status = simulate_human_move(tmp_positions, scores, index)

def simulate_human_move(positions, scores, index):
    free_spaces = get_free_spaces(positions)

    #print "Free spaces: " + str(free_spaces)

    for position in free_spaces:
        #print "Checking (human): " + str(position)
        row = (position - 1) / 3
        col = (position - 1) % 3

        tmp_positions = get_tmp_positions(positions)
        tmp_positions[row][col] = 'X'
        
        #board(tmp_positions)
    
        filled = is_filled(tmp_positions)
        won    = is_won(tmp_positions)

        if won:
            #scores[index][0] = scores[index][0] - 1
            #print scores
            return
        elif not filled:
            status = simulate_computer_move(tmp_positions, scores, index)

def clear_screen():
    print(chr(27) + "[2J")

def get_tmp_positions(positions):
    tmp_positions = []
    for position in positions:
        tmp_positions.append(position[:])

    return tmp_positions

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
        move_ok = check_move(move, positions, 'X')

    register_move(move, positions, 'X')

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
        computer_go(positions)
        
        filled = is_filled(positions)
        won    = is_won(positions)

        #clear_screen()
        board(positions)

        if filled or won:
            game_complete = True
            if filled and not won:
                print "It's a tie!"
            else:
                print "You lost!"
