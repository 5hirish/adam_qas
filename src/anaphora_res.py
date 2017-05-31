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


def get_noun_chunks(en_doc, prop_noun_entities):
    payload = {}
    i = 0
    for noun in en_doc.noun_chunks:
        if i < 10:
            payload["name[" + str(i) + "]"] = noun.text
            print(noun.label_, noun.text)
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


def map_entity_pronoun(prop_noun_entities, entity, anaphora_mappings):
    pronouns = ["i", "you", "he", "she", "it", "we", "they", "me", "him", "her", "us", "them"]

    first_person_pron = ["i", "me", "my", "mine"]
    second_person_pron = ["you", "your"]
    third_person_pron = [["he", "him", "his"], ["she", "her", "hers"], ["it"]]  # M - F - N

    first_person_plu_pron = ["we", "us", "our", "ours"]
    second_person_plu_pron = ["you", "yours"]
    third_person_plu_pron = ["they", "them", "their", "theirs"]

    gender = prop_noun_entities[entity]

    if gender == 'male':
        anaphora_mappings[entity] = first_person_pron + second_person_pron + third_person_pron[0]
    elif gender == 'female':
        anaphora_mappings[entity] = first_person_pron + second_person_pron + third_person_pron[1]
    else:
        anaphora_mappings[entity] = third_person_pron[2]
    return anaphora_mappings


sentence = "Louie is a quite fellow." \
           " But that doesn't mean he will endure anything." \
           " Samantha loves this about him." \
           " Why wouldn't she?" \
           " Her whole childhood was under his shadow."

en_nlp = spacy.load('en_core_web_md')

en_doc = en_nlp(u'' + sentence)
prop_noun = ""
anaphora_mappings = {}

prop_noun_entities = get_named_entities(en_doc)
# prop_noun_entities = get_noun_chunks(en_doc, prop_noun_entities)

for entity in prop_noun_entities.keys():
    anaphora_mappings = map_entity_pronoun(prop_noun_entities, entity, anaphora_mappings)
# pprint(prop_noun_entities)
pprint(anaphora_mappings)


for sent in en_doc.sents:
    for token in sent:
        if token.tag_ == "PRP" or token.tag_ == "PRP$":
            print(token.text, token.tag_, token.dep_, "---")      # PRON / PRP Propagation

        elif token.pos_ == "PROPN":

            if token.tag_ == "NNP":
                prop_noun = token.text
                payload = {"name[0]": token.text}
                prop_noun_entities = get_gender(payload, prop_noun_entities)
                prop_noun_gender = prop_noun_entities[token.text]
                anaphora_mappings = map_entity_pronoun(prop_noun_entities, prop_noun, anaphora_mappings)
                print(token.text, token.tag_, token.dep_, token.ent_type_, prop_noun, prop_noun_gender)  # NNP / NNPS

            elif token.tag_ == "NNPS":
                prop_noun = token.text
                print(token.text, token.tag_, token.dep_, token.ent_type_)  # NNP / NNPS
        else:
            print(token.text, token.tag_, token.dep_, token.ent_type_)


pprint(anaphora_mappings)