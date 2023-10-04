import json
from datetime import datetime
import pickle
import gzip

# 修改路径
raw_path = 'test_row_data.json.gz'  # path to load raw reviews 加载原始评论的路径
review_path = 'reviews.pickle'  # path to save reviews 保存评论的路径
test_review_path = 'test_review.json'

reviews = []
# 加载和迭代每个评论
# 不同的数据放到不同的键中
for line in gzip.open(raw_path, 'r'):
    review = eval(line)
    # text中的格式是summary+\n+reviewText
    # 对于我们中文数据集没有summary的键应该不用这样处理,直接提取就行了
    text = ''
    if 'summary' in review:
        summary = review['summary']
        if summary != '':
            text += summary + '\n'
    text += review['reviewText']

    # 这里中英文数据集的处理方式应该是一样的
    json_doc = {'user': review['reviewerID'],
                'item': review['asin'],
                'rating': int(review['overall']),
                'text': text,
                'time': datetime.fromtimestamp(int(review['unixReviewTime'])).strftime('%Y-%m-%d')}
    reviews.append(json_doc)



with open(test_review_path, 'w', encoding='utf-8') as json_file:
    json.dump(reviews, json_file, indent=4, ensure_ascii=False)
pickle.dump(reviews, open(review_path, 'wb'))
