import json

with open("../result/stopword_remove.json", "r", encoding="utf-8") as json_file:
    data_list = json.load(json_file)

for data in data_list:
    exp = data['exp_stopword_remove']
    exp_without_spaces = exp.replace(" ", "")
    data['exq_connect'] = exp_without_spaces

with open("../result/connect_sentense.json", "w", encoding="utf-8") as json_file:
    json.dump(data_list, json_file, ensure_ascii=False, indent=4)

