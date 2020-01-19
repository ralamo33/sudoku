import collections
import math
import random

class NodeIterator:
    def __init__(self, start, right):
        """
        Iterate through the nodes in a row or column.
        :param start: The starting node.
        :param right: True if you are iterating through the right. Otherwise you iteate from the bottom.
        """
        self.start = start
        self.right = right
        if right:
            self.next = start.right
        else:
            self.next = start.bottom

    def __next__(self):
        """
        Iterate through the nodes left or right.
        :return: Each node in the list.
        """
        if self.next is self.start:
            raise StopIteration
        elif self.right:
            return self.next.right
        else:
            return self.next.bottom

    def __iter__(self):
        return self

class DancingNode:
    """A quadrably linked node."""
    def __init__(self, index=0):
        self.left = self.right = self.bottom = self.top = self
        self.index = index

    def link_top(self, top):
        top.bottom = self
        top.top = self.top
        self.top.bottom = top
        self.top = top
        
    def link_bottom(self, bottom):
        bottom.top = self
        bottom.bottom = self.bottom
        self.bottom.top = bottom
        self.bottom = bottom
        
    def link_left(self, left):
        left.right = self
        left.left = self.left
        self.left.right = left
        self.left = left
        
    def link_right(self, right):
        right.left = self
        right.right = self.right
        self.right.left = right
        self.right = right

    def remove_horizontal(self):
        self.left.right = self.right
        self.right.left = self.left

    def remove_vertical(self):
        self.top.bottom = self.bottom
        self.bottom.top = self.top

    def restore_horizontal(self):
        self.left.right = self
        self.right.left = self

    def restore_vertical(self):
        self.top.bottom = self
        self.bottom.top = self


class DancingColumn:
    def __init__(self, index):
        self.index = index
        self.size = 0
        self.dancing_link = DancingNode()
        self.tried = []

    def link_bottom(self, node):
        self.dancing_link.link_bottom(node)
        self.size += 1

    def link_top(self, node):
        self.dancing_link.link_top(node)
        self.size += 1

    def link_right(self, node):
        self.dancing_link.link_right(node)

    def link_left(self, node):
        self.dancing_link.link_left(node)

    def select(self):
        row = random.randrange(self.size)
        choose = self.dancing_link
        if len(self.tried) == self.size:
            return False
        while choose in self.tried or choose is self.dancing_link:
            choose = choose.bottom
        self.tried.append(choose)
        """#Get each of the columns this row belongs to.
        for column in NodeIterator(choose, True):
            #Remove each column from the Matrix
            for column_nodes in NodeIterator(column, False):
                column.remove_horizontal()
                #For each node of the eliminated column. Remove the entire row.
                for eliminate_row in NodeIterator(eliminate_col, True)
                    eliminate_row.remove_vertical()"""
        return True
        

    def remove(self):
        """Remove this column from the dancing matrix."""
        self.dancing_link.remove_horizontal()
        below = self.dancing_link.bottom
        while below is not self:
            below.remove_horizontal()
            below = below.bottom

    def restore(self):
        """Restore this colun back into the dancing matrix."""
        self.dancing_link



class LinkedMatrix:
    """A matrix of dancing links representing a Sodou board converted into an exact cover problem."""
    def __init__(self, size=9):
        """
        :param size: The size of a side of the Soduku board.
        """
        self.size = size
        self.submatrix = math.sqrt(self.size)
        self.constraint_length = self.size ** 2
        self.header = DancingNode()
        self.cols = []
        self.select = []
        for i in range(((size ** 2) * 4)):
            col = DancingColumn(i)
            self.cols.append(col)
            self.header.link_left(col.dancing_link)
        for i in range(size ** 3):
            for constraint in self.get_constraints(i):
                self.cols[constraint].link_bottom(DancingNode(i))

    def knuth_algorithm(self):
        while self.header.right is not self.header:
            col = self.choose_column()
            if not col.select():
               self.backtrack()

    def backtrack(self):
        col = self.select[-1]
        col.reverse()

    def choose_column(self):
        min_size = 100
        options = []
        for col in self.cols:
            if col.size < min_size:
                min_size = col.size
                options.append(col)
            elif col.size == min_size:
                options.append(col)
        return options[random.randrange(len(options))]


    def get_constraints(self, index):
        """Return the indices of the KnuthColumns active in this."""
        row = math.floor(index / (self.size ** 2))
        col = math.floor((index % (self.size ** 2)) / self.size)
        num = index % self.size + 1
        return (self._cell_constraints(row, col), self._row_constraints(row, num),
               self._column_constraints(col, num), self._submatrix_constraints(row, col, num))

    def _cell_constraints(self, row, col):
        """Return the knuth column activated by this row's row-number-column constraints
        :return int"""
        return row * self.size + col

    def _row_constraints(self, row, num):
        """Return the knuth column activated by this row's row-number-column constraints
        :return int"""
        return self.constraint_length + num + (row * self.size) - 1

    def _column_constraints(self, col, num):
        """Return the knuth column activated by this row's row-number-column constraints
        :return int"""
        return (self.constraint_length * 2) + num + col * self.size - 1

    def _submatrix_constraints(self, row, col, num):
        """Return the knuth column activated by this row's row-number-column constraints
        :return int"""
        box = ((math.floor(row / self.submatrix)) * self.submatrix) + math.floor(col / self.submatrix)
        return int((self.constraint_length * self.submatrix) + (box * self.size) + num) - 1





if __name__ == "__main__":
    pass