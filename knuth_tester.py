import unittest
from solver import *

class MyTestCase(unittest.TestCase):

    def test_header(self):
        matrix = LinkedMatrix()
        self.assertEqual(matrix.header.right, matrix.cols[0].dancing_link)
        self.assertEqual(matrix.header.left, matrix.cols[-1].dancing_link)
        next = matrix.header.right
        for col in matrix.cols:
            self.assertEqual(col.dancing_link, next)
            next = next.right



    def test_linked_matrix(self):
        matrix = LinkedMatrix()
        self.assertEqual(324, len(matrix.cols))
        for col in matrix.cols:
            self.assertEqual(9, col.size)
            next = col.dancing_link.bottom
            for i in range(8):
                next = next.bottom
            self.assertEqual(col.dancing_link.top, next)

    def test_speed(self):
        m = LinkedMatrix()
        for i in range(100):
            m.cols[i].select()


    def test_dancing_col(self):
        dc = DancingColumn(1)
        dn = DancingNode(2)
        dn2 = DancingNode(3)
        dn3 = DancingNode(4)
        dn4 = DancingNode(5)
        dc.link_bottom(dn)
        self.assertEqual(dc.size, 1)
        self.assertEqual(dc.dancing_link.bottom, dn)
        self.assertEqual(dc.dancing_link.top, dn)
        dc.link_bottom(dn2)
        dc.link_bottom(dn3)
        dc.link_bottom(dn4)
        self.assertEqual(dc.size, 4)
        next = dc.dancing_link.bottom
        self.assertEqual(next, dn4)
        next = next.bottom
        self.assertEqual(next, dn3)
        next = next.bottom
        self.assertEqual(next, dn2)
        next = next.bottom
        self.assertEqual(next, dn)
        self.assertEqual(dc.dancing_link.top, dn)




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
