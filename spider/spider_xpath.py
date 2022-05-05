import util
import urllib.request,urllib.error
from lxml import etree
import socket

domain = "https://er23w1232.xyz/"
uri = "forum.php?mod=forumdisplay&fid=38"
url = domain + uri

urlPage = "&page="


pageStart = 1
pageMax = 100

def main():
    for page_index in range(1,101):
        htmlData ,err_code = requestGetOnePageHtml(url,page_index)
        if err_code > 0 :
            print("err_code:",err_code)
            exit(1)
        # print("htmlData:",htmlData)
        # util.save_content_to_file("./","html_data.html",htmlData)

        # parser1024(htmlData)
        parser98tang(htmlData)

        exit(2)


def requestGetOnePageHtml(baseUrl , page_index):
    headers = {
        "User-Agent":  util.get_rand_one_ua("pc"),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Language": "zh-CN,zh;q=0.9",
        # "referer":"https://er23w1232.xyz/",
        # "Accept-Charset":"GB2312,utf-8;q=0.7,*;q=0.7",
    }
    err = 0
    htmlData = ""
    # dataOri = {"x":1,"b":3}
    # data = bytes(urllib.parse.urlencode(dataOri),encoding="utf-8")
    url = baseUrl + urlPage + str(page_index)
    # reqObj = urllib.request.Request(url=url,method="GET",headers=headers,data=data )
    reqObj = urllib.request.Request(url=url,method="GET",headers=headers )

    print("requestGetOnePageHtml , url:"+url , " header:",headers)

    timeoutSecond = 2
    try:
        res = urllib.request.urlopen(reqObj,timeout=timeoutSecond)
    except urllib.error.URLError as e:
        print("exception...")
        if hasattr(e,"code"):
            print("case in :code",e.code)
            return htmlData,1
        if hasattr(e,"reason"):
            print("case in reason:",e.reason)
            return htmlData,2
    except socket.timeout as e:
        print("except socket.timeout",e)
        return htmlData , 22


    print("http res status:",res.status)
    if res.status != 200:
        print(" http res status err:",res.status)
        return htmlData,3

    htmlData = res.read().decode('utf-8')
    return htmlData,err

def get_empty_record ():
    record = {
        "href" : "",#详情连接
        "title" : "",#标题
        "author" : "",#作者
        "date" : ""#日期
    }
    return record

def parser1024(htmlData):
    htmlTree = etree.HTML(htmlData)

def parser98tang(htmlData):
    htmlTree = etree.HTML(htmlData)
    threadTablelistHtml = htmlTree.xpath('//div[@id="threadlist"]//tbody[contains(@id,"normalthread")]/tr[1]')

    for tr in threadTablelistHtml:
        record = get_empty_record()
        record["href"]      = tr.xpath("./td[1]/a[1]/@href")
        record["title"]     = tr.xpath("./th/a[2]/text()")
        record["author"]    = tr.xpath("./td[2]/cite/a/text()")
        record["date"]      = tr.xpath("./td[2]/em/span/span/text()")
        print(record)

        exit(11)

if  __name__ == "__main__" :
    main()