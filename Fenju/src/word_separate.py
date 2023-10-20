import jieba
import json
with open("../result/sentences_separate.json", "r", encoding="utf-8") as json_file:
    data_list = json.load(json_file)

jieba.initialize()
jieba.load_userdict("../dict_negative.txt")

for data in data_list:
    review_text = data["exp"]
    if (len(review_text) > 4):
        segregate_list = jieba.cut(review_text, cut_all=False)
        segregate_review = " ".join(segregate_list)
        data["exp_word_sepatate"] = segregate_review
    else:
        data["exp_word_sepatate"] = review_text

with open("../result/word_separate.json", "w", encoding="utf-8") as json_file:
    json.dump(data_list, json_file, ensure_ascii=False, indent=4)

print("已写入文件")