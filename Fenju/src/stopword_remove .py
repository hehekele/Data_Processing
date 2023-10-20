import json

import jieba

# 停用词路径
stopwords_path = '../baidu_stopwords.txt'
# 创建一个空的集合
stopwords = set()

# 打开停用词文件并加载数据
with open(stopwords_path, 'r', encoding='utf-8') as f:
    for line in f:
        # 可以去除字符串两边的空格和换行符
        stopwords.add(line.strip())


with open("../result/word_separate.json", "r", encoding="utf-8") as json_file:
    data_list = json.load(json_file)

for data in data_list:
    exp = data['exp']
    words = jieba.cut(exp, cut_all=False)
    word_list = list(words)
    remove_words = [word for word in word_list if word not in stopwords]
    new_exp = " ".join(remove_words)
    data['exp_stopword_remove'] = new_exp


with open("../result/stopword_remove.json", "w", encoding="utf-8") as json_file:
    json.dump(data_list, json_file, ensure_ascii=False, indent=4)