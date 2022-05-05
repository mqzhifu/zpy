from bs4 import BeautifulSoup
import re
import urllib.request,urllib.error
import xlwt
import urllib.parse

def main():
    print("main start:")
    url = "https://movie.douban.com/top250?start="
    # url = "http://www.baidu.com"

    for i in range(0,10):
        htmlBody = RequestGetHtml(url,i)
        parserHtml(htmlBody)

        exit(11)

def parserHtml( htmlBody):
    # r : 忽略特殊字符
    patternHTMLATagHref = re.compile(r'<a href="(.*?)">')
    #re.S : 让换行符包含在字符中
    # patternHTMLImgTagSrc = re.compile(r'<img(.*)src="(.*)?"(.*)/>',re.S)
    patternHTMLImgTagSrc = re.compile(r'<img.*src="(.*?)"')

    patternHTMLSpanTagClassTitle = re.compile(r'<span class="title">(.*?)</span>')
    patternHTMLSpanTagClassOther = re.compile(r'<span class="other">(.*?)</span>')

    print("parserHtml start:")
    bs = BeautifulSoup(htmlBody,"html.parser")
    print(bs.title.string)
    # print(bs.head.contents)
    divItemLists = bs.find_all("div",class_="item")
    for item in divItemLists:
        itemStr = str(item)
        # print("itemStr:",item)
        divStarSpanList =  item.find_all("div",class_="star")[0].find_all("span")
        #平均分
        averageScoreNum = divStarSpanList[1].string
        #评论总人数
        scorePeopleTotal = divStarSpanList[3].string
        print("averageScoreNum:",averageScoreNum, " scorePeopleTotal:",scorePeopleTotal)
        #标题
        reFindHrefRs = re.findall(patternHTMLSpanTagClassTitle,itemStr)
        title = ""
        for titleRe in reFindHrefRs:
            titleStr = titleRe.replace(u'\xa0', '')
            title = title + " " + titleStr

        print("title:",title)
        #标题2
        reFindHrefRs = re.findall(patternHTMLSpanTagClassOther,itemStr)
        print("other title:",reFindHrefRs[0])

        #详情-连接
        reFindHrefRs = re.findall(patternHTMLATagHref,itemStr)
        print("item patternHTMLATagHref:",reFindHrefRs)
        #封面图
        reFindHrefRs = re.findall(patternHTMLImgTagSrc,itemStr)
        print("item patternHTMLImgTagSrc:",reFindHrefRs[0])
        exit(22)


def RequestGetHtml(baseUrl , index):
    headers = {
        "Content-Type": "text/html; charset=utf-8",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36",
    }
    dataOri = {"x":1,"b":3}
    data = bytes(urllib.parse.urlencode(dataOri),encoding="utf-8")
    url = baseUrl + str(index * 25)
    reqObj = urllib.request.Request(url=url,method="GET",headers=headers,data=data )

    print("RequestGetHtml , url:"+url)

    try:
        res = urllib.request.urlopen(reqObj)
    except urllib.error.URLError as e:
        print("exception...")
        if hasattr(e,"code"):
            print("case in :code",e.code)
        if hasattr(e,"reason"):
            print("case in reason:",e.reason)

    print(res.status)
    if res.status == 418:
        print(" spider...")

    print(res.getheaders())
    print(res.getheader("Server"))
    html = res.read().decode('utf-8')
    # print("body:",body)
    print("RequestGetHtml finish.")
    return html

# def getData():
#     dataList = []
#     return dataList

if  __name__ == "__main__" :
    main()