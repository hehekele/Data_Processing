import json
import pickle

extract_path = './result/extract.pickle'
unified_path = './result/unified.pickle'

test_unified_path = './result/test_unified.json'

data = pickle.load(open(extract_path, 'rb'))

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
with open(test_unified_path, 'w', encoding='utf-8') as file:
    for item_str in processed_data:
        file.write(item_str + '\n')
pickle.dump(processed_data, open(unified_path, 'wb'))