import numpy as np
import random
import itertools
import pickle
from math import inf as infinity
from time import time
from collections import OrderedDict

players = ['X','O']
best_move = None

def print_board(game_state):
	print('----------------')
	print('| ' + str(game_state[0][0]) + ' || ' + str(game_state[0][1]) + ' || ' + str(game_state[0][2]) + ' |')
	print('----------------')
	print('| ' + str(game_state[1][0]) + ' || ' + str(game_state[1][1]) + ' || ' + str(game_state[1][2]) + ' |')
	print('----------------')
	print('| ' + str(game_state[2][0]) + ' || ' + str(game_state[2][1]) + ' || ' + str(game_state[2][2]) + ' |')
	print('----------------')

def copy_game_state(state):
    new_state = [[' ',' ',' '],[' ',' ',' '],[' ',' ',' ']]
    for i in range(3):
        for j in range(3):
            new_state[i][j] = state[i][j]
    return new_state

def check_current_state(game_state):
	# Check horizontals
	for i in range(3):
		if (game_state[i][0] == game_state[i][1] and game_state[i][1] == game_state[i][2] and game_state[i][0] is not ' '):
			return game_state[i][0], "Done"
	
	# Check verticals
	for j in range(3):
		if (game_state[0][j] == game_state[1][j] and game_state[1][j] == game_state[2][j] and game_state[0][j] is not ' '):
			return game_state[0][j], "Done"
	
	# Check diagonals
	if (game_state[0][0] == game_state[1][1] and game_state[1][1] == game_state[2][2] and game_state[0][0] is not ' '):
		return game_state[1][1], "Done"
	if (game_state[2][0] == game_state[1][1] and game_state[1][1] == game_state[0][2] and game_state[2][0] is not ' '):
		return game_state[1][1], "Done"

	# Check if draw
	draw_flag = 0
	for i in range(3):
		for j in range(3):
			if game_state[i][j] is ' ':		# Checking if there are any empty spaces and if yes then its not draw
				draw_flag = 1
	if draw_flag is 0:
		return None, "Draw"

	return None, "Not Done"

def play_move(state, player, block_num):
	row = int((block_num-1)/3)
	col = (block_num-1)%3
	
	if state[row][col] is ' ':
		state[row][col] = player
	else:
		block_num = int(input("Block is not empty, ya blockhead! Choose again: "))
		play_move(state, player, block_num)

# ------ Getting state values (ENVIRONMENT SETUP) ------

# getting all possible state combinations
player = ['X','O',' ']
all_possible_states = [[list(i[0:3]), list(i[3:6]), list(i[6:10])] for i in itertools.product(player, repeat = 9) if i.count('X') <= 5 and i.count('O') <= 5 and abs(i.count('X') - i.count('O')) in [1, 0]]

n_states = len(all_possible_states) # 2 players, 9 spaces
n_actions = 9   # 9 spaces
print("n_states = %i \nn_actions = %i"%(n_states, n_actions))

# -- store all states as a dictionary --
states_dict = OrderedDict({i: all_possible_states[i] for i in range(n_states)})
pickle.dump(states_dict, open('states_dict.p', 'wb'))

# Initialize state values with 0.0
state_values_for_AI_O = np.full((n_states), 0.0)
state_values_for_AI_X = np.full((n_states), 0.0)

# State values for AI 'O'
for i in range(n_states):
    winner, _ = check_current_state(states_dict[i])
    if winner == 'O':     # AI 'O' won & AI 'X' lost
        state_values_for_AI_O[i] = 1
        state_values_for_AI_X[i] = -1
    elif winner == 'X':   # AI 'O' lost & AI 'X' won
        state_values_for_AI_O[i] = -1
        state_values_for_AI_X[i] = 1

print(len(state_values_for_AI_O), " state_values_for_AI_O : ", state_values_for_AI_O)
print(len(state_values_for_AI_X), " state_values_for_AI_X : ", state_values_for_AI_X)

# -- updating the state values (REWARDS based on the ACTION performed) --

