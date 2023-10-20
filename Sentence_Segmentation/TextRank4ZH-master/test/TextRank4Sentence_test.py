#-*- encoding:utf-8 -*-
from __future__ import print_function

import sys
from imp import reload

try:
    reload(sys)
    sys.setdefaultencoding('utf-8')
except:
    pass

import codecs
from textrank4zh import TextRank4Sentence

text = codecs.open('./doc/03.txt', 'r', 'utf-8').read()
text = "前一天酒店客服小姐姐打电话联系问我们几点能到酒店，我说大概12点-1点，她说12点才退房所以可能晚一点哟，还说帮我们升级海景房，我就说好呀，结果我们3点多4点才到店，在前台拿房的时候前台的小姐姐态度已经一般，想着都算了，升级了嘛，给了一间10楼，我们进去的时候没有打扫完，地面全湿，味道超级超级难闻，洗手间等等都是湿的，不是前一天确认了我们1点多到酒店吗？3点多还没有打扫完房间，而且房间电话是打不通的，不知道是坏的还是怎样，去大堂沟通就说没有房间只有这间，我就说住不了，如果是这么差，我就不住，最后说所谓帮我升级了180度海景房，就是楼层升高了，问题也是一样，地板全是湿，味道超级大，一不小心摔倒了谁负责，前台小姐姐也是说没有办法，没有房间，这么大的酒店没有其它干净干爽的房间吗？这个不欺骗顾客吗？真心差，1分也不想给，设施就是有所谓的对海泳池，酒店环境老旧，比之前住的几间酒店差得远，服务态度不好，早餐也不是太多选择，不会推荐也不会再有下次，反正也是坑旅客住一次。"
tr4s = TextRank4Sentence()
tr4s.analyze(text=text, lower=True, source = 'all_filters')

for st in tr4s.sentences:
    print(type(st), st)

print(20*'*')
for item in tr4s.get_key_sentences(num=4):
    print(item.weight, item.sentence, type(item.sentence))