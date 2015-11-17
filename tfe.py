from random import choice as rchoice

class Game(object):

	def __init__(self, target=2048, size=4):
		self.over = False
		self.won = False
		self.score = 0
		self.new_cell_distribution = 9*[2] + [4]
		self.target = target
		self.size = size
		self.board = []
		for i in range(self.size):
			row = []
			for j in range(self.size):
				row.append(0)
			self.board.append(row)

		self.fill_random_cell()
		self.fill_random_cell()

	def get_empty_cells(self):
		empty_cells = []
		for i in range(self.size):
			for j in range(self.size):
				if (self.board[i][j] == 0):
					empty_cells.append((i, j))
		return empty_cells

	def fill_random_cell(self):
		empty_cells = self.get_empty_cells()
		if len(empty_cells) > 0:
			(row_index, col_index)= rchoice(empty_cells)
			cell_value = rchoice(self.new_cell_distribution)
			self.board[row_index][col_index] = cell_value
		return (row_index, col_index)

	def check_if_game_over(self):
		empty_cells = self.get_empty_cells()
		if len(empty_cells) == 0:
			for i in range(self.size):
				for j in range(self.size):
					if ((i < 3 and self.board[i][j] == self.board[i+1][j])
						or (j < 3 and self.board[i][j] == self.board[i][j+1])):
						return	
			self.over = True

	def reverse_board(self):
		self.board = [[i for i in reversed(row)] for row in self.board]

	def transpose_board(self):
		self.board = [[self.board[j][i] for j in range(self.size)] for i in range(self.size)]

	def move(self, reverse=False, transpose=False):
		''' By default, move right.
			Reverse to move left, transpose to move down, both to move up.
		'''
		if transpose:
			self.transpose_board()
		if reverse:
			self.reverse_board()

		moved = False
		for row_number in range(self.size):
			new_index = self.size - 1
			for current_index in reversed(range(self.size)):
				current_value = self.board[row_number][current_index]
				if current_value > 0:
					while new_index > current_index:
						# fuse case
						if self.board[row_number][new_index] == current_value:
							self.board[row_number][new_index] = 2*current_value
							self.board[row_number][current_index] = 0
							new_index -= 1 # no tile can fuse with this tile anymore
							moved = True
							
							# update score
							self.score += 2*current_value
							
							# check for win condition
							if self.board[row_number][new_index] == self.target:
								self.won = True
								self.over = True
							break

						# move case
						elif self.board[row_number][new_index] == 0:
							self.board[row_number][new_index] = current_value
							self.board[row_number][current_index] = 0
							moved = True
							break

						else:
							new_index -= 1

		# return board orientation to normal
		if reverse:
			self.reverse_board()
		if transpose:
			self.transpose_board()

		# if we have moved, then we need to fill a new cell
		new_cell_indices = None
		if moved:
			new_cell_indices = self.fill_random_cell()
		
		# once we spawn a new cell, check if the game is over
		self.check_if_game_over()
		return new_cell_indices

	# def move_left(self):
	# 	self.reverse_board()
	# 	new_cell_indices = self.move_right()
	# 	self.reverse_board()
	# 	return self.reverse_indices(new_cell_indices)

	# def move_up(self):
	# 	self.transpose_board()
	# 	self.reverse_board()
	# 	new_cell_indices = self.move_right()
	# 	self.reverse_board()
	# 	self.transpose_board()
	# 	return self.transpose_indices(self.reverse_indices(new_cell_indices))

	# def move_down(self):
	# 	self.transpose_board()
	# 	new_cell_indices = self.move_right()
	# 	self.transpose_board()
	# 	return self.transpose_indices(new_cell_indices)




