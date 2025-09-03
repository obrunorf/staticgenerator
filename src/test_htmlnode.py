import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        err = "err: empty node"
        node  = HTMLNode("p", "textinhozinho de testerino")
        node2 = HTMLNode("p", "textinhozinho de testerino")
        self.assertEqual(repr(node), repr(node2))
        node2.props ={
        "href": "https://www.google.com",
        "target": "_blank",}
        print("Node 1")
        print(node)
        print("Node 2")
        print(node2)
        print("Props to html")
        print(node2.props_to_html())
        self.assertNotEqual(repr(node), repr(node2))
        
        empty = HTMLNode()
        self.assertEqual(repr(empty), err)
        

if __name__ == "__main__":
    unittest.main()