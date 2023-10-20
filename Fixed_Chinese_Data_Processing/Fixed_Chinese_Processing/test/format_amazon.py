import json
import pickle
import gzip
import re

raw_path = '../test_data_1000.json.gz'  # path to load raw reviews 加载原始评论的路径
review_path = '../result/reviews.pickle'  # path to save reviews 保存评论的路径
test_review_path = '../result/test_review.json'

reviews = []
for line in gzip.open(raw_path, 'r'):
    review = eval(line)
    json_doc = {'item': review['item'],
                'item_score': float(review['item_score']),
                'text': review['review'],
                'user_score': float(review['user_score']),
                'time': review['time'],
                'user': review['user']}
    reviews.append(json_doc)
with open(test_review_path, 'w', encoding='utf-8') as json_file:
    json.dump(reviews, json_file, indent=4, ensure_ascii=False)
pickle.dump(reviews, open(review_path, 'wb'))
