import unittest

from textnode import TextNode, TextType
from node_funcs import text_node_to_html_node

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
        
        node3 = TextNode("This is a italic node", TextType.ITALIC)
        node4 = TextNode("This is a link node", TextType.LINK, "google.com")
        node5 = TextNode("This is a link node", TextType.LINK)
        node6 = TextNode("This is a broken link node", TextType.LINK, "google.com")
        node7 = TextNode("This is a link node", TextType.LINK, None)
        self.assertNotEqual(node3, node4)
        self.assertNotEqual(node, node4)
        self.assertNotEqual(node4, node6)
        self.assertNotEqual(node4, node5)
        self.assertEqual(node5, node7)
        
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
        
        node2 = TextNode("This is an img node", TextType.IMAGE, url="http://imagem.png")
        html_node2 = text_node_to_html_node(node2)
        print(html_node2)
        

if __name__ == "__main__":
    unittest.main()