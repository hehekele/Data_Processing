"""
    测试使用
"""
import thulac


def thulac_use():
    """
    用于分词和词性标注
    :return:
    """
    content = '出去玩了那么多次'
    th = thulac.thulac()
    res = th.cut(content, text=True)

    print(res)


if __name__ == '__main__':
    thulac_use()

# import jieba
# import jieba.posseg as pseg
# content = '南京市长江大桥'
# word_pos_list = pseg.cut(content)
# print(word_pos_list)