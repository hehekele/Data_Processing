import json
import pickle
import re
import jieba
import jieba.posseg as pseg
import thulac

review_path = '../result/reviews.pickle'  # resulting from format_amazon.py
sentence_path = '../result/sentences.pickle'  # path to save sentences
test_sentences_path = '../result/test_sentences.json'

# 分句
def get_sentences(string):
    string = re.sub('[，。？！\n]', '。', string)
    sentences = [sent.strip() for sent in string.split('。') if sent.strip() != '']
    return sentences

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

# 也可以尝试其他的库，比如清华的，哈工大的，百度的
# 下面是清华的库，可以修改
# 使用THULAC库进行词性标注
# def get_sentence_attr(string):
#     pronoun_num = 0  # 人称代词数量
#     noun_num = 0  # 名词数量
#     adj_num = 0  # 形容词数量
#
#     word_num = len(string)
#     # 使用THULAC库进行词性标注
#     thu = thulac.thulac()
#     word_pos= thu.cut(string, text=True)
#     print(word_pos)
#     pos_list = re.findall(r'_([a-zA-Z]+)', word_pos)
#     print(pos_list)
#     for pos in pos_list:
#         print(pos)
#         if pos == 'r':
#             pronoun_num += 1
#         elif pos == 'n':
#             noun_num += 1
#         elif pos == 'a':
#             adj_num += 1
#     print(word_num)
#     print(pronoun_num)
#     print(noun_num)
#     print(adj_num)
#     return word_num, pronoun_num, noun_num, adj_num
