import tfe
import curses

def get_cell_string(num):
	result = ""
	if num > 0:
		cellstr = str(num)
	else:
		cellstr = "."
	for x in range(4):
		try:
			result += cellstr[x]
		except IndexError:
			result += " "
	return result

def get_cell_color(num):
	if num <= 2:
		return curses.color_pair(0)
	elif num == 4:
		return curses.color_pair(187)
	elif num == 8:
		return curses.color_pair(185)
	elif num == 16:
		return curses.color_pair(184)
	elif num == 32:
		return curses.color_pair(214)
	elif num == 64:
		return curses.color_pair(202)
	elif num == 128:
		return curses.color_pair(196)
	elif num == 256:
		return curses.color_pair(197)
	elif num == 512:
		return curses.color_pair(201)
	elif num == 1024:
		return curses.color_pair(53)
	elif num == 2048:
		return curses.color_pair(124)


def display_game(has_colors, filter_indices=None):
	gamescr.addstr(1, 0, "Score: " + str(game.score))
	y_coord = 4
	for i in range(game.size):
		y_coord += 1
		x_coord = 0
		for j in range(game.size):
			if (i, j) == filter_indices:
				num = 0
			else:
				num = game.board[i][j]
			cellstr = get_cell_string(num)
			x_coord += 4
			if has_colors:
				cellcolor = get_cell_color(num)
				gamescr.addstr(y_coord, x_coord, cellstr, cellcolor)
			else:
				gamescr.addstr(y_coord, x_coord, cellstr)
	gamescr.refresh()

if __name__ == "__main__":

	# Initialize game screen
	game = tfe.Game()
	gamescr = curses.initscr()
	gamescr.keypad(1)
	curses.curs_set(0)
	curses.start_color()

	# initialize colors
	has_colors = False
	if curses.has_colors():
		has_colors = True
		curses.use_default_colors()
		for i in range(0, curses.COLORS):
	   		curses.init_pair(i, i, -1)
	else:
		gamescr.addstr(1, 0, '''Your terminal cannot display colors, which 
			may make the game board less readable.''')
		
	gamescr.addstr(0, 0, "Use arrow keys to move, or press 'q' to quit. \n")
	display_game(has_colors)

	# main game loop
	next_move = ""
	while next_move != ord("q"):
		next_move = gamescr.getch()
		new_cell_indices = None
		if next_move == curses.KEY_RIGHT:
			new_cell_indices = game.move()
		elif next_move == curses.KEY_LEFT:
			new_cell_indices = game.move(reverse=True)
		elif next_move == curses.KEY_DOWN:
			new_cell_indices = game.move(transpose=True)
		elif next_move == curses.KEY_UP:
			new_cell_indices = game.move(reverse=True, transpose=True)
		# if next_move == curses.KEY_UP:
		# 	new_cell_indices = game.move_up()
		# elif next_move == curses.KEY_LEFT:
		# 	new_cell_indices = game.move_left()
		# elif next_move == curses.KEY_DOWN:
		# 	new_cell_indices = game.move_down()
		# elif next_move == curses.KEY_RIGHT:
		# 	new_cell_indices = game.move_right()
		else:
			continue

		# if a new cell has spawned, we want to
		# wait 100ms before showing it.
		if new_cell_indices == None:
			display_game(has_colors)
		else:
			display_game(has_colors, filter_indices=new_cell_indices)
			curses.napms(100)
			display_game(has_colors)

		if game.over:
			if game.won:
				gamescr.addstr(10, 0, "You win!\n")
				gamescr.refresh()
			else:
				gamescr.addstr(10, 0, "Game over...\n")
				gamescr.refresh()

	curses.endwin()

