
from textblob import Word
from textblob.wordnet import Synset

"""--------------- TextBlob --------------"""

word = Word('plant')

# A synonym set, or synset, is a group of synonyms.

for i in range(len(word.synsets)):
    # The synonyms contained within a synset are called lemmas.
    lemmas = word.synsets[i]
    # hyponyms are the synsets that are more specific

    # Hyponyms have an "is-a" relationship to their hypernyms.
    print(word.synsets[i], " = ", word.definitions[i], ">", lemmas.hypernyms())
    # hypernyms are the synsets that are more general
    print(lemmas.hyponyms()[:3])
    # holonyms are things that the item is contained in
    # meronyms are components or substances that make up the item
    print(lemmas.member_holonyms())
    print(lemmas.part_meronyms())

"""
    Given that synsets can be organized as a graph, as shown above, we can measure the similarity of synsets based on
    the shortest path between them.
    This is called the path similarity, and it is equal to 1 / (shortest_path_distance(synset1, synset2) + 1).
    It ranges from 0.0 (least similar) to 1.0 (identical).
"""

rootword = Synset("tiger.n.02")
predator = Synset('lion.n.01')
mammal = Synset('cat.n.01')
reptile = Synset('snake.n.01')
organ = Synset('heart.n.02')

similar = {
            rootword: rootword.path_similarity(rootword),
            predator: rootword.path_similarity(predator),
            mammal: rootword.path_similarity(mammal),
            reptile: rootword.path_similarity(reptile),
            organ: rootword.path_similarity(organ)
        }

print(rootword,">>",similar)