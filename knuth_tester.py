import unittest
from solver import *

class MyTestCase(unittest.TestCase):


    def test_select(self):
        matrix = LinkedMatrix()
        chosen = matrix.cols[0]
        chosen.select(chosen.get_row())
        self.assertNotEqual(matrix.header.right, chosen)
        self.assertTrue(chosen.left.right, chosen.right)
        self.assertTrue(chosen.right.left, chosen.left)
        for row in NodeIterator(chosen, False):
            for i, node in enumerate(NodeIterator(row, True)):
                self.assertTrue(node.top.bottom, node.bottom)
                self.assertTrue(node.bottom.top, node.top)
        for size, col in enumerate(NodeIterator(matrix.header, True)):
            s = size
        self.assertEqual(319, s)
        chosen.reverse()
        for size, col in enumerate(NodeIterator(matrix.header, True)):
            s = size
        self.assertEqual(323, s)
        for col in NodeIterator(matrix.header, True):
            si = 0
            for size, row in enumerate(NodeIterator(col, False)):
                si = size
            print(col.index)
            self.assertEqual(si, 8)

    def test_header(self):
        matrix = LinkedMatrix()
        self.assertEqual(matrix.header.right, matrix.cols[0])
        self.assertEqual(matrix.header.left, matrix.cols[-1])
        next = matrix.header.right
        for col in matrix.cols:
            self.assertEqual(col, next)
            next = next.right



    def test_linked_matrix(self):
        matrix = LinkedMatrix()
        self.assertEqual(324, len(matrix.cols))
        for col in matrix.cols:
            self.assertEqual(9, col.size)
            next = col.bottom
            for i in range(8):
                next = next.bottom
            self.assertEqual(col.top, next)

    def test_get_row(self):
        m = LinkedMatrix()
        col = m.cols[0]
        for i in range(9):
            row = col.get_row()
            self.assertIsNotNone(row)
            col.select(row)
            col.reverse()
        self.assertIsNone(col.get_row())

    def test_reverse(self):
        m = LinkedMatrix()
        for i in range(100):
            col = m.cols[random.randrange(324)]
            col.select(col.get_row())
            col.reverse()
            self.assertEqual(324, len(m.cols))
            for col in m.cols:
                self.assertEqual(8, col.get_size())


    def test_speed(self):
        m = LinkedMatrix()
        m.knuth_algorithm()

    def test_matrix_solved(self):
        matrix = LinkedMatrix()
        self.solve_matrix(matrix, 3, 1)
        self.solve_matrix(matrix, 6, 2)
        self.solve_matrix(matrix, 9, 3)
        self.assertTrue(matrix.header.right is matrix.header)

    def solve_matrix(self, matrix, row_limit, num):
        for row in range((row_limit - 3), row_limit):
            col_num = num
            for col in range(9):
                row_index = self.translate_header_to_index(row, col, col_num)
                figured = False
                for col2 in matrix.cols:
                    for node in NodeIterator(col2, False):
                        if node.index == row_index:
                            figured = True
                            chosen_col = col2
                            chosen_row = node
                            break
                    if figured:
                        break
                col2.select(chosen_row)
                col_num = (col_num % 9) + 1
            num += 3

    def translate_header_to_index(self, row, col, num):
        index = row * 81 + col * 9 + num - 1
        return index

    def test_select_solution(self, rindex, cindex):
        m = LinkedMatrix
        col = m.cols[cindex]
        for rows in NodeIterator(col, False):
            if rows.index == rindex:
                row = rows
        col.select(rows)

    def test_dancing_col(self):
        dc = DancingColumn(1)
        dn = DancingNode(2)
        dn2 = DancingNode(3)
        dn3 = DancingNode(4)
        dn4 = DancingNode(5)
        dc.link_bottom(dn)
        self.assertEqual(dc.size, 1)
        self.assertEqual(dc.bottom, dn)
        self.assertEqual(dc.top, dn)
        dc.link_bottom(dn2)
        dc.link_bottom(dn3)
        dc.link_bottom(dn4)
        self.assertEqual(dc.size, 4)
        next = dc.bottom
        self.assertEqual(next, dn4)
        next = next.bottom
        self.assertEqual(next, dn3)
        next = next.bottom
        self.assertEqual(next, dn2)
        next = next.bottom
        self.assertEqual(next, dn)
        self.assertEqual(dc.top, dn)




    def test_dancing_node(self):
        node1 = DancingNode(1)
        node2 = DancingNode(2)
        node3 = DancingNode(3)
        node4 = DancingNode(4)
        node4.link_left(node3)
        node3.link_left(node2)
        node2.link_left(node1)
        self.assertEqual(node1.left, node4)
        self.assertEqual(node1.right, node2)
        self.assertEqual(node2.right, node3)
        self.assertEqual(node3.right, node4)
        self.assertEqual(node4.left, node3)
        self.assertEqual(node2.left, node1)
        self.assertEqual(node3.left, node2)
        node4.link_bottom(node3)
        node3.link_bottom(node2)
        node2.link_bottom(node1)
        self.assertEqual(node1.bottom, node4)
        self.assertEqual(node1.top, node2)
        self.assertEqual(node2.top, node3)
        self.assertEqual(node3.top, node4)
        self.assertEqual(node4.bottom, node3)
        self.assertEqual(node2.bottom, node1)
        self.assertEqual(node3.bottom, node2)


    def test_dancing_node2(self):
        node1 = DancingNode(1)
        node2 = DancingNode(2)
        node3 = DancingNode(3)
        node4 = DancingNode(4)
        node1.link_right(node2)
        node2.link_right(node3)
        node3.link_right(node4)
        self.assertEqual(node1.left, node4)
        self.assertEqual(node1.right, node2)
        self.assertEqual(node2.right, node3)
        self.assertEqual(node3.right, node4)
        self.assertEqual(node4.left, node3)
        self.assertEqual(node2.left, node1)
        self.assertEqual(node3.left, node2)
        node1.remove_horizontal()
        self.assertEqual(node2.left, node4)
        self.assertEqual(node4.right, node2)
        node2.remove_horizontal()
        self.assertEqual(node4.right, node3)
        self.assertEqual(node4.left, node3)
        self.assertEqual(node3.left, node4)
        self.assertEqual(node3.right, node4)
        node3.remove_horizontal()
        self.assertEqual(node4.left, node4)
        self.assertEqual(node4.left, node4)
        node4.remove_horizontal()
        self.assertEqual(node1.left, node4)
        self.assertEqual(node1.right, node2)
        self.assertEqual(node2.left, node4)
        self.assertEqual(node2.right, node3)
        self.assertEqual(node3.left, node4)
        self.assertEqual(node3.right, node4)
        self.assertEqual(node4.left, node4)
        self.assertEqual(node4.right, node4)
        node1.restore_horizontal()
        node2.restore_horizontal()
        node3.restore_horizontal()
        node4.restore_horizontal()
        self.assertEqual(node1.left, node4)
        self.assertEqual(node1.right, node2)
        self.assertEqual(node2.right, node3)
        self.assertEqual(node3.right, node4)
        self.assertEqual(node4.left, node3)
        self.assertEqual(node2.left, node1)
        self.assertEqual(node3.left, node2)
        node1.link_top(node2)
        node2.link_top(node3)
        node3.link_top(node4)
        self.assertEqual(node1.bottom, node4)
        self.assertEqual(node1.top, node2)
        self.assertEqual(node2.top, node3)
        self.assertEqual(node3.top, node4)
        self.assertEqual(node4.bottom, node3)
        self.assertEqual(node2.bottom, node1)
        self.assertEqual(node3.bottom, node2)
        node1.remove_vertical()
        self.assertEqual(node2.bottom, node4)
        self.assertEqual(node4.top, node2)
        node2.remove_vertical()
        self.assertEqual(node4.top, node3)
        self.assertEqual(node4.bottom, node3)
        self.assertEqual(node3.bottom, node4)
        self.assertEqual(node3.top, node4)
        node3.remove_vertical()
        self.assertEqual(node4.bottom, node4)
        self.assertEqual(node4.bottom, node4)
        node4.remove_vertical()
        self.assertEqual(node1.bottom, node4)
        self.assertEqual(node1.top, node2)
        self.assertEqual(node2.bottom, node4)
        self.assertEqual(node2.top, node3)
        self.assertEqual(node3.bottom, node4)
        self.assertEqual(node3.top, node4)
        self.assertEqual(node4.bottom, node4)
        self.assertEqual(node4.top, node4)
        node1.restore_vertical()
        node2.restore_vertical()
        node3.restore_vertical()
        node4.restore_vertical()
        self.assertEqual(node1.bottom, node4)
        self.assertEqual(node1.top, node2)
        self.assertEqual(node2.top, node3)
        self.assertEqual(node3.top, node4)
        self.assertEqual(node4.bottom, node3)
        self.assertEqual(node2.bottom, node1)
        self.assertEqual(node3.bottom, node2)





if __name__ == '__main__':
    unittest.main()
