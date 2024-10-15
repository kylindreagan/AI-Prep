import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count
        self.is_safe = {x: False for x in cells}
        self.is_mines = {x: False for x in cells}

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        if len(self.cells) == self.count:
            return self.cells.copy()
        return set(x for x in self.cells if self.is_mines[x])

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if 0 == self.count:
            return self.cells.copy()
        return set(x for x in self.cells if self.is_safe[x])

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.is_mines[cell] = True
            self.count -= 1
        if self.count == 0:
            remaining = set(x for x in self.cells if not self.is_mines[x])
            for r in remaining:
                self.mark_safe(r)

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.is_safe[cell] = True


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        self.moves_made.add(cell)
        if cell in self.safes:
            self.safes.remove(cell)
        total_cells = set()
        for i in range(3):
            for j in range(3):
                row = cell[0] + (i - 1)
                col = cell[1] + (j - 1)
                if 0 <= row < self.width and 0 <= col < self.height:
                    total_cells.add((row, col))
        s = Sentence(total_cells - {cell}, count)
        if count == 0:
            for h in total_cells:
                if h != cell:
                    self.mark_safe(h)
        elif count == len(total_cells):
            for h in total_cells:
                if h != cell:
                    self.mark_mine(h)
        
        for curr_cell in s.cells.copy():
            if curr_cell in self.mines:
                s.mark_mine(curr_cell)
            elif curr_cell in self.safes:
                s.mark_safe(curr_cell)
        
        self.knowledge.append(s)

        self.update_knowledge()
    
    def update_knowledge(self):
        """
        Update the knowledge base by marking safe cells or mines
        and inferring new sentences.
        """
        updated = True
        while updated:
            updated = False
            empty_sentences = []

            # Iterate over a copy to avoid modifying the list while iterating
            for sentence in self.knowledge[:]:
                # Infer known safes and mines from the sentence
                safes = sentence.known_safes()
                mines = sentence.known_mines()
                marked = set(x for x in sentence.cells if x in self.moves_made)

                # Mark all inferred safe cells
                for safe in safes:
                    if safe not in self.safes:
                        self.mark_safe(safe)
                        updated = True

                # Mark all inferred mine cells
                for mine in mines:
                    if mine not in self.mines:
                        self.mark_mine(mine)
                        updated = True
                
                # Logic for identifying a mine based on surrounding cells
                unmarked_mines = sentence.cells - safes - marked
                if len(unmarked_mines) == sentence.count:
                    # If there is exactly count unmarked cell left, we have found mines
                    for remaining_cell in unmarked_mines:
                        self.mark_mine(remaining_cell)
                        updated = True

                # Remove the sentence if it has no more cells to infer
                if len(sentence.cells) == 0 and sentence in self.knowledge:
                    self.knowledge.remove(sentence)
                
        

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        new_safes = [x for x in self.safes if x not in self.moves_made]
        return random.choice(new_safes) if new_safes else None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        possible_moves = [
            (row, col)
            for row in range(self.width)
            for col in range(self.height)
            if (row, col) not in self.mines and (row, col) not in self.moves_made
        ]
    
        if possible_moves:
            return random.choice(possible_moves)
        return None
