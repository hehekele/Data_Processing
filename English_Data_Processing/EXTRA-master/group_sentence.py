import json

from datasketch import MinHash, LeanMinHash, MinHashLSH
import datetime
import pickle

# 更新参数
sentence_path = 'sentences.pickle'  # resulting from process_sentence.py
directory = './'  # directory to save the grouped sentence ids 保存分组句子 id 的目录
# 这是一个包含相似性阈值的 Python 列表。
sim_thresholds = [0.9]  # the similarity between two near duplicates. To test more in this way [0.9, 0.85, 0.7] 两个接近重复项之间的相似度
# 表示用于句子相似性分析的 shingle（子序列）的大小。在这里，shingle_size 设置为 2，意味着将句子拆分为两个词的 shingles，以保留一定程度的词序信息。
shingle_size = 2  # preserve the word order to some extent
# 表示在句子分组中的最小句子数量。只有包含至少 group_size 个句子的分组才会被保留。
group_size = 5  # minimum number of sentences in a


def now_time():
    """a string of current time"""
    return '[' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f') + ']: '

# k-shingles是一种文本处理技术，用于将文本分割成连续的k个词的片段
def get_k_shingles(raw_text, k=1):
    # 全部转换成小写
    text_lower = raw_text.lower()
    # 将文本按空格拆分成单词，然后将这些单词存储在名为 words 的列表中。
    words = text_lower.split()
    # 如果k等于1，对应于 1-shingles，它们只是单个单词。
    if k == 1:
        return set(words)
    # 对于1-shingles并不会存在shingles列表中
    # 当k>1时，从输入文本生成 k-shingles
    shingles = []
    # shingles存储k-shingles
    for start in range(len(words) + 1 - k):
        # k_words中包括第start+1,start+2.....start+k个单词
        k_words = words[start:(start + k)]
        # 将 k_words 中的 k 个单词使用空格连接起来
        k_shingle = ' '.join(k_words)
        shingles.append(k_shingle)
        print(shingles)
    return set(shingles)


print(now_time() + 'Program running')
sentences = pickle.load(open(sentence_path, 'rb'))

# 创建了一个名为 minhash_dict 的字典，用于存储句子的 MinHash 对象
minhash_dict = {}
for idx, sentence in enumerate(sentences):
    # 保证词数大于规定的shingle_size 2，主语数量为0，名词和形容词的数量至少为1，才可以继续执行
    if sentence['word_num'] < shingle_size:
        continue
    if sentence['subj_num'] > 0:
        continue
    if sentence['noun_num'] < 1:
        continue
    if sentence['adj_num'] < 1:
        continue
    # 如歌句子满足上述条件
    # 提取出exp
    exp = sentence['exp']
    # 提取出exp的k_shingles
    shingle_set = get_k_shingles(exp, shingle_size)
    # 为满足上述条件的句子创建MinHash对象
    mh = MinHash()  # create MinHash for exp
    for s in shingle_set:
        # 对k-shingles编码成utf8格式
        # 对编码后的数据进行哈希处理，
        # 将生成的哈希值合并到 MinHash 对象的内部状态中。
        mh.update(s.encode('utf8'))  # convert shingle s into MinHash

    # 得到的 MinHash 对象 (mh) 存储在minhash_dict字典中
    # 字典的键是句子的索引 idx，值是转换为 LeanMinHash 对象的 MinHash。
    # 这里使用了 LeanMinHash 类来创建 MinHash 对象的轻量级表示。
    minhash_dict[idx] = LeanMinHash(mh)
print(now_time() + 'Created Minhash')
# 删除sentences用来释放内存
del sentences  # to save memory

# 这部分代码负责为不同的相似性阈值创建局部敏感哈希 (LSH) 索引，
# 然后使用这些索引根据 MinHash 表示对相似的句子进行分组。

# sim_thresholds是一个包含相似性阈值的 Python 列表。
# 在上面我们已经定义了 sim_thresholds = [0.9],所以阈值是0.9,这个阈值已经是相对较大的了
for sim_threshold in sim_thresholds:  # create MinHash for once, when testing multiple similarity values
    # 创建局部敏感哈希（LSH）索引对象的操作。
    # 在这里使用了 MinHashLSH 类的构造函数来实例化一个 LSH 索引对象。
    lsh = MinHashLSH(threshold=sim_threshold)  # create LSH index

    # 将之前生成的 MinHash 对象插入到局部敏感哈希（LSH）索引中，以便进行相似性分析和分组
    for idx, mh in minhash_dict.items():
        # 使用该lsh.insert()方法将MinHash对象插入到LSH（Locality-Sensitive Hashing）索引中lsh。
        lsh.insert(str(idx), mh)
    print(now_time() + 'Created LSH for similarity {}'.format(sim_threshold))

    # 这个集合的作用是标记哪些句子已经被处理过，以避免重复处理相同的句子。
    queried_ids = set()  # way more efficient than list
    # exp_id_groups 是一个列表，其中包含了根据相似性分组的句子索引。
    exp_id_groups = []

    # 使用局部敏感哈希（LSH）索引对相似的句子进行分组，并维护一个句子 ID 组的列表 exp_id_groups。
    for idx, mh in minhash_dict.items():
        # 在每次处理一个句子之前，代码会检查当前句子的索引是否已经存在于 queried_ids 集合中。
        # 如果当前句子的索引已经存在于 queried_ids 中，那么说明这个句子已经被处理过，就会使用 continue 跳过当前句子的处理，继续处理下一个句子。
        # 如果当前句子的索引不在 queried_ids 中，说明这个句子是新的，代码会将它添加到 queried_ids 集合中，标记为已处理
        if idx in queried_ids:
            continue
        # lsh.query(mh)方法的主要目的是根据 MinHash 值的相似性，找到与指定 MinHash 对象 mh 相似的其他数据项或对象
        # 将 one_group_ids_str 中的每个句子ID从字符串格式转换为整数格式，存储在 one_group_ids_int 列表中。
        # one_group_ids_str是一组重复句子的 id 列表
        one_group_ids_str = lsh.query(mh)  # id list of one group of duplicate sentences
        # 对于每个在 one_group_ids_str 列表中的索引，代码使用 lsh.remove(i) 方法从 LSH 索引中删除这些索引。
        # 这是为了提高处理效率，因为一旦句子被分组，就不需要再与其他相似的句子进行比较。
        for i in one_group_ids_str:
            lsh.remove(i)  # for efficiency
        # 这行代码将 one_group_ids_str 中的每个句子索引从字符串格式转换为整数格式，并将它们存储在 one_group_ids_int 列表中。
        one_group_ids_int = [int(i) for i in one_group_ids_str]
        # 它检查组内的句子数量是否大于指定的 group_size，即最小组内句子数量。
        # 如果满足条件，说明该组中的句子足够多，将其添加到 exp_id_groups 列表中。
        if len(one_group_ids_int) > group_size:
            exp_id_groups.append(one_group_ids_int)  # only keep a group with enough sentences
        # 在这两行代码中，将组内的句子索引添加到 queried_ids 集合中，以标记它们已经被处理过，避免重复处理。
        for i in one_group_ids_int:
            queried_ids.add(i)

    print(exp_id_groups)

    with open('test_group.json', 'w', encoding='utf-8') as json_file:
        json.dump(exp_id_groups, json_file, indent=4, ensure_ascii=False)
    pickle.dump(exp_id_groups, open(directory + 'groups{}.pickle'.format(sim_threshold), 'wb'))
    print(now_time() + 'Saved a file for similarity {}'.format(sim_threshold))
