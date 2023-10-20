import json
import re

def get_sentences(string):
    string = re.sub('[，。？！、 \n \s , . ! ~ ~ ～]', '。', string)
    sentences = [sent.strip() for sent in string.split('。') if sent.strip() != '']
    return sentences

with open('../result/extract.json', 'r', encoding='utf8') as fp:
    reviews = json.load(fp)

sentences = []

idx2 = 0
for idx, review in enumerate(reviews):
    text = review['review']
    exps = get_sentences(text)
    for exp in exps:
        word_num = len(exp)
        sentence = {
            'review_idx': idx,
            'every_idx': idx2,
            'exp': exp,
            'word_num': word_num
        }
        idx2 += 1
        sentences.append(sentence)
with open('../result/sentences_separate.json', 'w', encoding='utf-8') as json_file:
    json.dump(sentences, json_file, indent=4, ensure_ascii=False)