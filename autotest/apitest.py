import time

import  autotest.parser_swagger
import urllib.request
import socket
import json
import logging
import util.common
import pandas as pd

from IPython.display import display
import numpy as np
import matplotlib.pylab as plt
from tabulate import tabulate

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

        logging.basicConfig(format='%(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s',level=logging.INFO)  # 配置输出格式、配置日志级别

    def run(self):
        logging.info("run")

        ps = autotest.parser_swagger.ParserSwagger(self.swaggerFilePath, 1)
        self.swagger_data = ps.startRun()

        self.scannerAll()

    # 请示所有API接口
    def scannerAll(self):
        logging.info("scannerAll:")

        self.initMetrics()


        showList = []
        loopCnt = 0

        domain = self.getUrlPrefix()
        logging.info("domain:"+domain)

        self.metrics["all"] = len(self.swagger_data['list'])
        for row in self.swagger_data['list']:
            loopCnt = loopCnt + 1
            if (loopCnt > 10):
                break

            # requestRecord = {"httpRequestRecord":None,"buss_code":0,"buss_err_msg":""}

            if row["path"] in self.exceptApiPath:
                logging.debug("except:"+row["path"])
                self.metrics["except"] = self.metrics["except"] + 1
                continue

            url = domain + row['path']
            headers = self.setHeaderDefaultValue(row)

            htmlData ,record = self.httpRequest(url,row['method'],headers ,row['body'])

            if (record["http_code"] != 200 ):
                self.metrics["httpFailed"] = self.metrics["httpFailed"] + 1
            else:
                self.metrics["httpSuccess"] = self.metrics["httpSuccess"] + 1
                bussData,record = self.processData(htmlData,record)

            showList.append(record)


        self.dataTable(showList)

        logging.info(self.metrics)

    # 最大值显示红色
    def highlight_max(x):
        return ['color: red' if v == x.max() else '' for v in x]

    # 将:横向二维数据,转换成竖向二维数据,给PD使用
    def dataTable(self,dictList):
        html = "<table>\n"
        for row in dictList:
            td = "<td>"+row['url']+"</td>"
            td = td + "<td>"+row['method']+"</td>"
            td = td +"<td>"+str(row['http_code'])+"</td>"
            td = td +"<td>"+str(row['err_code'])+"</td>"
            td = td +"<td>"+str(row['err_msg'])+"</td>"
            td = td +"<td>"+str(row['exec_time'])+"</td>"
            td = td +"<td>"+str(row['buss_code'])+"</td>"
            td = td +"<td>"+row['buss_err_msg']+"</td>"

            trHtml = "<tr>"+td+"</tr>\n"
            html = html + trHtml

        html = html + "</table>"
        print(html)

        with open("rs.html", 'w') as file:
            content = file.write(html)

        # colNameList = self.getEmptyRecord().keys()
        # # print(colNameList)
        # pdData = {}
        # for kk in colNameList:
        #     pdData[kk] = []
        #
        # for row in dictList:
        #     for kk in colNameList:
        #         pdData[kk].append(row[kk])
        #
        # #显示所有列
        # pd.set_option('display.max_columns', None)
        # #显示所有行
        # pd.set_option('display.max_rows', None)
        # #设置value的显示长度为100，默认为50
        # pd.set_option('max_colwidth',200)
        # # 设置100列时才换行
        # pd.set_option('display.width', 1000)
        #
        # pdf = pd.DataFrame(pdData)
        # pdf = pdf.style.set_table_attributes('style="font-size: 10px"')
        # pdf.to_html('output.html')

        # tt = tabulate(df,headers=colNameList)
        # print(tt)

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
                body = {"username":"frame_sync_1" , "password":"123456"}

                htmlData ,record = self.httpRequest(url,row['method'],headers ,body)
                if (record["http_code"] != 200 ):
                    print("http err code:",record["http_code"])
                else:
                    bussData,bussRecord = self.processData(htmlData,record)
                    self.jwt = bussData["data"]["token"]
                    return self.jwt
                break





    # 处理：业务返回的内容(json)
    def processData(self,htmlData,requestRecord):

        data = {}
        try:
            data = json.loads(htmlData)
        except :
            logging.error(" json.loads err:"+htmlData)
            requestRecord["buss_code"] = 51
            requestRecord["buss_err_msg"] = " json.loads err:"+htmlData
        else:
            requestRecord["buss_code"] = data["code"]
            if(data["code"] != 200):

                requestRecord["buss_err_msg"] = data["msg"]

                self.metrics["bussFailed"] = self.metrics["bussFailed"] + 1
                logging.error(" business data code failed:"+data["msg"])
            else:
                self.metrics["bussSuccess"] = self.metrics["bussSuccess"] + 1
                # logging.info("business data")
        return data,requestRecord

    def getEmptyRecord(self):
        return {"url":"","method":"","http_code":-1,"err_code":0,"err_msg":"","exec_time":0,"buss_code":0,"buss_err_msg":""}

    # 发送一次HTTP请示
    def httpRequest(self,pUrl,pMethod,pHeaders,pData):
        # record = {"url":pUrl,"method":pMethod,"http_code":-1,"err_code":0,"err_msg":"","exec_time":0,"buss_code":0,"buss_err_msg":""}
        record = self.getEmptyRecord()
        record["url"] = pUrl
        record["method"] = pMethod

        logging.info("httpRequest url:"+pUrl  + " , method:"+pMethod +" , header:"+ util.common.map_to_str(pHeaders))

        if(pData):
            # pData = urllib.parse.urlencode(pData).encode('utf-8')
            reqObj = urllib.request.Request(url=pUrl,method=pMethod,headers=pHeaders, data=bytes(json.dumps(pData),"utf-8"))
        else:
            reqObj = urllib.request.Request(url=pUrl,method=pMethod,headers=pHeaders)

        htmlData = ""
        errPrefix = "httpRequest err "

        start_time = time.time()
        try:
            res = urllib.request.urlopen(reqObj,timeout=self.httpRequestTimeoutSecond)
        except urllib.error.URLError as e:
            if hasattr(e,"code"):
                logging.error(errPrefix+" URLError, code: "+str(e.code))
                record["err_code"] = 41

                return htmlData,record
            if hasattr(e,"reason"):
                logging.error(errPrefix + "  reason: "+str(e.reason))
                record["err_code"] = 42
                record["err_msg"] = e.reason

                return htmlData,record
        except socket.timeout as e:
            record["err_code"] = 43
            record["err_msg"] =str(socket.timeout) + e

            return htmlData , record
        except Exception as e :
            record["err_code"] = 43

            return htmlData , record

        record["exec_time"] = time.time() - start_time
        record["http_code"] = res.status

        logging.debug("httpRequest status:" + str(res.status))
        if res.status != 200:
            logging.error(errPrefix+ " statusCode:"+str(res.status))

            return htmlData,record

        htmlData = res.read().decode('utf-8')
        if (htmlData):
            return htmlData,record

        logging.error(errPrefix + " response empty~")
        record["http_code"] = 44

        return htmlData,record


        # return htmlData,err

    # 获取一个全新的、空的统计量
    def initMetrics(self):
        self.metrics = {
            "httpFailed":0,"httpSuccess":0, "bussFailed":0,"bussSuccess":0 , "except":0,"all":0
        }

    # 获取请示的完整URL地址
    def getUrlPrefix(self):
        return self.httpProtocolType + "://" + self.domain + ":" + self.port