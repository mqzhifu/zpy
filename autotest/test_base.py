import yaml
import os
import urllib.request
import logging
import time
import json
import socket

class TestBase():
    SwaggerData = None
    HttpRequest = None
    def __init__(self):
        self.SwaggerData =  get_swagger_yaml()
        self.HttpRequest = HttpRequest(self.SwaggerData['schemes'][0],self.SwaggerData['host'],self.get_common_header())

        print("TestBase init ok " )


    def login(self):
        uri = "api/v1/client/ssocenter/sso/login"
        self.HttpRequest.req(uri,"POST",{},{})
        # requests.get('https://example.com')
        print("333")

    def get_common_header(self):
        headers = {
            "X-Device-Id": "111111",
            "X-Web-Terminal-Id": "WINDOWS",
            "X-Device-Type": "1",
            "X-Platform-Id": "B",
            "X-Tenant-Id": "10049223",
            "Authorization": "",
        }
        return headers


class HttpRequest():
    Host = ""
    Headers = {}
    Schemes = ""
    HttpRequestTimeoutSecond = 2

    def __init__(self,schemes,host,headers):
        self.Host = host
        self.Headers = headers
        self.Schemes = schemes
        print("HttpRequest init host:",host,",Headers:",self.Headers)
        # 发送一次HTTP请示
    def req(self, uri, method, headers, data):
        # record = {"url":pUrl,"method":pMethod,"http_code":-1,"err_code":0,"err_msg":"","exec_time":0,"buss_code":0,"buss_err_msg":""}
        record = self.getEmptyRecord()
        record["url"] =self.Schemes + "://" + self.Host+ "/" + uri
        record["method"] = method

        if (not headers):
            headers = self.Headers

        print("httpRequest url:" + record["url"] + " , method:" + method + " , header:" + map_to_str(headers))

        if (data):
            reqObj = urllib.request.Request(url=record["url"], method=method, headers=headers,data=bytes(json.dumps(data), "utf-8"))
        else:
            reqObj = urllib.request.Request(url=record["url"], method=method, headers=headers)

        htmlData = ""
        errPrefix = "httpRequest err "

        start_time = time.time()
        try:
            res = urllib.request.urlopen(reqObj, timeout=self.HttpRequestTimeoutSecond)
        except urllib.error.URLError as e:
            if hasattr(e, "code"):
                logging.error(errPrefix + " URLError, code: " + str(e.code))

                record["http_res_code"] = e.code
                record["http_err_code"] = 41

                return htmlData, record
            if hasattr(e, "reason"):
                logging.error(errPrefix + "  reason: " + str(e.reason))
                record["http_err_code"] = 42
                record["http_err_msg"] = e.reason

                return htmlData, record
        except socket.timeout as e:
            logging.error("socket.timeout")
            record["http_err_code"] = 43
            record["http_err_msg"] = str(e)

            return htmlData, record
        except Exception as e:
            logging.error("unkon exception")
            record["http_err_code"] = 44
            return htmlData, record

        record["exec_time"] = round(time.time() - start_time, 4)
        record["http_res_code"] = res.status

        logging.debug("httpRequest status:" + str(res.status))
        if res.status != 200:
            logging.error(errPrefix + " statusCode:" + str(res.status))

            return htmlData, record

        htmlData = res.read().decode('utf-8')
        if (htmlData):
            return htmlData, record

        logging.error(errPrefix + " response empty~")
        record["http_res_code"] = 49

        return htmlData, record

    def getEmptyRecord(self):
        return {"url": "", "method": "", "http_res_code": -1, "http_err_code": 0, "http_err_msg": "", "exec_time": 0,
                "buss_code": 0, "buss_err_msg": ""}



def get_swagger_yaml():
    yamlPath = "/Users/clarissechamley/data/gambl/thirdgame/thirdgame_tenant_api/docs/all.yaml"
    # open方法打开直接读出来
    f = open(yamlPath, 'r', encoding='utf-8')
    cfg = f.read()
    # print(type(cfg))  # 读出来是字符串
    # print(cfg)
    dataMap = yaml.load(cfg,Loader=yaml.FullLoader)   # 用load方法转字典
    return dataMap

# 一维 map 转 string ，用于方便输出
def map_to_str(continer):
    str = "["
    for k,v in continer.items():
        str += k + ":" + v + ","

    return str + "]"

classTestBase =  TestBase()
classTestBase.login()

print("finish..........")