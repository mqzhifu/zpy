import util.spider as uspider
import urllib.request,urllib.error
from lxml import etree
import socket
import socks
import threading
import time

def main():
    base_url = "https://cn.pornhub.com/pornstars?page={page_number}"
    page_index = 3
    oneUrl = base_url.replace("{page_number}", str(page_index))
    html ,err_code = requestGetOnePageHtml(oneUrl,11)

    uspider.save_content_to_file("./","html_data.html",html)

    # print(html)

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

if  __name__ == "__main__" :
    main()