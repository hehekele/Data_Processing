import json
import pickle
import nltk
import re

# 更新路径
review_path = 'reviews.pickle'  # resulting from format_amazon.py
sentence_path = 'sentences.pickle'  # path to save sentences
test_sentences_path = 'test_sentences.json'

# 利用正则把特殊符号替换成句号，方便分割
# 对于中文数据集,我们想要分词,是分成一句一句的
# 这里我先用没处理前的东西,也是像英文数据集这样按照一个分号进行分割,这一步的处理先不改变
def get_sentences(string):
    string = re.sub('[:,?!\n]', '.', string)
    sentences = [sent.strip() for sent in string.split('.') if sent.strip() != '']
    return sentences

# 在转换完的句子的基础上，根据句号分割，生成字符串列表
# 再把空格去掉，也就是每一个分句生成一个句子列表

# 这里的问题是这个库好像是专门针对英文数据的,它能够提取出中文的各个词性吗
def get_sentence_attr(string):
    # 记录主语，名词，形容词的数量
    subj_num = 0
    noun_num = 0
    adj_num = 0
    # 大小写转换
    words = string.lower().split()
    # 使用 NLTK 的pos_tag()函数获取每个单词的词性标记。
    # 返回各个词性的数量
    w_t_list = nltk.pos_tag(words)
    for (w, t) in w_t_list:
        if w in subj_words:
            subj_num += 1
        if t in noun_taggers:
            noun_num += 1
        if t in adj_taggers:
            adj_num += 1
    return len(words), subj_num, noun_num, adj_num

# 一些主语
subj_words = ['i', 'me', 'my', 'mine', 'myself', 'we', 'us', 'our', 'ours', 'ourselves']
# 代表各个类型的词性
noun_taggers = ['NN', 'NNP', 'NNPS', 'NNS']
adj_taggers = ['JJ', 'JJR', 'JJS']


reviews = pickle.load(open(review_path, 'rb'))
sentences = []
# `enumerate()` 用于将一个可迭代对象（这里是 reviews 列表）的元素和索引配对起来进行遍历。为`reviews`中的每个元素生成一个索引-元素的元组。
for idx, review in enumerate(reviews):
    text = review['text']
    # 这里就是reviews中的text键中的每一个短句都在exps中,遍历每个短句也就是exp
    # 这里中英文的处理也是一样的
    exps = get_sentences(text)
    for exp in exps:
        word_n, subj_n, noun_n, adj_n = get_sentence_attr(exp)
        # 这里面存着索引，解释原句子，句子字数？，主语数量，名词数量，形容词的数量
        sentence = {
            'review_idx': idx,
            'exp': exp,
            'word_num': word_n,
            'subj_num': subj_n,
            'noun_num': noun_n,
            'adj_num': adj_n,
        }
        sentences.append(sentence)

with open(test_sentences_path, 'w', encoding='utf-8') as json_file:
    json.dump(sentences, json_file, indent=4, ensure_ascii=False)
pickle.dump(sentences, open(sentence_path, 'wb'))
