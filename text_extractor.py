import json

with open("corpus_ncom.json", "r", encoding="utf-8") as f1:
        data1 = json.load(f1)
with open("corpus_ncorp.json", "r", encoding="utf-8") as f2:
    data2 = json.load(f2)

f = open('texts.txt', 'w', encoding='utf-8')

for subcorp in data1["subcorpora"]:
    for text in subcorp["texts"]:
         
        #  print(text["text"]["content"])
         f.write(text["text"]["content"])

for subcorp in data2["subcorpora"]:
    if subcorp["corpus"]["Название"] == "Рабочая версия":
        for subcorp1 in subcorp["subcorpora"]:
            for subcorp2 in subcorp1["subcorpora"]:
                 for text in subcorp2["texts"]:
                    # print(text["text"]["content"])
                    f.write(text["text"]["content"])