import numpy as np

WIN_SLOTS = []
BOARD_WIDTH = 7
BOARD_HEIGHT = 6
MAGIC_NUM = 4

#filling up the win slots - first add vertical wins
for col in range(BOARD_WIDTH):
	for seq_start in range(1 + BOARD_HEIGHT - MAGIC_NUM):
		win = []
		for row in range(seq_start, seq_start + MAGIC_NUM):
			win.append((row, col))
		WIN_SLOTS.append(win)

#add horizontal winning combos
for row in range(BOARD_HEIGHT):
	for seq_start in range(1 + BOARD_WIDTH - MAGIC_NUM):
		win = []
		for col in range(seq_start, seq_start + MAGIC_NUM):
			win.append((row, col))
		WIN_SLOTS.append(win)

#3pi/4 diagonals...hard coded for times sake:
for col in range(4):
	for row in range(3):
		win = []
		for i in range(4):
			win.append((row + i, col + i))
		WIN_SLOTS.append(win)

#pi/4 diagonals...hard coded for times sake:
for col in range(3, 7):
	for row in range(3):
		win = []
		for i in range(4):
			win.append((row-i, col-i))
		WIN_SLOTS.append(win)

#two methods for converting between string and matrix to represent the board
def str_to_matrix(board):
	matrix = []
	for i in range(0, BOARD_HEIGHT*BOARD_WIDTH, BOARD_WIDTH):
		matrix.append([cell for cell in board[i:i+BOARD_WIDTH]])
	return matrix

def matrix_to_string(board):
	string = ''
	for i in range(BOARD_HEIGHT):
		for j in range(BOARD_WIDTH):
			string += (board[i][j])
	return string

class connectFour:
	def __init__(self):
		#matrix of 0's...can be filled with 1s and 2s for the respective players
		self.state = '0' * BOARD_HEIGHT * BOARD_WIDTH

		#whose turn it is (1 or 2)
		self.turn = 2

		#0 for in progress, -1 for tie, 1 and 2 for respective player wins
		self.winner = 0

	def print_board(self):
		for i in range(0, BOARD_HEIGHT*BOARD_WIDTH, BOARD_WIDTH):
			print(self.state[i:i+BOARD_WIDTH])
		
	def make_move(self, col):
		fill = True
		if self.winner != 0:
			return -1
		matrix = str_to_matrix(self.state)
		for row in range(BOARD_HEIGHT, 0, -1):
			if matrix[row-1][col] == '0':
				matrix[row-1][col] = str(self.turn)
				self.state = matrix_to_string(matrix)
				fill = False
				break
		if fill:
			return -1
		self.turn = 1 if self.turn == 2 else 2
		return self.check_win()

	def generate_moves(self):
		empty_cols = [col for col, top_cell in enumerate(str_to_matrix(self.state)[0]) if top_cell == '0']
		new_states = []
		#calculate all the new states it could go to and return this as well
		for col in empty_cols:
			copy = str_to_matrix(self.state)
			for i in range(BOARD_HEIGHT):
				if copy[i][col] != '0':
					copy[i-1][col] = str(self.turn)
					break
				elif i == BOARD_HEIGHT - 1:
					copy[i][col] = str(self.turn)
			new_states.append(matrix_to_string(copy))

		return empty_cols, new_states

	def check_win(self):
		filled = [col for col, top_cell in enumerate(str_to_matrix(self.state)[0]) if top_cell == '0']
		if not filled:
			self.winner = -1
			return -1
		win_slots = WIN_SLOTS
		board = str_to_matrix(self.state)
		#check for win
		for sequence in win_slots:
			num1 = 0
			num2 = 0
			for row, col in sequence:
				if board[row][col] == '1':
					num1 += 1
				elif board[row][col] == '2':
					num2 += 1
			if num1 == 4:
				self.winner = 1
				return 1
			elif num2 == 4:
				self.winner = 2
				return 2
		return 0

	@staticmethod
	def game_status(state):
		win_slots = WIN_SLOTS
		board = str_to_matrix(state)
		#check for win
		for sequence in win_slots:
			num1 = 0
			num2 = 0
			for row, col in sequence:
				if board[row][col] == '1':
					num1 += 1
				elif board[row][col] == '2':
					num2 += 1
			if num1 == 4:
				return 1
			elif num2 == 4:
				return 2
		return 0
			
