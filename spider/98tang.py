import os

import util.spider as uspider
import urllib.request,urllib.error
from lxml import etree
import socket
import socks
import threading
import time
# 证书问题
# import ssl
# ssl._create_default_https_context = ssl._create_unverified_context

# pip3 install Pysocks

domain = "https://er23w1232.xyz/"
uri = "forum.php?mod=forumdisplay&fid=38&page={page_number}"
url = domain + uri


def main():

    startTime = time.time()

    spiderByPage(1,3)

    # thread_list = []
    # step = 30
    # for i in range(1,350,step):
    #     thisTimePageStart = i
    #     thisTimePageEnd = i + step - 1
    #     print("create thread : ",thisTimePageStart,thisTimePageEnd)
    #
    #     thread = threading.Thread(target=spiderByPage,args=(thisTimePageStart,thisTimePageEnd))
    #     thread_list.append(thread)
    #
    # for p in thread_list:
    #     # print("p.start:", p.getName())
    #     p.start()
    #
    # for p in thread_list:
    #     p.join()
    #

    execTime = time.time() - startTime
    print("exec time:",execTime)


def spiderByPage(pageStart,pageMax):
    print("spiderByPage :",pageStart,pageMax)
    finalPageMax = 352
    if pageMax >= finalPageMax:
        pageMax = finalPageMax

    record_list = []
    for page_index in range(pageStart,pageMax+1):
        # if page_index == 1:#第一页的数据需要特殊处理，回头再说
        #     continue

        oneUrl = url.replace("{page_number}", str(page_index))
        htmlData ,err_code = requestGetOnePageHtml(oneUrl,page_index)
        if err_code > 0 :
            print("err_code:",err_code)
            return [],err_code
        # print("htmlData:",htmlData)
        # uspider.save_content_to_file("./","html_data.html",htmlData)

        records = parser98tang(htmlData,domain,page_index)
        # print( t.getName(),  " one page record len:",len(records))
        for i in records:
            record_list.append(i)
        # parser98tang(htmlData)

    # print(t.getName()," final page record len:",len(record_list))
    content = ""
    for i in record_list:
        print(i)
        lineStr = str(i["page"]) + " , " + i["href"] + " , " + i["title"] + os.linesep
        # print(lineStr)
        content = content + lineStr

    dir = "./98tang/"
    fileNamePrefix = "page_list"
    fileNmae = str(pageStart) + "_" +str(pageMax)
    extName = ".txt"
    fullPath = dir + fileNamePrefix + fileNmae + extName

    with open(fullPath,"w",encoding="utf-8")as fp:
        fp.write(content)

def requestGetOnePageHtml(url , page_index):
    # if page_index == -1:
    #     print("详情页过来的请求")

    # print(url)
    headers = uspider.get_common_header()
    # print(headers)
    err = 0
    htmlData = ""
    # dataOri = {"x":1,"b":3}
    # data = bytes(urllib.parse.urlencode(dataOri),encoding="utf-8")
    # url = baseUrl + urlPage + str(page_index)
    # reqObj = urllib.request.Request(url=url,method="GET",headers=headers,data=data )

    socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 10010)
    socket.socket = socks.socksocket

    reqObj = urllib.request.Request(url=url,method="GET",headers=headers)

    print("requestGetOnePageHtml , url:"+url , " header:",headers)

    timeoutSecond = 2

    try:
        res = urllib.request.urlopen(reqObj,timeout=timeoutSecond)
        # res = urllib.request.urlopen(reqObj)
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

    # print(res.read())

    htmlData = res.read().decode('utf-8')
    return htmlData,err

def get_empty_record ():
    record = {
        "page" : 0,
        "href" : "",#详情连接
        "title" : "",#标题
        "author" : "",#作者
        "date" : "",#日期
        "size":"",#文件大小
        "imgs":[],#图片列表
        "format":"",#文件格式
    }
    return record

def spider_detail(url,record):
    pageDetailHtmlDataStr,err_code = requestGetOnePageHtml(url,-1)
    pageDetailHtmlTree = etree.HTML(pageDetailHtmlDataStr)

    dateStrList = pageDetailHtmlTree.xpath('//span[contains(@class,"fl gray")]/text()')
    date = dateStrList[0].split(": ")[1]
    print("date:",date)

    record["date"] = date

    read_tpc_element = pageDetailHtmlTree.xpath('//div[@id="read_tpc"]')[0]
    read_tpc_element_text = read_tpc_element.xpath('text()')
    for i in read_tpc_element_text:
        # 影片名稱 影片名称
        # 是否有碼 是否有码
        # 字幕语言 字幕語言
        # 下載軟件 做種時間 圖片預覽 出品廠商  作种期限
        # 影片格式 影片大小 影片容量 影片时间 影片说明 影片截图
        #

        if i.find("影片格式")!= - 1:
            fileFormat = i.split("：")[1]
            record["format"] = fileFormat
            # print("影片格式:",fileFormat)

        if i.find("影片大小")!= - 1:
            fileSize = i.split("：")[1]
            record["size"] = fileSize
            # print("影片大小:",fileSize)

        if i.find("影片容量")!= - 1:
            fileSize = i.split("：")[1]
            record["size"] = fileSize
            # print("影片容量:",fileSize)

    # print("read_tpc_element_text:",read_tpc_element_text)
    imgHref =  pageDetailHtmlTree.xpath('//div[@id="read_tpc"]//img/@src')
    # if len(imgHref) > 0:
    record["imgs"] = imgHref
    # print("imgHref:",imgHref)

def parserDetail(url,page_index):
    htmlData ,err_code = requestGetOnePageHtml(url,-1)
    htmlTree = etree.HTML(htmlData)
    # /html/body/div[7]/div[6]/div[2]/div[1]/table/tbody/tr[1]/td[2]/div[2]/div/div[1]/table
    # tt = htmlTree.xpath("//td[@id='postmessage']")
    tt = htmlTree.xpath("//td[contains(@id,'postmessage')][1]/text()" )

    print(tt)
    exit(1)

def parser98tang(htmlData,domain,page_index):
    htmlTree = etree.HTML(htmlData)
    threadTablelistHtml = htmlTree.xpath('//div[@id="threadlist"]//tbody[contains(@id,"normalthread")]/tr[1]')

    record_list = []
    for tr in threadTablelistHtml:
        record = get_empty_record()
        record["page"] = page_index
        record["href"]      = tr.xpath("./td[1]/a[1]/@href")[0]
        record["title"]     = tr.xpath("./th/a[2]/text()")[0]
        record["author"]    = tr.xpath("./td[2]/cite/a/text()")[0]
        if page_index == 1:
            record["date"]      = tr.xpath("./td[2]/em/span/span/text()")
        else:
            record["date"]      = tr.xpath("./td[2]/em/span/text()")[0]
        # print(record)
        url = domain + record["href"]
        parserDetail(url,page_index)
        record_list.append(record)

    return record_list
        # exit(11)

if  __name__ == "__main__" :
    main()