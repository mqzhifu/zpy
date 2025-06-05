import yaml
import urllib.request
import logging
import time
import json
import socket
from urllib import parse

class HttpRequest():
    Host = ""
    Headers = {}
    Schemes = ""
    HttpRequestTimeoutSecond = 10

    def __init__(self,schemes,host,headers):
        self.Host = host
        self.Headers = headers
        self.Schemes = schemes
        print("HttpRequest init host:",host,",Headers:",self.Headers)
        # 发送一次HTTP请示
    def req(self, uri, method, headers, data,contentType):
        # record = {"url":pUrl,"method":pMethod,"http_code":-1,"err_code":0,"err_msg":"","exec_time":0,"buss_code":0,"buss_err_msg":""}
        record = self.getEmptyRecord()
        record["url"] =self.Schemes + "://" + self.Host+ "/" + uri
        record["method"] = method

        if (not headers):
            headers = self.Headers

        headers["content-type"] = contentType
        record["headers"] = headers
        record["data"] = data

        # print("httpRequest url:" + record["url"] + " , method:" + method + " , header:" + map_to_str(headers))
        # print("httpRequest url:" + record["url"] + " , method:" + method ,",data:",data )
        print("httpRequest url:" + record["url"] + " , method:" + method)

        if (data):
            if (contentType == "application/json"):
                data = json.dumps(data).encode('utf-8')
            else:
                data = urllib.parse.urlencode(data).encode('utf-8')
                print("httpRequest data:" , data)

            reqObj = urllib.request.Request(url=record["url"], method=method, headers=headers,data=data)
        else:
            reqObj = urllib.request.Request(url=record["url"], method=method, headers=headers)

        htmlData = ""
        errPrefix = "httpRequest err "

        start_time = time.time()
        # res = urllib.request.urlopen(reqObj, timeout=self.HttpRequestTimeoutSecond)
        try:
            res = urllib.request.urlopen(reqObj, timeout=self.HttpRequestTimeoutSecond)
        except urllib.error.URLError as e:
            if hasattr(e, "code"):
                print(errPrefix + " URLError, code: " + str(e.code))

                record["http_res_code"] = e.code
                record["http_err_msg"] = "e-code"
                return htmlData, record
            if hasattr(e, "reason"):
                print(errPrefix + "  reason: " + str(e.reason))

                record["http_res_code"] = e.code
                record["http_err_msg"] = e.reason

                return htmlData, record
        except socket.timeout as e:
            logging.error("socket.timeout")

            record["http_res_code"] = 60
            record["http_err_msg"] = str(e)

            return htmlData, record
        except Exception as e:
            print("unkon exception")

            record["http_res_code"] = 61
            record["http_err_msg"] = str(e)
            return htmlData, record

        record["exec_time"] = round(time.time() - start_time, 4)
        record["http_res_code"] = res.status

        print("httpRequest status:" + str(res.status))
        if res.status != 200:
            logging.error(errPrefix + " statusCode:" + str(res.status))
            return htmlData, record

        htmlData = res.read().decode('utf-8')
        if (htmlData):
            return htmlData, record

        print(errPrefix + " response empty~")
        record["http_res_code"] = 68
        record["http_err_msg"] = "response empty"

        return htmlData, record

    def getEmptyRecord(self):
        return {"url": "", "method": "", "http_res_code": -1, "http_err_msg": "", "exec_time": 0,"headers": {},"data":{},
                "buss_code": 0, "buss_err_msg": ""}

    def getBussDataRecord(self):
        return {"code":-1,"msg":"","data":"","error":"-"}

    def processBussData(self, htmlData):
        data = self.getBussDataRecord()
        try:
            data = json.loads(htmlData)
        except:
            print(" json.loads err:" + htmlData)
            data["code"] = 500
            data["msg"] = " json.loads err:" + htmlData
            # requestRecord["buss_code"] = 51
            # requestRecord["buss_err_msg"] = " json.loads err:" + htmlData
        else:
            print("httpReq processBussData ok~~~~~~")
            # requestRecord["buss_code"] = data["code"]
            # if (data["code"] != 0):
                # requestRecord["buss_err_msg"] = data["msg"]
                # requestRecord["buss_code"] =60
                # self.metrics["bussFailed"] = self.metrics["bussFailed"] + 1
                # logging.error(" business data code failed:" + data["msg"])
            # else:
                # requestRecord["buss_code"] = 200
                # self.metrics["bussSuccess"] = self.metrics["bussSuccess"] + 1
                # logging.info("business data")

        return data


    def processCallbackBussData(self, htmlData, requestRecord):
        print("httpRequest callback buss data:",htmlData)
        # try:
        data = json.loads(htmlData)
        # except:
        #     logging.error(" json.loads err:" + htmlData)
        #     requestRecord["buss_code"] = 51
        #     requestRecord["buss_err_msg"] = " json.loads err:" + htmlData
        # else:
        #     requestRecord["buss_code"] = data["code"]
        #     if (data["code"] != 0):
        #         requestRecord["buss_err_msg"] = data["msg"]
        #         requestRecord["buss_code"] =60
        #         # self.metrics["bussFailed"] = self.metrics["bussFailed"] + 1
        #         # logging.error(" business data code failed:" + data["msg"])
        #     else:
        #         requestRecord["buss_code"] = 200
        #         # self.metrics["bussSuccess"] = self.metrics["bussSuccess"] + 1
        #         # logging.info("business data")
        data["code"] = -2
        return data,htmlData,requestRecord



# 一维 map 转 string ，用于方便输出
def map_to_str(continer):
    str = "["
    for k,v in continer.items():
        str += k + ":" + v + ","

    return str + "]"
