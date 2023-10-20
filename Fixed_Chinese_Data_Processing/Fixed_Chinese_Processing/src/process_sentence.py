import json
import pickle
import re
import jieba
import jieba.posseg as pseg
import thulac

review_path = '../result/reviews.pickle'  # resulting from format_amazon.py
sentence_path = '../result/sentences.pickle'  # path to save sentences
test_sentences_path = '../result/test_sentences.json'
connect_sentense_path = '../connect_sentense.pickle'

# 使用jieba库进行词性标注
def get_sentence_attr(string):
    pronoun_num = 0  # 人称代词数量
    noun_num = 0  # 名词数量
    adj_num = 0  # 形容词数量
    pronoun_tags = ["r", "rr", "rz", "ry", "rys"]

    # 先分词
    word_pos_list = pseg.cut(string)
    word_num = len(string)

    # 再词性标注
    for word, pos in word_pos_list:
        if pos in pronoun_tags:
            pronoun_num += 1
        elif pos.startswith("n"):  # 以'n'开头的是名词
            noun_num += 1
        elif pos.startswith("a"):  # 以'a'开头的是形容词
            adj_num += 1
    return word_num, pronoun_num, noun_num, adj_num
sentences = []

reviews = pickle.load(open(connect_sentense_path, 'rb'))

for idx, review in enumerate(reviews):
    row_exp = review['row_exp']
    processed_exp = review['processed_exp']
    review_idx = review['review_idx']

    word_n, pronoun_n, noun_n, adj_n = get_sentence_attr(processed_exp)

    sentence = {
        'review_idx': review_idx,
        'row_exp': row_exp,
        'processed_exp': processed_exp,
        'word_num': word_n,
        'pronoun_num': pronoun_n,
        'noun_num': noun_n,
        'adj_num': adj_n,
    }
    sentences.append(sentence)

with open(test_sentences_path, 'w', encoding='utf-8') as json_file:
    json.dump(sentences, json_file, indent=4, ensure_ascii=False)
pickle.dump(sentences, open(sentence_path, 'wb'))

