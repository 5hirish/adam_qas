import spacy

sentence = "Louie is a quite fellow." \
           " But that didn't mean he will endure anything." \
           " Samantha loves this about him." \
           " Why wouldn't she?"

pronouns = ["i", "you", "he", "she", "it", "we", "they", "me", "him", "her", "us", "them"]

first_person_pron = ["i", "me"]
second_person_pron = ["you"]
third_person_pron = [["he", "him"], ["she", "her"], ["it"]]     # M - F - N

first_person_plu_pron = ["we", "us"]
second_person_plu_pron = ["you"]
third_person_plu_pron = ["they", "them"]

en_nlp = spacy.load('en_core_web_md')

en_doc = en_nlp(u'' + sentence)
anaphora = ""

for sent in en_doc.sents:
    for token in sent:
        if token.pos_ == "PRON":
            print(token.text, token.tag_, token.dep_, anaphora)      # PRON / PRP

        elif token.pos_ == "PROPN":

            if token.tag_ == "NNP" and token.ent_type_ == "PERSON":
                anaphora = token.text
                print(token.text, token.tag_, token.dep_, token.ent_type_)  # NNP / NNPS

            elif token.tag_ == "NNPS":
                anaphora = token.text
                print(token.text, token.tag_, token.dep_, token.ent_type_)  # NNP / NNPS
        else:
            print(token.text, token.tag_, token.dep_, token.ent_type_)
