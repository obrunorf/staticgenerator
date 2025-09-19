import unittest

from generator import *

class TestGenerator(unittest.TestCase):
    def test_extract_title(self):
        mkd ="# this is the title one"
        title = extract_title(mkd)
        self.assertEqual(title, "this is the title one")
        
        mkd2 = """meu sacao roxo se pa
# o titulo esta aqui
## titular falso irairair 
#titulo errado tb"""
        title = extract_title(mkd2)
        self.assertEqual(title, "o titulo esta aqui")
if __name__ == "__main__":
    unittest.main()