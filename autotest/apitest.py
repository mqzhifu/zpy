import  autotest.parser_swagger
import urllib.request
import socket
import json

class ApiTest:
    domain = ""
    port = ""
    httpProtocolType = ""

    def __init__(self,domain,port,httpProtocolType):
        self.domain = domain
        self.port = port
        self.httpProtocolType = httpProtocolType


    def getUrlPrefix(self):
        return self.httpProtocolType + "://" + self.domain + ":" + self.port

    def setHeaderDefaultValue(self,row):
        headers = row["header"]
        if( not headers):
            return headers

        xToken = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJwcm9qZWN0X2lkIjo2LCJzb3VyY2VfdHlwZSI6MTEsImlkIjoxLCJ1c2VybmFtZSI6ImZyYW1lX3N5bmNfMSIsIm5pY2tfbmFtZSI6InN5bmNfMSIsImV4cCI6MTY5NTY0NTk5MSwiaXNzIjoiY2stYXIiLCJuYmYiOjE2OTUyODU5ODF9.aCM8YonGKaSi0OSrPXtM7v5HNV_D5cOhYGI0Xwiqnnc"
        for k,v in headers.items():
            if ('X-Source-Type' == k):
                headers[k] = "12"
            elif ('X-Project-Id' == k):
                headers[k] = "6"
            elif ('X-Access' == k):
                headers[k] = "imzgoframe"
            elif ('X-Second-Auth-Uname' == k):
                headers[k] = "test"
            elif ('X-Second-Auth-Ps' == k):
                headers[k] = "qweASD1234560"



        headers["X-Token"] = xToken

        contentType = "application/json; charset=UTF-8"
        if (row["consumes"]):
            contentType = row["consumes"]

        headers["Content-Type"] =  contentType
        return headers

    def run(self):

        ps = autotest.parser_swagger.ParserSwagger("D:/project/zpy/data/swagger.json", 1)
        data = ps.startRun()


        domain = self.getUrlPrefix()
        total = {"httpFailed":0,"httpSuccess":0, "bussFailed":0,"bussSuccess":0 , "all":len(data)}
        for row in data:
            print(row)
            url = domain + row['path']
            headers = self.setHeaderDefaultValue(row)
            # print(headers)
            # exit()

            htmlData ,errCode = self.httpRequest(url,row['method'],headers ,row['body'])
            if (errCode > 0 ):
                total["httpFailed"] = total["httpFailed"] + 1
                print("http err code:",errCode)
            else:
                total["httpSuccess"] = total["httpSuccess"] + 1
                total = self.processData(htmlData,total)
            # exit()
        print(total)
        # url = "http://127.0.0.1:1111/swagger/index.html"
        # headers = {"1":"2"}
    def processData(self,htmlData,total):
        print(htmlData)
        try:
            data = json.loads(htmlData)
        except :
            print(" json.loads err:"+htmlData)
        else:
            if(data["code"] != 200):
                total["bussFailed"] = total["bussFailed"] + 1
                print(" data failed:"+data["msg"])
            else:
                total["bussSuccess"] = total["bussSuccess"] + 1
                print(" data ok!")


        return total


    def httpRequest(self,pUrl,pMethod,pHeaders,data):
        print("requestGetOnePageHtml , url:"+pUrl , " , method:"+pMethod, " , header:",pHeaders)


        reqObj = urllib.request.Request(url=pUrl,method=pMethod,headers=pHeaders)

        htmlData = ""
        timeoutSecond = 2



        try:
            res = urllib.request.urlopen(reqObj,timeout=timeoutSecond)
            # res = urllib.request.urlopen(reqObj)
        except urllib.error.URLError as e:
            print("exception...")
            if hasattr(e,"code"):
                print("case in :code",e.code)
                exit()
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
        # print(res.read())
        if (htmlData):
            return htmlData,0
        else:
            return htmlData,33


        # return htmlData,err
