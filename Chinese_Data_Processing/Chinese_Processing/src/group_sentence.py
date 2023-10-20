import json

import jieba
from datasketch import MinHash, LeanMinHash, MinHashLSH
import datetime
import pickle

sentence_path = '../result/sentences.pickle'  # resulting from process_sentence.py
directory = '../result/'  # directory to save the grouped sentence ids 保存分组句子 id 的目录
sim_thresholds = [0.9]  # the similarity between two near duplicates. To test more in this way [0.9, 0.85, 0.7] 两个接近重复项之间的相似度
shingle_size = 2  # preserve the word order to some extent
group_size = 5  # minimum number of sentences in a


def now_time():
    """a string of current time"""
    return '[' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f') + ']: '

# 先分词。分成一个一个词语。
# 再生成k-shingles
def get_k_shingles(raw_text, k=1):
    word = jieba.cut(raw_text)
    words = list(word)
    if k == 1:
        return set(words)
    shingles = []
    for start in range(len(words) + 1 - k):
        k_words = words[start:(start + k)]
        k_shingle = ' '.join(k_words)
        shingles.append(k_shingle)
    return set(shingles)


print(now_time() + 'Program running')
sentences = pickle.load(open(sentence_path, 'rb'))

minhash_dict = {}
for idx, sentence in enumerate(sentences):
    # 句子要满足如下条件
    if sentence['word_num'] < shingle_size:
        continue
    if sentence['pronoun_num'] > 0:
        continue
    if sentence['noun_num'] < 1:
        continue
    if sentence['adj_num'] < 1:
        continue
    exp = sentence['exp']
    shingle_set = get_k_shingles(exp, shingle_size)
    # 为满足条件的生成Minhash对象
    mh = MinHash()
    for s in shingle_set:
        # 将生成的哈希值合并到 MinHash 对象的内部状态中。
        mh.update(s.encode('utf8'))  # convert shingle s into MinHash
    # 得到的 MinHash 对象 (mh) 存储在minhash_dict字典中
    # 字典的键是句子的索引 idx，值是转换为 LeanMinHash 对象的 MinHash。
    minhash_dict[idx] = LeanMinHash(mh)
print(now_time() + 'Created Minhash')
del sentences  # to save memory

for sim_threshold in sim_thresholds:  # create MinHash for once, when testing multiple similarity values
    # 使用MinHashLSH 类的构造函数来实例化一个 LSH 索引对象。
    lsh = MinHashLSH(threshold=sim_threshold)  # create LSH index
    for idx, mh in minhash_dict.items():
        # 使用lsh.insert()方法将MinHash对象插入到LSH索引中。
        lsh.insert(str(idx), mh)
    print(now_time() + 'Created LSH for similarity {}'.format(sim_threshold))

    queried_ids = set()  # way more efficient than list
    exp_id_groups = []

    for idx, mh in minhash_dict.items():
        if idx in queried_ids:
            continue
        # 该函数根据 MinHash 值的相似性，找到与指定 MinHash 对象 mh 相似的其他数据项或对象
        one_group_ids_str = lsh.query(mh)  # id list of one group of duplicate sentences
        for i in one_group_ids_str:
            lsh.remove(i)  # for efficiency
        one_group_ids_int = [int(i) for i in one_group_ids_str]
        if len(one_group_ids_int) > group_size:
            exp_id_groups.append(one_group_ids_int)  # only keep a group with enough sentences
        for i in one_group_ids_int:
            queried_ids.add(i)

    print(exp_id_groups)

    with open('../result/test_group.json', 'w', encoding='utf-8') as json_file:
        json.dump(exp_id_groups, json_file, indent=4, ensure_ascii=False)
    pickle.dump(exp_id_groups, open(directory + 'groups{}.pickle'.format(sim_threshold), 'wb'))
    print(now_time() + 'Saved a file for similarity {}'.format(sim_threshold))
