from flask import Flask, request, jsonify, redirect, url_for
from flask import Flask
from flask import render_template
import uuid
import yaml
import time
import httpReq
import apiReq
import json

class TestBase:
    SwaggerData = None
    HttpRequest = None
    ApiReq = None
    Schemes = ""
    Host  = ""
    UserLoginData = ""
    Username = ""
    Password = ""
    TenantCode = ""
    TenantId = 0
    PlatformConfig = None
    GameList = None

    def __init__(self,host, schemes, username,password,tenantId,tenantCode,platformConfig,gameList):
        swaggerPath ="/Users/clarissechamley/data/gambl/thirdgame/thirdgame_tenant_api/docs/all.yaml"
        self.SwaggerData =  get_swagger_yaml(swaggerPath)

        self.Username = username
        self.Password = password
        self.TenantId = tenantId
        self.TenantCode = tenantCode
        self.PlatformConfig = platformConfig
        self.GameList = gameList

        # self.HttpRequest = httpReq.HttpRequest(self.SwaggerData['schemes'][0],self.SwaggerData['host'],self.getCommonHeader())
        # self.HttpRequest = httpReq.HttpRequest("https", "api-c.test.3333d.vip",self.getCommonHeader())
        self.HttpRequest = httpReq.HttpRequest(schemes, host, self.getCommonHeader())

        self.ApiReq = apiReq.ApiReq(self.HttpRequest,self.TenantCode,self.TenantId,platformConfig )

        print("TestBase init ok " )

    def testCaseGame(self):
        res = {
            "user_login":{"id":1,"bussData":self.HttpRequest.getBussDataRecord(),"reqRes":self.HttpRequest.getEmptyRecord(),"name":"user_login"},
            "game_login": {"id":2,"bussData": self.HttpRequest.getBussDataRecord(),"reqRes": self.HttpRequest.getEmptyRecord(),"name":"game_login"},
            "get_wallet": {"id":3,"bussData": self.HttpRequest.getBussDataRecord(),"reqRes": self.HttpRequest.getEmptyRecord(),"name":"get_wallet"},
            "game_bet": {"id":4,"bussData": self.HttpRequest.getBussDataRecord(),"reqRes": self.HttpRequest.getEmptyRecord(),"name":"game_bet"},
        }

        if (self.TenantCode == "india"):
            data, htmlData, requestRecord = self.ApiReq.sendSms(self.Username)
            if requestRecord["http_res_code"] != 200 or data["code"] != 0:
                if (data["code"] != 10):
                    print("sendSms failed ", data, htmlData, requestRecord)
                    return res
            data, htmlData, requestRecord = self.ApiReq.userSmsLogin(self.Username)
            # print("========aaaaa:",self.Username,data)
        else :
            data,htmlData, requestRecord = self.ApiReq.userAccountLogin(self.Username,self.Password )

        res["user_login"]["bussData"] = data
        res["user_login"]["reqRes"] = requestRecord

        if requestRecord["http_res_code"] != 200 or data["code"] != 0:
            print("userLogin failed ",data,htmlData,requestRecord)
            return res

        print("-------user login token:",data["data"]["token"])
        # 保留用户登陆记录
        self.UserLoginData = data
        # 登陆成功后，请求头中加入token，用于用户登陆验
        # 证
        self.HttpRequest.Headers = self.getCommonHeader()

        data, htmlData, requestRecord =  self.ApiReq.gameLogin(self.GameList[self.TenantCode]['game_id'],self.GameList[self.TenantCode]['game_code'])

        res["game_login"]["bussData"] = data
        res["game_login"]["reqRes"] = requestRecord

        if requestRecord["http_res_code"] != 200 or data["code"] != 0:
            print("gameLogin failed ",data,htmlData,requestRecord)
            return res

        data, htmlData, requestRecord = self.ApiReq.getWallet(self.UserLoginData["data"]["userId"],self.GameList[self.TenantCode]['game_id'])
        res["get_wallet"]["bussData"] = data
        res["get_wallet"]["reqRes"] = requestRecord

        if requestRecord["http_res_code"] != 200 :
            print("getWallet failed ",data,htmlData,requestRecord)
            return res

        data, htmlData, requestRecord = self.ApiReq.gameBet(self.UserLoginData["data"]["userId"],self.GameList[self.TenantCode]['game_code'])
        print("gameBet data",data )

        res["game_bet"]["bussData"] = data
        res["game_bet"]["reqRes"] = requestRecord

        return res

    def getCommonHeader(self):
        headers = {
            "X-Device-Id": "111111",
            "X-Web-Terminal-Id": "WINDOWS",
            "X-Device-Type": "1",
            "X-Platform-Id": "B",
            "X-Tenant-Id":self.TenantId,
            # "X-Tenant-Id": "10049223",
            # "X-Tenant-Id": "1000010",
            # "Authorization": "",
        }
        if self.UserLoginData and self.UserLoginData["data"]:
            if self.UserLoginData["data"]["token"]:
                headers["Authorization"] = "Bearer "+ self.UserLoginData["data"]["token"]

        return headers

