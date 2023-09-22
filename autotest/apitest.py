import  autotest.parser_swagger
import urllib.request
import socket
import json
import logging
import util.common


class ApiTest:
    domain = ""
    port = ""
    httpProtocolType = ""
    swaggerFilePath = ""
    httpRequestTimeoutSecond = 2

    jwt = ""# 登陆成功的 token
    swagger_data = []
    metrics = {} # 一次整体请示所有接口的，汇总统计
    exceptApiPath = []

    # 构造函数，初始化变量
    def __init__(self,domain,port,httpProtocolType,swaggerFilePath):
        self.domain = domain
        self.port = port
        self.httpProtocolType = httpProtocolType
        self.swaggerFilePath = swaggerFilePath
        self.initMetrics()
        self.exceptApiPath = ["/sys/quit","/game/match/sign","/game/match/sign/cancel","/user/logout"]

        logging.basicConfig(format='%(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s',level=logging.DEBUG)  # 配置输出格式、配置日志级别

    def run(self):
        logging.info("run")

        ps = autotest.parser_swagger.ParserSwagger(self.swaggerFilePath, 1)
        self.swagger_data = ps.startRun()

        self.scannerAll()

    # 请示所有API接口
    def scannerAll(self):
        logging.info("scannerAll:")

        self.initMetrics()

        domain = self.getUrlPrefix()
        logging.info("domain:"+domain)

        self.metrics["all"] = len(self.swagger_data['list'])
        for row in self.swagger_data['list']:
            if row["path"] in self.exceptApiPath:
                logging.debug("except:"+row["path"])
                self.metrics["except"] = self.metrics["except"] + 1
                continue

            url = domain + row['path']
            headers = self.setHeaderDefaultValue(row)

            htmlData ,errCode = self.httpRequest(url,row['method'],headers ,row['body'])
            if (errCode > 0 ):
                self.metrics["httpFailed"] = self.metrics["httpFailed"] + 1
                # print("http err code:",errCode)
            else:
                self.metrics["httpSuccess"] = self.metrics["httpSuccess"] + 1
                self.processData(htmlData)


        logging.info(self.metrics)

    # 一次请示的，http header 默认值处理
    def setHeaderDefaultValue(self,row):
        headers = row["header"]
        if( not headers):
            return headers

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

        # 处理公共请示头的验证：jwt
        if(util.common.key_exist_return_value(row,"security")):
            # security = util.common.key_exist_return_value(row,"security")
            # print(security[0]["ApiKeyAuth"])
            headers[self.swagger_data["securityDefinitions"]["ApiKeyAuth"]["name"]] = self.loginJWT()
            # print(self.swagger_data["securityDefinitions"]["ApiKeyAuth"]["name"])
            # print(headers)
            # exit()

        # contentType = "application/json; charset=UTF-8"
        contentType = "application/json"
        if (row["consumes"]):
            contentType = row["consumes"]

        headers["Content-Type"] = contentType
        return headers

    # 获取 用户 token，如果不存在，就发起请求
    def loginJWT(self):
        if (self.jwt):
            return self.jwt

        domain = self.getUrlPrefix()
        for row in self.swagger_data['list']:
            if(row["path"] == "/base/login"):
                url = domain + row['path']
                headers = self.setHeaderDefaultValue(row)
                # print(row['body'])
                body = {"username":"frame_sync_1" , "password":"123456"}
                # print(body)
                htmlData ,errCode = self.httpRequest(url,row['method'],headers ,body)
                if (errCode > 0 ):
                    print("http err code:",errCode)
                else:
                    bussData = self.processData(htmlData)
                    self.jwt = bussData["data"]["token"]
                    return self.jwt
                break





    # 处理：业务返回的内容(json)
    def processData(self,htmlData):
        # print(htmlData)
        data = {}
        try:
            data = json.loads(htmlData)
        except :
            print(" json.loads err:"+htmlData)
        else:
            if(data["code"] != 200):
                self.metrics["bussFailed"] = self.metrics["bussFailed"] + 1
                logging.error(" business data code failed:"+data["msg"])
            else:
                self.metrics["bussSuccess"] = self.metrics["bussSuccess"] + 1
                logging.info("business data")

        return data

    # 发送一次HTTP请示
    def httpRequest(self,pUrl,pMethod,pHeaders,pData):
        logging.info("httpRequest url:"+pUrl  + " , method:"+pMethod +" , header:"+ util.common.map_to_str(pHeaders))

        if(pData):
            # pData = urllib.parse.urlencode(pData).encode('utf-8')
            reqObj = urllib.request.Request(url=pUrl,method=pMethod,headers=pHeaders, data=bytes(json.dumps(pData),"utf-8"))
        else:
            reqObj = urllib.request.Request(url=pUrl,method=pMethod,headers=pHeaders)

        htmlData = ""
        errPrefix = "httpRequest err "
        try:
            res = urllib.request.urlopen(reqObj,timeout=self.httpRequestTimeoutSecond)
        except urllib.error.URLError as e:
            if hasattr(e,"code"):
                logging.error(errPrefix+" URLError, code: "+str(e.code))
                return htmlData,1
            if hasattr(e,"reason"):
                logging.error(errPrefix+"  reason: "+e.reason)
                return htmlData,2
        except socket.timeout as e:
            print("except socket.timeout",e)
            return htmlData , 22


        logging.debug("httpRequest status:" + str(res.status))
        if res.status != 200:
            logging.error(errPrefix+ " statusCode:"+str(res.status))
            return htmlData,3

        htmlData = res.read().decode('utf-8')
        if (htmlData):
            return htmlData,0
        else:
            logging.error(errPrefix + " response empty~")
            return htmlData,33


        # return htmlData,err

    # 获取一个全新的、空的统计量
    def initMetrics(self):
        self.metrics = {"httpFailed":0,"httpSuccess":0, "bussFailed":0,"bussSuccess":0 , "except":0,"all":0}

    # 获取请示的完整URL地址
    def getUrlPrefix(self):
        return self.httpProtocolType + "://" + self.domain + ":" + self.port