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
        self.next = start

    def __next__(self):
        """
        Iterate through the nodes left or right.
        :return: Each node in the list.
        """
        if self.right:
            self.next = self.next.right
        else:
            self.next = self.next.bottom
        if self.next is self.start:
            raise StopIteration
        return self.next

    def __iter__(self):
        return self

class DancingNode:
    """A quadrubably linked node."""
    def __init__(self, index=0):
        self.left = self.right = self.bottom = self.top = self
        self.index = index
        self.column_head = False

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
        header = self.get_column()
        header.size -= 1
        self.top.bottom = self.bottom
        self.bottom.top = self.top

    def remove_row(self):
        self.remove_vertical()
        for node in NodeIterator(self, True):
            node.remove_vertical()

    def restore_horizontal(self):
        self.left.right = self
        self.right.left = self

    def restore_vertical(self):
        self.top.bottom = self
        self.bottom.top = self

    def restore_row(self):
        self.restore_vertical()
        for node in NodeIterator(self, True):
            node.restore_vertical()

    def get_column(self, i=0):
        i += 1
        if self.column_head:
            return self
        else:
            return self.bottom.get_column(i)

class DancingColumn(DancingNode):
    def __init__(self, index):
        DancingNode.__init__(self, index)
        self.size = 0
        self.tried = []
        self.column_head = True

    def link_bottom(self, bottom):
        DancingNode.link_bottom(self, bottom)
        self.size += 1

    def remove_rows(self):
        """
        For each DancingNode in this column, remove the row they represent from the matrix.
        :return: None
        """
        i = 0
        for row in NodeIterator(self, False):
            i += 1
            row.remove_row()

    def restore_rows(self):
        """
        For each DancingNode in this column, restore the row they represent back into the matrix.
        :return: None
        """
        for row in NodeIterator(self, False):
            row.restore_row()

    def select(self):
        """
        Select a row from this column and use it to reduce the matrix.
        :return: True if Matrix successfully reduced
        False if Matrix unsuccessfully reduced
        """
        row = random.randrange(self.size)
        chosen = None
        for choose in NodeIterator(self, False):
            if choose not in self.tried:
                chosen = choose
        if chosen is None:
            return False
        self.tried.append(choose)
        print(self.index)
        #Get each of the columns this row belongs to.
        self.remove_horizontal()
        self.remove_rows()
        for value, node in enumerate(NodeIterator(choose, True)):
            head = node.get_column()
            head.remove_horizontal()
            head.remove_rows()
        return True

    def reverse(self):
        selected = self.tried[-1]
        self.restore_horizontal()
        self.restore_rows()
        for node in NodeIterator(selected, True):
            head = node.get_column()
            head.restore_horizontal()
            head.restore_rows()



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
            self.header.link_left(col)
        for i in range(size ** 3):
            row = [DancingNode(i), DancingNode(i), DancingNode(i), DancingNode(i)]
            row[0].link_right(row[1])
            row[1].link_right(row[2])
            row[2].link_right(row[3])
            for node, constraint in enumerate(self.get_constraints(i)):
                self.cols[constraint].link_bottom(row[node])

    def knuth_algorithm(self):
        while self.header.right is not self.header:
            col = self.choose_column()
            if not col.select():
                print("BACKTRACK!")
                self.backtrack()
            self.select.append(col)

    def backtrack(self):
        col = self.select[-1]
        col.reverse()
        self.select.remove(col)
        if not col.select():
            self.backtrack()
        self.select.append(col)

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