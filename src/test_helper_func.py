from node_funcs import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes, markdown_to_blocks
import unittest
from textnode import TextNode, TextType

class TestHelperFunc(unittest.TestCase):
    def test_split_nodes(self):
        
        old_nodes = [TextNode("This is text with a `python script` term", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(old_nodes, "`", TextType.CODE)
        new_nodes2 = [TextNode('This is text with a ',TextType.TEXT, None),
                      TextNode('python script',TextType.CODE, None),
                      TextNode(' term', TextType.TEXT, None)]
        self.assertEqual(new_nodes, new_nodes2)
        
        old_nodesB = [TextNode("`PYTHON SCRIPT` with also some **boldy text** lets go!", TextType.TEXT)]
        new_nodesB = split_nodes_delimiter(old_nodesB, "`", TextType.CODE)
        new_nodesB2 = [TextNode('PYTHON SCRIPT',TextType.CODE, None),
                      TextNode(' with also some **boldy text** lets go!',TextType.TEXT, None)]
        self.assertEqual(new_nodesB, new_nodesB2)
        new_nodesC = split_nodes_delimiter(old_nodesB, '**', TextType.BOLD)
        new_nodesC2 = [TextNode("`PYTHON SCRIPT` with also some ",TextType.TEXT, None),
                      TextNode('boldy text',TextType.BOLD, None),
                      TextNode(" lets go!",TextType.TEXT, None)]
        self.assertEqual(new_nodesC, new_nodesC2)
    
    def test_re_link_and_img(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
        
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another img too ![image](https://imaginarylink.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png"), ("image", "https://imaginarylink.png")], matches)
        
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
            )
        self.assertEqual([("to boot dev","https://www.boot.dev" ),("to youtube","https://www.youtube.com/@bootdotdev")], matches)
        
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
    def test_split_link(self):
        node = TextNode(
            "Now this one has regular links and here they go [zelda](www.nintendo.com) and another [ganon](www.wario.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Now this one has regular links and here they go ", TextType.TEXT),
                TextNode("zelda", TextType.LINK, "www.nintendo.com"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "ganon", TextType.LINK, "www.wario.com"
                ),
            ],
            new_nodes,
        )
    
    def test_split_images2(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png) and then more text maybe",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
                TextNode(" and then more text maybe", TextType.TEXT),
            ],
            new_nodes,
        )
    
    def test_text_to_textnodes(self):
        nodes = text_to_textnodes("This is **bold** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)")
        self.assertListEqual(nodes,
                             [
                                TextNode("This is ", TextType.TEXT),
                                TextNode("bold", TextType.BOLD),
                                TextNode(" with an ", TextType.TEXT),
                                TextNode("italic", TextType.ITALIC),
                                TextNode(" word and a ", TextType.TEXT),
                                TextNode("code block", TextType.CODE),
                                TextNode(" and an ", TextType.TEXT),
                                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                                TextNode(" and a ", TextType.TEXT),
                                TextNode("link", TextType.LINK, "https://boot.dev"),
                            ])
        
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
        
if __name__ == "__main__":
    unittest.main()