import time
import urllib.request ,urllib.error
import util.spider as us
import socket
import util.common as uc
import socks

from urllib.parse import quote

class Lagou:
    data_path = ""
    domain = "https://www.lagou.com/wn/jobs?cl=false&fromSearch=true&kd={keyword}"
    def __init__(self,data_path):
        self.data_path = data_path

    def start(self):
        # sys.setdefaultencoding('utf8')

        startTime = time.time()

        finalDomain = self.domain.replace("{keyword}","golang")
        htmlData,httpResStatus,err = self.requestGetOnePageHtml(finalDomain)
        if err < 0:
            uc.ppp("requestGetOnePageHtml err ,code=",err)

        us.save_content_to_file(self.data_path,"lagou.html",htmlData)


        # thread_list = []
        # step = 100
        # for i in range(1,1600,step):
        #     thisTimePageStart = i
        #     thisTimePageEnd = i + step - 1
        #     print("create thread : ",thisTimePageStart,thisTimePageEnd)
        #     # print("create thread : ",i,i+1)
        #     #
        #     thread = threading.Thread(target=spiderByPage,args=(thisTimePageStart,thisTimePageEnd))
        #     # thread = threading.Thread(target=spiderByPage,args=(i,i+1))
        #     thread_list.append(thread)
        #
        # for p in thread_list:
        #     # print("p.start:", p.getName())
        #     p.start()
        #
        # for p in thread_list:
        #     p.join()

        execTime = time.time() - startTime

        print("exec time:",execTime)

    def requestGetOnePageHtml(self,url):
        timeoutSecond = 2
        httpResStatus = 0
        err = 0
        htmlData = ""


        print("requestGetOnePageHtml:",url, "  timeout:",timeoutSecond)
        # url = quote(url)
        headers = us.get_common_header()
        # print(headers)

        # dataOri = {"x":1,"b":3}
        # data = bytes(urllib.parse.urlencode(dataOri),encoding="utf-8")
        # url = baseUrl + urlPage + str(page_index)
        # reqObj = urllib.request.Request(url=url,method="GET",headers=headers,data=data )

        socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 10010)
        socket.socket = socks.socksocket

        reqObj = urllib.request.Request(url=url,method="GET",headers=headers)

        # print("requestGetOnePageHtml , url:"+url , " header:",headers)
        try:
            res = urllib.request.urlopen(reqObj,timeout=timeoutSecond)
            # res = urllib.request.urlopen(reqObj)
        except urllib.error.URLError as e:
            print("exception...")
            if hasattr(e,"code"):
                print("case in :code",e.code)
                return htmlData,httpResStatus,-11
            if hasattr(e,"reason"):
                print("case in reason:",e.reason)
                return htmlData,httpResStatus,-12
        except socket.timeout as e:
            print("except socket.timeout",e)
            return htmlData ,httpResStatus, -22


        print("http res status:",res.status)
        if res.status != 200:
            print(" http res status err:",res.status)
            return htmlData,res.status,err

        # print(res.read())
        htmlData = res.read().decode('utf-8')
        return htmlData,200,err

