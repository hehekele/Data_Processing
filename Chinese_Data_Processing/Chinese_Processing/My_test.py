# import re
#
# def get_chinese_sentences(string):
#     # 将标点符号替换为中文句号
#     string = re.sub('[，。？！\n]', '。', string)
#     # 根据中文句号分割字符串并去除空白句子
#     sentences = [sent.strip() for sent in string.split('。') if sent.strip() != '']
#     return sentences
#
# # 示例文本
# text = "你好，这是一个示例文本。它包含了一些标点符号，比如逗号，问号，和感叹号！另外，还有换行符。\n这是另一个句子。"
#
# # 调用函数处理文本
# sentences = get_chinese_sentences(text)
#
# # 打印处理后的句子列表
# for sentence in sentences:
#     print(sentence)


# import jieba.posseg as pseg
#
# # 要分析的句子
# sentence = "他是一个聪明的学生，她喜欢读书。"
#
# # 使用jieba进行分词和词性标注
# words = pseg.cut(sentence)
#
# # 初始化计数器
# pronoun_count = 0  # 人称代词数量
# noun_count = 0     # 名词数量
# adj_count = 0      # 形容词数量
#
# # 人称代词的词性标签，可以根据需要添加更多的代词
# pronoun_tags = ["r", "rr", "rz", "ry", "rys"]
#
# # 遍历分词结果并统计
# for word, pos in words:
#     if pos in pronoun_tags:
#         pronoun_count += 1
#     elif pos.startswith("n"):  # 以'n'开头的是名词
#         noun_count += 1
#     elif pos.startswith("a"):  # 以'a'开头的是形容词
#         adj_count += 1
#
# # 输出结果
# print(f"人称代词数量：{pronoun_count}")
# print(f"名词数量：{noun_count}")
# print(f"形容词数量：{adj_count}")

# import jieba
# # 要分词的中文句子
# sentence = "我喜欢学习自然语言处理"
#
# # 使用jieba进行分词
# words = jieba.cut(sentence)
#
# # 将分词结果转化为列表
# # word_list = list(words)
#
# # 输出分词结果
# print(words)


# import json
#
# # JSON数据
# json_data = '{"38": "\\u4ea4\\u901a\\u65b9\\u4fbf"}'
#
# # 解析JSON数据
# parsed_data = json.loads(json_data)
#
# # 获取键为 "38" 的值并解码Unicode转义序列
# value = parsed_data["38"].encode().decode('utf8')
#
# # 输出解码后的文本
# print(value)


# 输入的句子
sentence = "出去_v 玩_v 了_u 那_r 么_q 多次_m"

import re

# 输入的句子
sentence = "出去_v 玩_v 了_u 那_r 么_q 多次_m"

# 使用正则表达式提取下划线后面的英文字母
matches = re.findall(r'_([a-zA-Z]+)', sentence)

# 打印提取出的英文字母列表
print(matches)







