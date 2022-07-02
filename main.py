import math
import os
import re
import heapq

import jieba
import jieba.analyse

dic = "data/dic.txt"
data = "data/data.csv"
cut_txt = "data/data_cut.txt"
idf_txt = "data/data_idf.txt"
keyword_txt = "data/data_key.txt"
index_keyword_txt = "data/index2key.txt"
data_status_txt = "data/data_status.txt"
recommend_txt = "data/recommend.txt"
stopword_txt = "data/stop_word.txt"


def loadTitle():
    f = open(data, encoding='utf - 8')
    i = 0
    tits = []
    for line in f:
        if i == 0:
            i += 1
            continue
        (title, author, desc, find, cover, content) = line.split(',')
        cc = title.replace('/', " ").replace(':', " ") \
            .replace(',', " ").replace('。', " ") \
            .replace('，', " ").replace('!', " ") \
            .replace('?', " ").replace('[', " ") \
            .replace(']', " ").replace('-', " ") \
            .replace('|', " ").replace('=', " ") \
            .replace('-', " ").replace('；', " ").replace('：', " ") \
            .replace(';', " ").replace('\n', " ").replace('.', " ") \
            .replace('-', " ").replace('•', " ").replace('、', " ") \
            .replace('"', " ").replace('+', " ").replace('-', " ") \
            .replace('\'', " ").replace('\"', " ").replace('「', " ") \
            .replace('」', " ").replace('—', " ").replace('•', " ") \
            .replace("\\n", " ").replace('！', " ").replace('？', " ") \
            .replace('·', " ").replace('【', " ").replace('】', " ") \
            .replace('（', " ").replace('）', " ").replace('…', " ") \
            .replace('◆', " ").replace('《', " ").replace('》', " ")
        cc = re.sub('[a-zA-Z]', '', cc)
        tits.append(cc)
    return tits


def cut():
    stopwords = [line.strip() for line in open(stopword_txt, encoding='utf - 8').readlines()]
    jieba.load_userdict(dic)
    f = open(data, encoding='utf - 8')
    i = 0
    file = open(cut_txt, mode='a', encoding='utf - 8')
    for line in f:
        if i == 0:
            i += 1
            continue
        (title, author, desc, find, cover, content) = line.split(',')
        cc = title + " " + desc + " " + content
        cc = cc.replace('/', " ").replace(':', " ") \
            .replace(',', " ").replace('。', " ") \
            .replace('，', " ").replace('!', " ") \
            .replace('?', " ").replace('[', " ") \
            .replace(']', " ").replace('-', " ") \
            .replace('|', " ").replace('=', " ") \
            .replace('-', " ").replace('；', " ").replace('：', " ") \
            .replace(';', " ").replace('\n', " ").replace('.', " ") \
            .replace('-', " ").replace('•', " ").replace('、', " ") \
            .replace('"', " ").replace('+', " ").replace('-', " ") \
            .replace('\'', " ").replace('\"', " ").replace('「', " ") \
            .replace('」', " ").replace('—', " ").replace('•', " ") \
            .replace("\\n", " ").replace('！', " ").replace('？', " ") \
            .replace('·', " ").replace('【', " ").replace('】', " ") \
            .replace('（', " ").replace('）', " ").replace('…', " ") \
            .replace('◆', " ").replace('《', " ").replace('》', " ")
        cc = re.sub('[a-zA-Z]', '', cc)
        c = jieba.cut(cc, HMM=True)
        lin = ' '.join(c)
        wr = ' '.join(lin.split())
        res = []
        for word in wr.split(" "):
            if word not in stopwords:
                res.append(word)

        file.write(' '.join(res))
        file.write("\n")
    file.close()


def loadIdf():
    f = open(cut_txt, encoding='utf - 8')
    data_content = []
    for line in f:
        data_content.append(line.replace("\\n", "").replace("\n", ""))

    idf_dic = {}

    # data_content是分析文本
    doc_count = len(data_content)  # 总共有多少篇文章

    for i in range(len(data_content)):
        new_content = data_content[i].split(' ')
        for word in set(new_content):
            if len(word) > 1:
                idf_dic[word] = idf_dic.get(word, 0.0) + 1.0
            # 此时idf_dic的v值：有多少篇文档有这个词，就是多少
    for k, v in idf_dic.items():
        w = k
        p = '%.10f' % (math.log(doc_count / (1.0 + v)))  # 结合上面的tf-idf算法公式
        if u'\u4e00' < w <= u'\u9fa5':  # 判断key值全是中文
            idf_dic[w] = p
    with open(idf_txt, 'w', encoding='utf-8') as f:
        for k in idf_dic:
            if k != '\n':
                f.write(str(k) + ' ' + str(idf_dic[k]) + '\n')


def loadKeyWord():
    jieba.analyse.set_idf_path(idf_txt)
    f = open(cut_txt, encoding='utf - 8')
    data_content = []
    file = open(keyword_txt, mode='a', encoding='utf - 8')
    for line in f:
        lin = line.replace("\\n", "").replace("\n", "")
        tags = jieba.analyse.extract_tags(lin, topK=15)
        if len(tags) == 0:
            continue
        file.write(" ".join(tags))
        file.write("\n")
    file.close()


def count():
    file = open(keyword_txt, encoding='utf - 8')
    w = open(index_keyword_txt, mode='a', encoding='utf - 8')
    li = []
    for line in file:
        for word in line.split(" "):
            li.append(word.replace("\n", ""))
    se = set(li)
    for word in se:
        w.write(word)
        w.write("\n")


def recommend():
    file = open(keyword_txt, encoding='utf - 8')
    keyword = []
    for line in file:
        lin = line.replace("\n", '')
        if lin == "":
            continue
        li = []
        for word in lin.split(" "):
            li.append(word)
        keyword.append(li)
    print(keyword)
    w = open(recommend_txt, mode='a', encoding='utf - 8')
    j = 0
    tits = loadTitle()
    for words in keyword:
        nex = []
        for i in range(len(keyword)):
            if i == j:
                nex.append(0.0)
                continue
            all_list = []
            for word in words:
                all_list.append(word)
            for word in keyword[i]:
                all_list.append(word)
            all_set = set(all_list)
            su = 0
            for word in all_set:
                if word in words:
                    if word not in keyword[i]:
                        su += 1
                if word in keyword[i]:
                    if word not in words:
                        su += 1

            nex.append(- (su/30.0)+1)
        # print(nex)
        w.write(tits[j])
        w.write(" => ")

        dd = heapq.nlargest(4, range(len(nex)), nex.__getitem__)
        print(sorted(nex, reverse=True))
        for ne in heapq.nlargest(4, range(len(nex)), nex.__getitem__):
            w.write("" + tits[ne])
            w.write(" ")
        w.write("\n")
        j += 1


if __name__ == '__main__':
    if os.path.exists(cut_txt):
        os.remove(cut_txt)
    if os.path.exists(idf_txt):
        os.remove(idf_txt)
    if os.path.exists(keyword_txt):
        os.remove(keyword_txt)
    if os.path.exists(recommend_txt):
        os.remove(recommend_txt)
    # 分词
    cut()
    # 计算 自定义 IDF 值
    loadIdf()
    # 提取关键词
    loadKeyWord()
    # 推荐算法
    recommend()
