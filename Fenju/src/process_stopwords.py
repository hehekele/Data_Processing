import jieba
import jieba.posseg as pseg

# 加载你的中文单词列表
word_list = []
with open("../baidu_stopwords.txt", "r", encoding="utf-8") as file:
    word_list = [line.strip() for line in file]

# 定义函数来检测名词和形容词
def is_noun_or_adjective(word):
    words = pseg.cut(word)
    for w, flag in words:
        if flag in ['n', 'a']:  # 'n' 表示名词，'a' 表示形容词
            return True
    return False

# 过滤掉名词和形容词
filtered_word_list = [word for word in word_list if not is_noun_or_adjective(word)]
#
# # 输出结果或将其保存到文件
# for word in filtered_word_list:
#     print(word)

# 如果要将结果保存到文件
with open("../baidu_stopwords.txt", "w", encoding="utf-8") as file:
    file.write("\n".join(filtered_word_list))
