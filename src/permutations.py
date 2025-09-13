import itertools

from nltk.corpus import abc

# Define allowed letters for each position
positions2 = [
    ['s', 'v', 'p', 'f', 'r', 'l', 'h', 'c'],              # 1st letter
    ['u', 'h', 'l', 'r', 'a', 'e', 'i', 'o'],              # 2nd letter
    ['c', 'm', 't', 'r', 'p', 'g', 'a', 'o'],              # 3rd letter
    ['i', 'u', 's', 't', 'r', 'd', 'l', 'e'],              # 4th letter
    ['a', 'e', 'i', 'u', 't', 'r', 'l', 'h'],              # 5th letter
    ['l', 't', 'n', 'r', 's', 'e', 'z', 'h'],              # 6th letter
    ['e', 'r', 'n', 'y', 's', 'g', 'h', 'd'],              # 7th letter
]
positions =[
    ['p','t','l','s','m','w','b','c'],
    ['a','e','i','o','u','h','r','t'],
    ['v','l','r','n','t','s','o','i'],
    ['d','t','h','s','i','k','v','a'],
    ['a','e','o','n','l','r','c','s'],
    ['n','d','g','r','w','t','e','y']
]
def run():
    # Load the set of valid English words (converted to lowercase)
    english_words = set(w.lower() for w in abc.words() if len(w) == 6)

    # Generate all possible 7-letter combinations based on constraints
    possible_combinations = itertools.product(*positions)

    # Filter to valid English words
    valid_words = [''.join(letters) for letters in possible_combinations if ''.join(letters) in english_words]

    # Output (you can also write to a file if needed)
    print(f"Found {len(valid_words)} valid words:")
    for word in sorted(valid_words):
        print(word)


run()