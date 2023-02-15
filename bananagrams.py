import anagramSolver as a_s
import copy
import time

class banagrams(object):
    def __init__(self, letters = '', grid = [[' ']], max_len = 8):
        ''' Creates the grid to be used as a board and stores our available letters in a letter bank. '''
        self.grid = grid
        self.max_len = max_len

        self.letter_bank = {}
        self.total_letters = {}

        for l in letters: # self.addLetter but DON'T update until all letters are added. Makes initialization faster.
            if l in self.letter_bank.keys():
                self.letter_bank[l] += 1
                self.total_letters[l] += 1
            else:
                self.total_letters[l] = 1
                self.letter_bank[l] = 1
        self.possible_words = []
        self.get_possible_words() # Build a list of possible words given the drawn letters.

    @property
    def filled_tiles(self):
        filled_tiles = []
        for i in range(len(self.grid)):
            for j in range(len(self.grid[0])):
                if self.grid[i][j] != ' ':
                    filled_tiles.append((i,j))
        return filled_tiles

    def addWord(self, w, position = [0,0], orientation = 'H'):
        ''' Position = position of first letter relative to current origin as a list.
        Orientation = vertical or horizontal '''
        # Clear self.most_recent as we only want to hold the most recent word
        self.most_recent = []
        # Origin position
        origin_x = 0
        origin_y = 0
        # Get the lengths of the word in the x and y directions
        if orientation == 'V':
            word_length_x = 0
            word_length_y = len(w)
        elif orientation == 'H':
            word_length_x = len(w)
            word_length_y = 0
        # Add the word
        if orientation == 'V':
            # Reshape the grid to fit the first letter of the word.
            self.resize(position)
            # Revalue positions
            for i in range(len(position)):
                if position[i] < 0:
                    position[i] = 0
            # Check to see if word can fit in resized grid
            length_y = len(self.grid)
            difference = (length_y - (word_length_y + position[0]))
            if difference >= 0:
                # If so, add the word
                for i in range(len(w)):
                    if self.grid[position[0] + i][position[1]] == ' ':
                        self.grid[position[0] + i][position[1]] = w[i]
                        self.most_recent.append((position[0] + i,position[1]))
                        self.removeLetter(w[i])
            else:
                # If not, resize again to fit.
                to_add = -difference
                for i in range(to_add):
                    self.expand_row(dir = 'D')
                for i in range(len(w)):
                    if self.grid[position[0] + i][position[1]] == ' ':
                        self.grid[position[0] + i][position[1]] = w[i]
                        self.most_recent.append((position[0] + i, position[1]))
                        self.removeLetter(w[i])
        elif orientation == 'H':
            # Reshape the grid to fit the first letter of the word.
            self.resize(position)
            # Revalue positions
            for i in range(len(position)):
                if position[i] < 0:
                    position[i] = 0
            # Check to see if word can fit in resized grid
            length_x = len(self.grid[0])
            difference = (length_x - (word_length_x + position[1]))
            if difference >= 0:
                # If so, add the word
                for i in range(len(w)):
                    if self.grid[position[0]][position[1] + i] == ' ':
                        self.grid[position[0]][position[1] + i] = w[i]
                        self.most_recent.append((position[0], position[1] + i))
                        self.removeLetter(w[i])
            else:
                # If not, resize again to fit.
                to_add = -difference
                for i in range(to_add):
                    self.expand_col(dir = 'R')
                for i in range(len(w)):
                    if self.grid[position[0]][position[1] + i] == ' ':
                        self.grid[position[0]][position[1] + i] = w[i]
                        self.most_recent.append((position[0], position[1] + i))
                        self.removeLetter(w[i])
        return self.grid

    def get_possible_words(self):
        ''' updates and returns all words that can be formed from our current letters. Note that this is NOT a
         property function since then it would be called a lot and that's slow. We ONLY want to run this once during
         initialization and once whenever we add a letter, NOT during the solving process '''
        string = ''
        for k in self.total_letters.keys():
            for i in range(self.total_letters[k]):
                string += k
        self.possible_words = a_s.anagram(string, max_len=self.max_len, known = self.possible_words)
        return self.possible_words

    def get_buildable_words(self, letters_list):
        ''' Like get_possible_words, but instead looks at the words that can be created with self.letter_bank instead
         of self.total_letters. letters_list is a bunch of extra letters that we add to the list (i.e. anchor letters that are
          already on the board) '''
        string = ''
        for letter in letters_list:
            string += letter
        for k in self.letter_bank.keys():
            for i in range(self.letter_bank[k]):
                string += k
        self.buildable_words = a_s.anagram(string, words = self.possible_words, max_len=self.max_len)
        return self.buildable_words

    def addLetter(self, l):
        ''' Adds a letter to the letter banks and updates the possible words '''
        if l in self.letter_bank.keys():
            self.letter_bank[l] += 1
            self.total_letters[l] += 1
        else:
            self.total_letters[l] = 1
            self.letter_bank[l] = 1
        self.get_possible_words() # Update the possible words list

    def removeLetter(self, l):
        if l in self.letter_bank.keys():
            self.letter_bank[l] -= 1
            if self.letter_bank[l] < 0:
                raise Exception('Not Enough Letters!')
        else:
            raise Exception(f'Letter {l} has not been drawn yet!')

    def resize(self, position):
        # Columns
        if position[1] < 0:
            for i in range(abs(position[1])):
                self.expand_col(dir='L')
        elif position[1] > (len(self.grid[0]) - 1):
            for i in range(position[1] - (len(self.grid[0]) - 1)):
                self.expand_col(dir='R')
        # Rows
        if position[0] < 0:
            for i in range(abs(position[0])):
                self.expand_row(dir='U')
        elif position[0] > (len(self.grid) - 1):
            for i in range(position[0] - (len(self.grid) - 1)):
                self.expand_row(dir='D')

    def expand_col(self, dir = 'L'):
        ''' Adds an empty column to self.grid on the 'dir' side of the grid. Used for resizing '''
        for i in range(len(self.grid)):
            if dir == 'L':
                self.grid[i] = [' '] + self.grid[i]
            elif dir == 'R':
                self.grid[i] = self.grid[i] + [' ']
            else:
                raise Exception('Not a valid direction')

    def expand_row(self, dir = 'U'):
        ''' Adds an empty row to self.grid on the 'dir' side of the grid. Used for resizing'''
        empty_row = [[' ' for x in range(len(self.grid[0]))]]
        if dir == 'U':
            self.grid = empty_row + self.grid
        elif dir == 'D':
            self.grid = self.grid + empty_row
        else:
            raise Exception('Not a valid direction')

    def checkValid(self):
        ''' Finds all words on the current board and makes sure they are each valid. '''
        words_list = []
        # Grab all rows and columns
        rows = self.grid
        columns = [[self.grid[i][j] for i in range(len(self.grid))] for j in range(len(self.grid[0]))]
        # Get words from rows/columns
        for row in rows:
            row_str = ''.join(row)
            joined_row = row_str.split(' ') # Joins adjacent non ' ' entries
            for entry in joined_row:
                if len(entry) > 1:
                    words_list.append(entry)
        for col in columns:
            col_str = ''.join(col)
            joined_col = col_str.split(' ')
            for entry in joined_col:
                if len(entry) > 1:
                    words_list.append(entry)
        # Check Validity of word
        flag = True
        for word in words_list:
            if word not in self.possible_words:
                flag = False
                break
        return flag

    def findNeighbours(self, position):
        ''' Returns coordinates of all non-empty neighbouring spaces '''
        neighbours = []
        for i in range(3):
            for j in range(3):
                if (i,j) != (1,1):
                    try:
                        index_1 = position[0] + i - 1
                        index_2 = position[1] + j - 1
                        if index_1 < 0 or index_2 < 0:
                            pass
                        elif self.grid[index_1][index_2] != ' ':
                            neighbours.append((index_1,index_2))
                    except:
                        pass
        return neighbours

    def num_neighbours(self, position):
        return len(self.findNeighbours(position))

    def possible_connections(self, position):
        ''' Takes in a poition of a letter on the grid and returns all possible words with length less than self.max_len
        that can be built using that position of which it occurs. It also takes into account other
        letters on the board.
        For example, if the letter is 'd' and we can place the words 'dog' and 'odd' this function will return
        [('dog',0),('odd',1),('odd',2)]
        This function basically takes in ALL of our constraints and figures out which words we can actually play on
        a given board at a given location. '''
        # Are we building horizontally or vertically?
        neighbours = self.findNeighbours(position)
        if neighbours == []:
            orientation = 'H'
        elif (position[0], position[1] + 1) in neighbours or (position[0], position[1] + -1) in neighbours:
            orientation = 'V'
        elif (position[0] + 1, position[1]) in neighbours or (position[0] - 1, position[1]) in neighbours:
            orientation = 'H'
        else:
            raise Exception('Neighbours are not consistant')
        # All constraining combinations of on board_letters
        indices, anchors = self.letter_indices(position, orientation)
        # All filtered words using those constraints
        for i in range(len(indices)):
            added_letters = [x[0] for x in indices[i]]
            buildable_words = self.get_buildable_words(added_letters)
            possible_words = filter_possible_words(buildable_words, indices[i])
            for word in possible_words:
                if self.grid[position[0]][position[1]] != ' ':
                    yield (word, anchors[i], orientation)
                else:
                    if anchors[i] == [0,0]: # If we're at the starting position, only add words that start at [0,0]
                        yield (word, anchors[i], orientation)

    def letter_indices(self, position, orientation):
        ''' Takes a position and an orientation and returns all the letters and indices of letters on the board
         within max_len units. Returns tuple, one being the indices and one being the positions of the first
          letter of the words'''
        if orientation == 'H':
            ans = []
            anchors = []
            for i in range(self.max_len):
                loop_letters = [' ' for x in range(self.max_len)]
                first_letter = [position[0],position[1]-self.max_len+i+1]
                for j in range(self.max_len):
                    if first_letter[1] + j < 0: # Since you can negative index lists
                        pass
                    else:
                        try:
                            # Add letter at coordinates on grid
                            loop_letters[j] = self.grid[first_letter[0]][first_letter[1] + j]
                        except:
                            # Keep the list a ' '
                            pass
                temp = []
                for j in range(len(loop_letters)):
                    if loop_letters[j] != ' ':
                        temp.append((loop_letters[j], j))
                ans.append(temp)
                anchors.append(first_letter)
            return ans, anchors

        elif orientation == 'V':
            ans = []
            anchors = []
            for i in range(self.max_len):
                loop_letters = [' ' for x in range(self.max_len)]
                first_letter = [position[0] - self.max_len + i + 1, position[1]]
                for j in range(self.max_len):
                    if first_letter[0] + j < 0: # Since you can negative index lists
                        pass
                    else:
                        try:
                            # Add letter at coordinates on grid
                            loop_letters[j] = self.grid[first_letter[0]+j][first_letter[1]]
                        except:
                            # Keep the list a ' '
                            pass
                temp = []
                for j in range(len(loop_letters)):
                    if loop_letters[j] != ' ':
                        temp.append((loop_letters[j], j))
                ans.append(temp)
                anchors.append(first_letter)
            return ans, anchors

    def is_done(self):
        flag = True  # Check to see if completed
        for key in self.letter_bank.keys():
            if self.letter_bank[key] != 0:
                flag = False
        return flag

    def __str__(self):
        ans = ''
        for row in self.grid:
            ans += str(row) + '\n'
        return ans

