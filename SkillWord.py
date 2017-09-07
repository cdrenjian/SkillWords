#-*-coding:utf-8-*-
import requests,urllib,re,json,jieba
from wordcloud import WordCloud
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
# html = requests.get("http://www.baidu.com").content
# soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')
# result = soup.a.string
# print result
import sys
reload(sys) # Python2.5 初始化后会删除 sys.setdefaultencoding 这个方法，我们需要重新载入
sys.setdefaultencoding('utf-8')

citys="北京,天津,太原,大同,呼和浩特,包头,石家庄,廊坊,邯郸,华东,上海,杭州,\
宁波,温州,南京,济南,青岛,台州,嘉兴,金华,绍兴,苏州,无锡,常州,南通,扬州,徐州,\
连云港,福州,厦门,泉州,烟台,潍坊,临沂,淄博,菏泽,威海,合肥,马鞍山,芜湖,广州,\
深圳,海口,三亚,南宁,桂林,玉林,百色,武汉,南昌,郑州,长沙,九江,赣州,株洲,常德,宜昌,\
十堰,荆州,洛阳,南阳,新乡,安阳,重庆,成都,绵阳,贵阳,遵义,昆明,大理,拉萨,西安,宝鸡,\
西宁,银川,兰州,咸阳,天水,乌鲁木齐,昌吉,固原,沈阳,大连,哈尔滨,长春,吉林,朝阳,锦州,四平,大庆,牡丹江"
urls=[]
desc=[]
keyword="python"  #搜索的主关键词
filename="description.txt"  #爬取到的职位描述的保存文件名
imgname="python.png"#词云保存图片文件名
def geturl():
    for i in citys.split(","):
        url="http://zhaopin.baidu.com/api/quanzhiasync?query="+keyword+"&sort_type=1&city="+str(urllib.quote(i))+"&detailmode=close&rn=20&pn="
        num=20
        while len(requests.get(url+str(num)).content)>500:
            urls.append(url+str(num))  #得到有效的url，便于下一步请求内容并提取数据
            print "成功添加"+url+str(num)
            num=num+20

def getcontent():
    for i in urls:
        data=requests.get(i).content
        data=json.loads(data)   #将json转化为词典
        try:
            data=list(data["data"]["main"]["data"]["disp_data"]) #得的单条信息词典的list集合
        except:
            pass
        if data:
            with open(filename, "a") as f:
                for i in data:
                    desc.append(i["description"])
                    print i["description"]
                    f.write(i["description"])
def select_en(a):  #选出英文单词
    w=""
    tj=""
    for j in a:
        if j.isalpha() or j==" ":
            w=w+j
        else:
            print w
            if len(w)<3:
                w=""
            elif len(w)>10:
                w=""
            elif w.encode("utf-8"):
                tj=tj+str(w)+","
                w=""
    tj=tj.lower()
    return tj.replace(" ","")
def select_cn(a):
    return ",".join(jieba.cut(a))

def wordcloud(s):   #制作词云
    s=s.lower()
    s= WordCloud(background_color="white", width=1000, height=860, margin=2).generate(s)
    plt.imshow(s)
    plt.axis("off")
    plt.show()
    s.to_file(imgname)

def  counts(s):  #进行中文分词统计词频
    s=s.split(",")   #以“，”切割，返回一个list
    s_key=set(s)
    dict={i:s.count(i) for i in s_key}
    print dict
    print sorted(dict.items(), key=lambda x:x[1],reverse=True)   #打印关键词以及其出现次数
    result=sorted(dict, key=lambda x: s.count(x), reverse=True)
    result=",".join(result)
    print "成功选出热门词： "+str(result)

if __name__=="__main__":
    geturl()    #爬取所有的有效url
    print"总共合计： "+str(len(urls))+"条链接"
    getcontent()  #得到有效的职位描述数据
    with open(filename,"r") as f:
        words=f.read()
        cn=select_cn(words)  #提取英文词
        en=select_en(words)  #提取中文词,ps：提取到的这些中文词有用信息很少，干扰信息较多，没太大价值。
        counts(en)     #统计英文词频
        wordcloud(en)  #制作词云
        counts(cn)    #统计中文词频