def update_state_value_O(curr_state_idx, next_state_idx, learning_rate):
    new_value = state_values_for_AI_O[curr_state_idx] + learning_rate*(state_values_for_AI_O[next_state_idx]  - state_values_for_AI_O[curr_state_idx])
    state_values_for_AI_O[curr_state_idx] = new_value
    
def update_state_value_X(curr_state_idx, next_state_idx, learning_rate):
    new_value = state_values_for_AI_X[curr_state_idx] + learning_rate*(state_values_for_AI_X[next_state_idx]  - state_values_for_AI_X[curr_state_idx])
    state_values_for_AI_X[curr_state_idx] = new_value


def getBestMove(state, player, epsilon):
    '''
    Reinforcement Learning Algorithm
    '''
    moves = []
    curr_state_values = []

    empty_cells = [i*3 + (j+1) for i in range(3) for j in range(3) if state[i][j] is ' ']
    
    for empty_cell in empty_cells:
        moves.append(empty_cell)
        new_state = copy_game_state(state)
        play_move(new_state, player, empty_cell)
        next_state_idx = list(states_dict.keys())[list(states_dict.values()).index(new_state)]
        if player == 'X':
            curr_state_values.append(state_values_for_AI_X[next_state_idx])
        else:
            curr_state_values.append(state_values_for_AI_O[next_state_idx])
        
    print('Possible moves = ' + str(moves))
    print('Move values = ' + str(curr_state_values))    
    best_move_idx = np.argmax(curr_state_values)
    
    # -- Model tuning based for Exploration vs Exploitation --
    if np.random.uniform(0,1) <= epsilon:       # Exploration
        best_move = random.choice(empty_cells)
        print('Agent decides to explore! Takes action = ' + str(best_move))
        epsilon *= 0.99
    else:   #Exploitation
        best_move = moves[best_move_idx]
        print('Agent decides to exploit! Takes action = ' + str(best_move))
    return best_move


# ----- MODEL TRAINING -----

# Parameters
learning_rate = 0.2
epsilon = 0.2
num_iterations = 10000

start_time = time()
for iteration in range(num_iterations):
    print("\nIteration " + str(iteration) + "!")
    
    game_state = [[' ',' ',' '], [' ',' ',' '],[' ',' ',' ']]
    print_board(game_state)
    
    current_player_idx = random.choice([0,1])

    winner = None
    current_state = "Not Done"

    while current_state == "Not Done":
        curr_state_idx = list(states_dict.keys())[list(states_dict.values()).index(game_state)]
        
        if current_player_idx == 0:     # AI_X's turn
            print("\nAI X's turn!")         
            block_choice = getBestMove(game_state, players[current_player_idx], epsilon)
            play_move(game_state, players[current_player_idx], block_choice)
            new_state_idx = list(states_dict.keys())[list(states_dict.values()).index(game_state)]
            
        else:       					# AI_O's turn
            print("\nAI O's turn!")   
            block_choice = getBestMove(game_state, players[current_player_idx], epsilon)
            play_move(game_state, players[current_player_idx], block_choice)
            new_state_idx = list(states_dict.keys())[list(states_dict.values()).index(game_state)]
        
        print_board(game_state)

        # -- REWARD based on the move choosen --
        update_state_value_O(curr_state_idx, new_state_idx, learning_rate)
        update_state_value_X(curr_state_idx, new_state_idx, learning_rate)

        winner, current_state = check_current_state(game_state)

        if winner is not None:
            print(str(winner) + " won!")
        else:
            current_player_idx = (current_player_idx + 1)%2
        
        if current_state is "Draw":
            print("Draw!")

print('Training Complete!')

end_time = time()    
print("Time taken is : ", end_time - start_time, " seconds")

# Save state values for future use
np.savetxt('trained_state_values_X.txt', state_values_for_AI_X, fmt = '%.6f')
np.savetxt('trained_state_values_O.txt', state_values_for_AI_O, fmt = '%.6f')