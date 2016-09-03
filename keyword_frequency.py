import json
from collections import Counter

def normalize_word(word):
    # Nornalize to lowercase
    word = word.lower()
    # Remove trailing comas or dots
    word = word.rstrip('-.,;*()/\\')
    word = word.lstrip('-,;*()/\\')
    return word

# Get words
words = open('./jobtitles.txt').read().split()
normalized_words = [normalize_word(word) for word in words]

# Frequency
counter = Counter(normalized_words)

for word, freq in counter.most_common():
    print("%d %s" % (freq, word))