class Agent:
	def __init__(self, learning_rate):
		#game states its seen before, mapped to their result. states will be converted to strings to be hashable
		self.values = {}

		self.prev_state = None

		self.learning_rate = learning_rate

	def get_value(self, state):
		if state not in self.values.keys():
			self.values[state] = 0.5
		return self.values[state]

	def make_move(self, game, explore_prob=0.1):
		if game.winner == 1:
			self.values[self.prev_state] += self.learning_rate * (0 - self.get_value(self.prev_state))
			return -1

		if game.winner == -1:
			self.values[self.prev_state] += self.learning_rate * (0.5 - self.get_value(self.prev_state))
			return -1

		#looking for moves
		possible_moves, new_states = game.generate_moves()
		vals = [self.get_value(state) for state in new_states]

		#adding randomness
		if np.random.random() < explore_prob:
			#exploratory move
			random_move = possible_moves[np.random.randint(len(possible_moves))]
			win = game.make_move(random_move)
			if win > 0:
				self.values[game.state] = 1
			elif win == -1:
				self.values[game.state] = 0.5
			# print(game.state)
			self.prev_state = game.state
			return random_move
		else:
			best_move = possible_moves[np.argmax(vals)]
			win = game.make_move(best_move)
			# game.print_board()
			if win > 0:
				self.values[game.state] = 1
			elif win == -1:
				self.values[game.state] = 0.5
			if self.prev_state:
				# print("yo")
				self.values[self.prev_state] += self.learning_rate * (self.get_value(game.state) - self.get_value(self.prev_state))
			# print(game.state)
			self.prev_state = game.state
			return best_move

	def new_game(self):
		self.prev_state = None

class Opponent:
	def __init__(self):
		pass

	def make_random_move(self, game):
		possible_moves, _ = game.generate_moves()
		random_move = possible_moves[np.random.randint(len(possible_moves))]
		game.make_move(random_move)
		return random_move

	def make_move(self, game):
		possible_moves, new_states = game.generate_moves()

		for move, state in zip(possible_moves, new_states):
			#make a winning move if possible
			if connectFour.game_status(state) == 1:
				game.make_move(move)
				return move
		#block a winning move if one exists
		for move in possible_moves:
			mod_state = str_to_matrix(state)
			for i in range(BOARD_HEIGHT):
				if mod_state[i][move] != '0' or i == BOARD_HEIGHT - 1:
					mod_state[i-1][move] = '2'
					break
			if connectFour.game_status(matrix_to_string(mod_state)) == 2:
				game.make_move(move)
				return move
		return self.make_random_move(game)


training_games = 100000
trained_agent = Agent(0.05)

# play training_games number of games, training the same Agent
for i in range(training_games):
	if i % 1000 == 0:
		print(i / 1000)
	game = connectFour()
	opponent = Opponent()
	trained_agent.new_game()
	while True:
		if trained_agent.make_move(game) < 0:
			break
		if game.winner != 0:
			break
		if opponent.make_move(game) < 0:
			break

wins = 0
ties = 0
losses = 0
total_games = 1000

for i in range(total_games):
	game = connectFour()
	opponent = Opponent()
	trained_agent.new_game()
	while True:
		# print("pp")
		if trained_agent.make_move(game) < 0:
			break
		if game.winner != 0:
			break
		if opponent.make_move(game) < 0:
			break
	if game.winner == -1:
		ties += 1
	elif game.winner == 1:
		losses += 1
	else:
		wins += 1

# output the benchmark results
print(f"Record: {wins}-{losses}-{ties}")
print(f"Win Percentage: {100 * wins / total_games}")



	
