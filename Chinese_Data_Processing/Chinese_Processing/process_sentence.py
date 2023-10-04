import json
import pickle
import re
import jieba.posseg as pseg

review_path = 'reviews.pickle'  # resulting from format_amazon.py
sentence_path = 'sentences.pickle'  # path to save sentences
test_sentences_path = 'test_sentences.json'

def get_sentences(string):
    string = re.sub('[，。？！\n]', '。', string)
    sentences = [sent.strip() for sent in string.split('。') if sent.strip() != '']
    return sentences

def get_sentence_attr(string):
    pronoun_num = 0  # 人称代词数量
    noun_num = 0  # 名词数量
    adj_num = 0  # 形容词数量
    pronoun_tags = ["r", "rr", "rz", "ry", "rys"]

    # 使用jieba进行分词和词性标注
    word_pos_list = pseg.cut(string)
    word_num = len(string)

    for word, pos in word_pos_list:
        if pos in pronoun_tags:
            pronoun_num += 1
        elif pos.startswith("n"):  # 以'n'开头的是名词
            noun_num += 1
        elif pos.startswith("a"):  # 以'a'开头的是形容词
            adj_num += 1
    return word_num, pronoun_num, noun_num, adj_num

reviews = pickle.load(open(review_path, 'rb'))
sentences = []
for idx, review in enumerate(reviews):
    text = review['text']
    exps = get_sentences(text)
    for exp in exps:
        word_n, pronoun_n, noun_n, adj_n = get_sentence_attr(exp)
        sentence = {
            'review_idx': idx,
            'exp': exp,
            'word_num': word_n,
            'pronoun_num': pronoun_n,
            'noun_num': noun_n,
            'adj_num': adj_n,
        }
        sentences.append(sentence)

with open(test_sentences_path, 'w', encoding='utf-8') as json_file:
    json.dump(sentences, json_file, indent=4, ensure_ascii=False)
pickle.dump(sentences, open(sentence_path, 'wb'))

