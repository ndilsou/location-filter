import spacy
import html

nlp = spacy.load('en_core_web_md')
title = nlp(html.unescape(u"Meet the 12 new bombshells poised to join Love Island"))
doc = nlp(html.unescape(u"."))

main_entities = []
for ent in title.ents:
    if ent.label_ in ["GPE"]:
        print(ent.text, ent.label_)
        main_entities.append(ent)

for ent in doc.ents:
    if ent.label_ in ["GPE", "ORG", "LOC", "FAC"]:
        print(ent.text, ent.label_, [(ment.text, ment.similarity(ent)) for ment in main_entities])
