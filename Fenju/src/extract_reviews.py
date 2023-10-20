import json
import gzip

raw_path = '../test_data_1000.json.gz'  # path to load raw reviews 加载原始评论的路径

reviews = []
for line in gzip.open(raw_path, 'r'):
    text = eval(line)
    json_doc = {'item': text['item_id'],
                'user': text['user_id'],
                'time': text['time'],
                'item_score': float(text['item_score']),
                'user_score': float(text['user_score']),
                'review': text['review']
                }
    reviews.append(json_doc)
with open('../result/extract.json', 'w', encoding='utf-8') as json_file:
    json.dump(reviews, json_file, indent=4, ensure_ascii=False)
