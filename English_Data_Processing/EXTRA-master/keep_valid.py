# keep valid是保持有效的意思
import pickle
import json
# 在groups0.9.pickle中只保存了索引
# 主要是为了创建id2exp，和索引
# 更新路径
review_path = 'reviews.pickle'  # resulting from format_amazon.py
sentence_path = 'sentences.pickle'  # resulting from process_sentence.py
group_path = 'groups0.9.pickle'  # resulting from group_sentence.py
ID_path = 'IDs.pickle'  # path to save explanation IDs
id2exp_path = 'test_id2exp.json'  # path to save id2exp


reviews = pickle.load(open(review_path, 'rb'))
sentences = pickle.load(open(sentence_path, 'rb'))
exp_id_groups = pickle.load(open(group_path, 'rb'))
id2doc = {}

# 创建一个映射，将句子索引与相关的文档信息关联起来，并将这些信息存储在 id2doc 字典中。
for group in exp_id_groups:
    # ！！！这里有点问题
    # 这个 exp_idx 变量代表了当前分组中的一个句子索引，通常是该组的代表性句子。
    exp_idx = list(group)[0]
    for oexp_idx in group:
        sentence = sentences[oexp_idx]
        review_idx = sentence['review_idx']
        if review_idx not in id2doc:
            review = reviews[review_idx]
            json_doc = {
                'user': review['user'],
                'item': review['item'],
                'rating': review['rating'],
                'time': review['time'],
                # exp_idx = list(group)[0]
                # for oexp_idx in group:
                'exp_idx': [str(exp_idx)],
                'oexp_idx': [str(oexp_idx)]
            }
            id2doc[review_idx] = json_doc
        else:
            id2doc[review_idx]['exp_idx'].append(str(exp_idx))
            id2doc[review_idx]['oexp_idx'].append(str(oexp_idx))


IDs = []
idx_set = set()
for _, doc in id2doc.items():
    IDs.append(doc)
    exp_idx = doc['exp_idx']
    oexp_idx = doc['oexp_idx']
    idx_set |= set(exp_idx) | set(oexp_idx)
with open('test_Ids.json', 'w', encoding='utf-8') as f:
    json.dump(IDs, f, indent=4)
pickle.dump(IDs, open(ID_path, 'wb'))


id2exp = {}
for idx, sentence in enumerate(sentences):
    idx = str(idx)
    if idx in idx_set:
        id2exp[idx] = sentence['exp']
with open(id2exp_path, 'w', encoding='utf-8') as f:
    json.dump(id2exp, f, indent=4)

