# Position Functions
def least_neighbours(b):
    ''' Returns a list of the non ' ' positions in order of fewest neighbours '''
    if b.grid == [[' ']]:
        return [(0,0)]
    func = lambda t: b.num_neighbours(t)
    return sorted(b.filled_tiles, key=func)

# Helper Functions
def filter_possible_words(words, indices_list):
    ''' Looks through words and ONLY returns words that have the specified characters in the specified indexes.
     indices_list is a list of tuples of letters and numbers. The letter is the letter, the number is the index. '''
    ans = []
    for word in words:
        flag = True
        for letter in indices_list:
            try:
                if word[letter[1]] != letter[0]:
                    flag = False
            except:
                flag = False # If an index error, then the word isn't long enough. Obviously false.
        if flag:
            if len(word) != len(indices_list):
                ans.append(word)
    return ans

def scrabble_score(word, bias = 2):
    score_dict = {'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1,
                  'm': 3, 'n': 1,'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 8, 'w': 4, 'x': 8,
                  'y': 4, 'z': 10}
    score = 0
    for letter in word:
        score += (score_dict[letter]**bias)
    return score

def solve(board, position_function = least_neighbours, path = [], show = False):
    ''' Takes in an incomplete board and returns a bananagrams solution containing those letter.
     position_function = function that takes in a banangrams object and returns a list of positions to iterate through
     letters = string of letters drawn
     '''
    if board.is_done() == True:
        return board

    if path == []:
        path.append(board)

    position_queue = position_function(board) # Order of positions that we try to add words to
    for position in position_queue:
        word_queue = sorted(board.possible_connections(position),
                                reverse=True, key=lambda t: scrabble_score(t[0])) # Longest words first
        for word in word_queue:
            current_board = copy.deepcopy(board)
            try:
                current_board.addWord(word[0], word[1], word[2])
                if not current_board.checkValid(): # Make sure the word fits
                    continue
            except:
                continue
            if show:
                print(f'Letters Remaining:  {"".join([x for x in current_board.letter_bank.keys() if current_board.letter_bank[x] != 0])}')
                print(current_board)
            path.append(current_board)
            solution = solve(current_board, path=path, show=show)
            if solution != None:
                return path
            path.pop()

def retrace(path, new_letter):
    for i in range(len(path)):
        board = path[-i]
        board.addLetter(new_letter)
        solution = solve(board, path = path[:-i])
        if solution != None:
            return solve(board)

def play_game(letters, ret = False, path = None):
    if not ret:
        game = banagrams(letters)
        t1 = time.process_time()
        solution_path = solve(game)
        t2 = time.process_time()
        print(solution_path[-1])
        print(f'\tTime Elapsed = {t2 - t1} s')
    else:
        new_letter = letters[-1]
        t1 = time.process_time()
        solution_path = retrace(path, new_letter)
        t2 = time.process_time()
        print(solution_path[-1])
        print(f'\tTime Elapsed = {t2 - t1} s')
    return solution_path

if __name__ == '__main__':
    with open('titlecard') as f:
        for line in f:
            print(line, end = '')
    print('\n=====================================================================')
    letters = input('Enter your initial letters: ')
    solution = play_game(letters)
    while True:
        new_letter = input('Peel! ')
        letters += new_letter
        play_game(letters)