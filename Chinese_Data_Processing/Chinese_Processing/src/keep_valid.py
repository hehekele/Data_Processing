# 上一步已经将索引分组了。这里是将索引和解释对应起来

import pickle
import json

review_path = '../result/reviews.pickle'  # resulting from format_amazon.py
sentence_path = '../result/sentences.pickle'  # resulting from process_sentence.py
group_path = '../result/groups0.9.pickle'  # resulting from group_sentence.py
ID_path = '../result/IDs.pickle'  # path to save explanation IDs
id2exp_path = '../result/test_id2exp.json'  # path to save id2exp


reviews = pickle.load(open(review_path, 'rb'))
sentences = pickle.load(open(sentence_path, 'rb'))
exp_id_groups = pickle.load(open(group_path, 'rb'))
id2doc = {}
for group in exp_id_groups:
    exp_idx = list(group)[0]
    for oexp_idx in group:
        sentence = sentences[oexp_idx]
        review_idx = sentence['review_idx']
        if review_idx not in id2doc:
            review = reviews[review_idx]
            json_doc = {'item': review['item'],
                        'score': review['score'],
                        'user': review['user'],
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
with open('../result/test_Ids.json', 'w', encoding='utf-8') as f:
    json.dump(IDs, f, indent=4, ensure_ascii=False)
pickle.dump(IDs, open(ID_path, 'wb'))


id2exp = {}
for idx, sentence in enumerate(sentences):
    idx = str(idx)
    if idx in idx_set:
        id2exp[idx] = sentence['exp']
with open(id2exp_path, 'w', encoding='utf-8') as f:
    json.dump(id2exp, f, indent=4, ensure_ascii=False)

























