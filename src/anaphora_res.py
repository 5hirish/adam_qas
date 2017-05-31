import spacy
import requests
from pprint import pprint

def get_named_entities(en_doc):

    prop_noun_entities = {}
    payload = {}
    i = 0
    for ent in en_doc.ents:
        if i < 10:
            payload["name["+str(i)+"]"] = ent.text
            print(ent.label_, ent.text)
        if i == 9:
            prop_noun_entities = get_gender(payload, prop_noun_entities)
            i = 0
        i += 1
    pprint(payload)
    if i < 10:
        prop_noun_entities = get_gender(payload, prop_noun_entities)
    return prop_noun_entities


def get_gender(payload, prop_noun_entities):
    gender_req = requests.get("https://api.genderize.io/", params=payload)
    json_gen = gender_req.json()

    for ji in range(len(json_gen)):
        prop_noun_entities[json_gen[ji]['name']] = json_gen[ji]['gender']

    return prop_noun_entities


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
prop_noun = ""

prop_noun_entities = get_named_entities(en_doc)
pprint(prop_noun_entities)

for sent in en_doc.sents:
    for token in sent:
        if token.pos_ == "PRON":
            print(token.text, token.tag_, token.dep_, prop_noun)      # PRON / PRP

        elif token.pos_ == "PROPN":

            if token.tag_ == "NNP" and token.ent_type_ == "PERSON":
                prop_noun = token.text
                prop_noun_gender = prop_noun_entities[token.text]
                print(token.text, token.tag_, token.dep_, token.ent_type_, prop_noun, prop_noun_gender)  # NNP / NNPS

            elif token.tag_ == "NNP":
                prop_noun = token.text
                payload = {"name[0]": token.text}
                prop_noun_entities = get_gender(payload, prop_noun_entities)
                prop_noun_gender = prop_noun_entities[token.text]
                print(token.text, token.tag_, token.dep_, token.ent_type_, prop_noun, prop_noun_gender)  # NNP / NNPS

            elif token.tag_ == "NNPS":
                prop_noun = token.text
                print(token.text, token.tag_, token.dep_, token.ent_type_)  # NNP / NNPS
        else:
            print(token.text, token.tag_, token.dep_, token.ent_type_)
