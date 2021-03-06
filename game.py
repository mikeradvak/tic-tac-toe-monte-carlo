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
            actual_value = (i * 3) + 1
            return [actual_value, actual_value + 1, actual_value + 2]
        elif (positions[0][i] == positions[1][i] and positions[0][i] == positions[2][i]):
            actual_value = i + 1
            return [actual_value, actual_value + 3, actual_value + 6]

def get_free_spaces(positions):
    free_spaces = []

    for row in positions:
        for position in row:
            if position != 'X' and position != 'O':
                free_spaces.append(position)

    return free_spaces

def computer_go(positions):
    print "Computer going..."

    free_spaces = get_free_spaces(positions)
    scores      = []
    win_computer_value = 2
    win_human_value    = 3
    max_depth          = 1
    current_depth      = 1

    for position in free_spaces:
        scores.append([0.0, position, [], []])

    for index, position in enumerate(free_spaces):
        computer_move = simulate_computer_move(positions, scores, index, win_computer_value, win_human_value, max_depth, current_depth)

    #print scores

    high_score = 0.0
    computer_move = 0
    for score in scores:
        if score[0] >= high_score:
            high_score = score[0]
            computer_move = score[1]

    row = (computer_move - 1) / 3
    col = (computer_move - 1) % 3

    print "Computer picked: " + str(positions[row][col])
    positions[row][col] = 'O'

def simulate_computer_move(positions, scores, index, win_computer_value, win_human_value, max_depth, current_depth):
    free_spaces = get_free_spaces(positions)

    #print "Free spaces: " + str(free_spaces)

    for position in free_spaces:
        #print "Checking (computer): " + str(position)
        row = (position - 1) / 3
        col = (position - 1) % 3

        tmp_positions = get_tmp_positions(positions)
        tmp_positions[row][col] = 'O'

        #board(tmp_positions)
    
        filled = is_filled(tmp_positions)
        won    = is_won(tmp_positions)

        if won:
            #win_condition = get_win_condition(tmp_positions)
            #if win_condition not in scores[index][2] and scores[index][1] in win_condition:
                #scores[index][0] = scores[index][0] + ((max_depth - current_depth) * win_computer_value)
                #scores[index][2].append(win_condition)
            win_condition = get_win_condition(tmp_positions)
            win_condition.append(current_depth)

            #print "Computer wins in " + str(current_depth)

            for score in scores:
                if score[1] == position:
                    if win_condition not in score[2]:
                        #print "Adding " + str(pow(win_computer_value, (max_depth - current_depth))) + " to " + str(score[1]) + "(" + str(win_computer_value) + ", " + str(max_depth - current_depth) + ")"

                        score[2].append(win_condition)
                        score[0] = score[0] + pow(win_computer_value, (max_depth - current_depth))
                        #print str(score[0])
                    break
            return
        elif not filled:
            status = simulate_human_move(tmp_positions, scores, index, win_computer_value, win_human_value, max_depth, current_depth)

def simulate_human_move(positions, scores, index, win_computer_value, win_human_value, max_depth, current_depth):
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
            win_condition = get_win_condition(tmp_positions)
            win_condition.append(current_depth)

            #print "Human wins in " + str(current_depth)

            for score in scores:
                if score[1] == position:
                    if win_condition not in score[3]:
                        #print "Adding " + str(pow(win_human_value, (max_depth - current_depth))) + " to " + str(score[1]) + "(" + str(win_human_value) + ", " + str(max_depth - current_depth) + ")"

                        score[3].append(win_condition)
                        score[0] = score[0] + pow(win_human_value, (max_depth - current_depth))

                        #print str(score[0])
                    break                         
            return                                
        elif not filled:                          
            status = simulate_computer_move(tmp_positions, scores, index, win_computer_value, win_human_value, max_depth, current_depth + 1)
                                                  
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


move_ok = False
while not move_ok:
    move    = input('Do you want to go first or second (1 or 2): ')
    if move == 1 or move == 2:
        move_ok = True
    else:
        print 'Please enter 1 (first) or 2 (second).'

if (move == 2):
    computer_go(positions)


#clear_screen()
board(positions)

while not game_complete:
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
