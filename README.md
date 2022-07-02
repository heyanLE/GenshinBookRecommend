文本信息挖掘课设：
本项目通过采集原神中书籍文本数据与词典。分词后使用 TF-IDF 算法得出每本书籍关键字。通过关键词计算每本书籍间的相似度。根据相似度给出推荐。

爬取数据源：[米游社书籍Wiki](https://bbs.mihoyo.com/ys/obc/channel/map/189/68)  
词典：[genshinAutoGlossary](https://github.com/duoduoffff/genshinAutoGlossary)  
停用词：[stopwords](https://github.com/goto456/stopwords)

data 文件夹文件说明：  
|文件名|说明|
|--|--|
|data.csv|书籍数据源|
|dic.txt|词典|
|data_cut.txt|分词后书籍数据|
|data_idf.txt|文本中所有词语 IDF 值|
|data_key.txt|书籍关键词|
|stop_word.txt|停用词|
|recommend.txt|推荐书籍|

