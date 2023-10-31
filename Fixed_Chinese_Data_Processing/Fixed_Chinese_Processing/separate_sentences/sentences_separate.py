import json
import pickle
import re
import jieba

extract_path = './result/extract.pickle'
stopwords_path = '../baidu_stopwords.txt'
test_connect_sentense_path = '../src/data/test_processed_sentense.json'
connect_sentense_path = '../src/data/processed_sentense.pickle'

reviews = pickle.load(open(extract_path, 'rb'))

sentences = []
stopwords = set()
# 将句子按照标点符号来分
def cut_reviews(string):
    string = re.sub('[，。？！、 \n \s , . ! ~ ~ ～]', '。', string)
    sentences = [sent.strip() for sent in string.split('。') if sent.strip() != '']
    return sentences

idx2 = 0
for idx, review in enumerate(reviews):
    text = review['review']
    exps = cut_reviews(text)
    for exp in exps:
        word_num = len(exp)
        sentence = {
            'review_idx': idx,
            'every_idx': idx2,
            'row_exp': exp,
            'word_num': word_num
        }
        idx2 += 1
        sentences.append(sentence)

# 分词去停用词
jieba.initialize()
jieba.load_userdict("../dict_negative.txt")
# 打开停用词文件并加载数据
with open(stopwords_path, 'r', encoding='utf-8') as f:
    for line in f:
        # 可以去除字符串两边的空格和换行符
        stopwords.add(line.strip())

for sentence in sentences:
    review_text = sentence["row_exp"]
    if (len(review_text) > 4):
        segregate_list = jieba.cut(review_text, cut_all=False)
        segregate_review = " ".join(segregate_list)
        sentence["processed_exp"] = segregate_review
    else:
        sentence["processed_exp"] = review_text
    words = sentence["processed_exp"].split()
    word_list = list(words)
    remove_words = [word for word in word_list if word not in stopwords]
    new_exp = " ".join(remove_words)
    sentence['processed_exp'] = new_exp

    exp_without_spaces = sentence['processed_exp'].replace(" ", "")
    sentence['processed_exp'] = exp_without_spaces

with open(test_connect_sentense_path, "w", encoding="utf-8") as json_file:
    json.dump(sentences, json_file, ensure_ascii=False, indent=4)
pickle.dump(sentences, open(connect_sentense_path, 'wb'))

