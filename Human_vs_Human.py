import numpy as np

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

# PLaying
play_again = 'Y'
while play_again == 'Y' or play_again == 'y':
	game_state = [[' ',' ',' '],
				  [' ',' ',' '],
				  [' ',' ',' ']]
	
	current_state = "Not Done"

	print("\nNew Game!")
	print_board(game_state)

	player_choice = input("Choose which player goes first - X or O : ")
	winner = None

	if player_choice == 'X' or player_choice == 'x':
		current_player_idx = 0
	else:
		current_player_idx = 1

	while current_state == "Not Done":
		block_choice = int(input(players[current_player_idx] +"'s turn! Choose where to place (1 to 9): "))
		play_move(game_state, players[current_player_idx], block_choice)
	
		# --- printing board and winner ---
		print_board(game_state)
		winner, current_state = check_current_state(game_state)
		
		if winner is not None:
			print(str(winner) + " won!")	# print winner
		else:
			current_player_idx = (current_player_idx + 1)%2		# give the turn to other player
		
		if current_state is "Draw":
			print("Draw!")
			
	play_again = input('Play again? (Y/N) : ')
	if play_again == 'N':
		print('Come back later!')