def get_swagger_yaml(swaggerPath):
    yamlPath = swaggerPath
    # open方法打开直接读出来
    f = open(yamlPath, 'r', encoding='utf-8')
    cfg = f.read()
    # print(type(cfg))  # 读出来是字符串
    # print(cfg)
    dataMap = yaml.load(cfg,Loader=yaml.FullLoader)   # 用load方法转字典
    return dataMap
# usernameBra = "mqzhifu"
# passwordBra ="mqzhifu123"
# tenantIdBra = 1000010
# tenantCodeBra = "brabxbwptnb"
#
# usernameIna = "11911111180"
# tenantIdIna = 10049223
# tenantCodeIna = "india"
platformConfig = {
    "brabxbwptnb":
        {
            "merchant":"bxcct1CG",
            "token":"3ef6c9b25ce74669af5865d45a0eb87d",
            "secret_key":"36a1adeb-5a70-408b-9de2-398820f5f34f",
            "public_key":"4a846e274ee4448390553913d30da060",
            "platform_code":"CG",
        },
    "india":
        {
            "merchant":"bxzyy1CG",
            "token":"665b529bbd164148a62547c0ec12ace1",
            "secret_key":"8d152c40-9134-4e15-bf06-16615be9bf8b",
            "public_key":"a042a64a0d904e10866915f9732447db",
            "platform_code":"CG",
        }
}


host = { "test": "api-c.test.3333d.vip","local": "127.0.0.1"}
schemes = ["https","http"]
tenant = {"10049223": "india","1000010": "brabxbwptnb"}

game_list = {
    "india":{"game_id":"117018","game_code":"8911","name":"黑神雕志平"},
    "brabxbwptnb":{"game_id":"1657027833","game_code":"vs25rlbank","name":"摇滚银行"},
}

config = {"platform":platformConfig,"host":host,"schemes":schemes,"tenant":tenant,"game_list":game_list}

# ============== http ========================================
app = Flask(__name__)


def getHttpResEmpty():
    return {"code":200,"error":"","msg":"","data":""}

@app.route('/get_config', methods=['GET', 'POST'])
def get_config():
    resp = getHttpResEmpty()
    resp["data"] = config
    return json.dumps(resp)

@app.route('/run', methods=['GET', 'POST'])
def run():
    get_data = request.get_data()
    data = json.loads(get_data)

    print("http run data:",data)

    resp = getHttpResEmpty()
    # resp["data"] = data

    classTestBase = TestBase(data['req_host'],data['schemes'], data['user_login_account'],  data['user_login_ps'], data['tenant_id'],tenant[data['tenant_id']], platformConfig,game_list)
    resp["data"] = classTestBase.testCaseGame()

    return json.dumps(resp)

@app.route('/', methods=['GET', 'POST'])
def index():
    print("flask app.route index")
    return render_template('index.html')

app.run(host='0.0.0.0', port=4444,debug=True)
# app.run(host='192.168.31.54', port=4444,debug=True)


print("finish..........")