
from textblob import Word

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
