import spacy
import requests


def get_gender(prop_noun):
    gender_req = requests.get("https://api.genderize.io/?name="+prop_noun)
    json_gen = gender_req.json()
    return json_gen['gender']


sentence = "Louie is a quite fellow." \
           " But that didn't mean he will endure anything." \
           " Google loves this about him." \
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
prop_noun = ""



for sent in en_doc.sents:
    for token in sent:
        if token.pos_ == "PRON":
            print(token.text, token.tag_, token.dep_, prop_noun)      # PRON / PRP

        elif token.pos_ == "PROPN":

            if token.tag_ == "NNP" and token.ent_type_ == "PERSON":
                prop_noun = token.text
                prop_noun_gender = get_gender(prop_noun)
                print(token.text, token.tag_, token.dep_, token.ent_type_, prop_noun, prop_noun_gender)  # NNP / NNPS

            elif token.tag_ == "NNP":
                prop_noun = token.text
                prop_noun_gender = get_gender(prop_noun)
                print(token.text, token.tag_, token.dep_, token.ent_type_, prop_noun, prop_noun_gender)  # NNP / NNPS

            elif token.tag_ == "NNPS":
                prop_noun = token.text
                print(token.text, token.tag_, token.dep_, token.ent_type_)  # NNP / NNPS
        else:
            print(token.text, token.tag_, token.dep_, token.ent_type_)
