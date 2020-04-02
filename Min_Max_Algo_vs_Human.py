import numpy as np
import random
from math import inf as infinity

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


def getBestScore(state, player):
	'''
	Minimax Algorithm
	'''
	winner, current_state = check_current_state(state)
	
	# -- return the results based on the prespective of AI --
	if current_state == "Done" and winner == 'O': # If AI won
		return 1
	elif current_state == "Done" and winner == 'X': # If Human won
		return -1
	elif current_state == "Draw":    # Draw condition
		return 0

	empty_cells = [i*3 + (j+1) for i in range(3) for j in range(3) if state[i][j] is ' ']
	moves = []

	for empty_cell in empty_cells:
		move = {}
		move['index'] = empty_cell
		new_state = copy_game_state(state)
		play_move(new_state, player, empty_cell)

		if player == 'O':    # If AI
			result = getBestScore(new_state, 'X')    # make more depth tree for human
			move['score'] = result
		else:	# If Human
			result = getBestScore(new_state, 'O')    # make more depth tree for AI
			move['score'] = result
		
		moves.append(move)

	# print(f"Moves: { moves }")
	
	# Find best move
	global best_move
	if len(moves) > 1:
		if player == 'O':   # If AI is player - choose best score among the moves
			best_score = -infinity
			for move in moves:
				if move['score'] > best_score:
					best_score = move['score']
					# best_move = move['index']
			# print(f"Best AI Move : { best_move } with score : { best_score }")
		else:				# If Human is player - choose least score among the moves
			best_score = infinity
			for move in moves:
				if move['score'] < best_score:
					best_score = move['score']
					# best_move = move['index']
			# print(f"Best Human Move : { best_move } with score : { best_score }")
			
		# -- randomize the best selection
		best_moves_list = [move for move in moves if move['score']==best_score]
		selected = random.choice(best_moves_list)
		best_move = selected['index']
		best_score = selected['score']
		
		return best_score
	else:
		best_move = moves[0]['index']
		best_score = moves[0]['score']
		return best_score



# PLaying
play_again = 'Y'
while play_again == 'Y' or play_again == 'y':
	game_state = [[' ',' ',' '],
				  [' ',' ',' '],
				  [' ',' ',' ']]
	
	current_state = "Not Done"

	print("\nNew Game!")
	print_board(game_state)

	player_choice = input("Choose which player goes first - X (You - the petty human) or O (The mighty AI): ")
	winner = None

	if player_choice == 'X' or player_choice == 'x':
		current_player_idx = 0
	else:
		current_player_idx = 1

	while current_state == "Not Done":
		if current_player_idx == 0: 	# Human's turn
			block_choice = int(input("Oye Human, your turn! Choose where to place (1 to 9): "))
			play_move(game_state, players[current_player_idx], block_choice)
		
		else:   # AI's turn
			best = getBestScore(game_state, players[current_player_idx])
			print(f" --#-- Best predicted AI score : { best } --#--")
			block_choice = best_move
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
			
	play_again = input('Wanna try again?(Y/N) : ')
	if play_again == 'N':
		print('Come back later!')