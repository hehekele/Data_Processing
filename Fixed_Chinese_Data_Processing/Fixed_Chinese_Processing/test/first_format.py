# -*- coding: utf-8 -*-
# 处理源数据的格式
import json

with open("./三亚吉阳区3413.json", 'r', encoding='utf8') as fp:  # path为json文件路径
    data = json.load(fp)

# 处理数据的函数
def process_data(data):
    processed_data = []
    for item in data:
        # 删除每个字典后面的逗号
        item_str = json.dumps(item, ensure_ascii=False)
        # 去除键和值的前后空格
        item_str = item_str.replace('" ', '"').replace(' "', '"')
        processed_data.append(item_str)
    return processed_data

# 处理数据
processed_data = process_data(data)

# 将处理后的数据写入JSON文件
with open('processed_data.json', 'w', encoding='utf-8') as file:
    for item_str in processed_data:
        file.write(item_str + '\n')

print("处理后的数据已写入 processed_data.json 文件。")
