import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        err = "err: empty node"
        node  = HTMLNode("p", "textinhozinho de testerino")
        node2 = HTMLNode("p", "textinhozinho de testerino")
        self.assertEqual(repr(node), repr(node2))
        node2.props ={
        "href": "https://www.google.com",
        "target": "_blank",}
        """print("Node 1")
        print(node)
        print("Node 2")
        print(node2)
        print("Props to html")
        print(node2.props_to_html())"""
        self.assertNotEqual(repr(node), repr(node2))
        
        empty = HTMLNode()
        self.assertEqual(repr(empty), err)
        
        
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
        
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
        
        

if __name__ == "__main__":
    unittest.main()