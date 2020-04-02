import numpy as np
import random
from math import inf as infinity
import itertools
import pickle
from collections import OrderedDict

players = ['X','O']

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

def getBestMove(state, player):
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
		curr_state_values.append(state_values_for_AI[next_state_idx])
		
	print('Possible moves = ' + str(moves))
	print('Move values = ' + str(curr_state_values))    
	best_move_idx = np.argmax(curr_state_values)
	best_move = moves[best_move_idx]
	return best_move


# ---- Playing ---
	
# LOAD ALL STATES DICTIONARY
states_dict = OrderedDict(pickle.load(open('states_dict.p', 'rb')))

# LOAD TRAINED STATE VALUES
state_values_for_AI = np.loadtxt('trained_state_values_O.txt', dtype=np.float64)

play_again = 'Y'
while play_again == 'Y' or play_again == 'y':
	game_state = [[' ',' ',' '], [' ',' ',' '], [' ',' ',' ']]
	
	print("\nNew Game!")
	print_board(game_state)
	
	player_choice = input("Choose which player goes first - X (You - the petty human) or O (The mighty AI): ")
	
	if player_choice == 'X' or player_choice == 'x':
		current_player_idx = 0
	else:
		current_player_idx = 1

	winner = None
	current_state = "Not Done"
	
	while current_state == "Not Done":

		if current_player_idx == 0: 	# Human's turn
			block_choice = int(input("Oye Human, your turn! Choose where to place (1 to 9): "))
			play_move(game_state, players[current_player_idx], block_choice)
		
		else:   # AI's turn
			block_choice = getBestMove(game_state, players[current_player_idx])
			play_move(game_state, players[current_player_idx], block_choice)
			print("AI plays move: " + str(block_choice))
		
		# --- printing board and winner ---
		print_board(game_state)
		winner, current_state = check_current_state(game_state)
		
		if winner is not None:
			print(str(winner) + " won!")	# print winner
		else:
			current_player_idx = (current_player_idx + 1)%2		# give the turn to other player
		
		if current_state is "Draw":
			print("Draw!")
			
	play_again = input('Wanna try again? (Y/N) : ')
	if play_again == 'N':
		print('Come back later!')