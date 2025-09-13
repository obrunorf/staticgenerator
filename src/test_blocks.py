import unittest
from blocks import BlockType, block_to_blocktype, markdown_to_html_node

class TestBlocks(unittest.TestCase):
    def test_block_to_blocktype(self):
        s = 'teste teste testado sem nada'
        self.assertEqual(block_to_blocktype(s), BlockType.PARAGRAPH)
        
        s = '```codigozao da massa```'
        self.assertEqual(block_to_blocktype(s), BlockType.CODE)
        
        s = """1. primeiro\n2. segundo\n3. terceiro"""
        self.assertEqual(block_to_blocktype(s), BlockType.ORDRED_LIST)
        
        s = """- teste\n- desordado\n- maluco beleza"""
        self.assertEqual(block_to_blocktype(s), BlockType.UNORDERED_LIST)
        
        s = """> teste\n>desordenado\n> maluco beleza"""
        self.assertEqual(block_to_blocktype(s), BlockType.QUOTE)
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        print(html)
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )
        
        
if __name__ == "__main__":
    unittest.main()