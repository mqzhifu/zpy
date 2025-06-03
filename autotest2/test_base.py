import random

from flask import Flask
from flask import render_template
import uuid
import yaml
import time
import httpReq
import apiReq

class TestBase:
    SwaggerData = None
    HttpRequest = None
    ApiReq = None

    UserLoginData = ""
    Username = ""
    Password = ""
    TenantCode = ""
    TenantId = 0

    def __init__(self,username,password,tenantId,tenantCode):
        # self.SwaggerData =  get_swagger_yaml()

        self.Username = username
        self.Password = password
        self.TenantId = tenantId
        self.TenantCode = tenantCode

        # self.HttpRequest = httpReq.HttpRequest(self.SwaggerData['schemes'][0],self.SwaggerData['host'],self.getCommonHeader())
        self.HttpRequest = httpReq.HttpRequest("https", "api-c.test.3333d.vip",self.getCommonHeader())


        self.ApiReq = apiReq.ApiReq(self.HttpRequest,self.TenantCode,self.TenantId )

        print("TestBase init ok " )

    def testCaseGame(self):
        res = {
            "user_login":{"id":1,"bussData":self.HttpRequest.getBussDataRecord(),"reqRes":self.HttpRequest.getEmptyRecord(),"name":"user_login"},
            "game_login": {"id":2,"bussData": self.HttpRequest.getBussDataRecord(),"reqRes": self.HttpRequest.getEmptyRecord(),"name":"game_login"},
            "get_wallet": {"id":3,"bussData": self.HttpRequest.getBussDataRecord(),"reqRes": self.HttpRequest.getEmptyRecord(),"name":"get_wallet"},
            "game_bet": {"id":4,"bussData": self.HttpRequest.getBussDataRecord(),"reqRes": self.HttpRequest.getEmptyRecord(),"name":"game_bet"},
        }

        data,htmlData, requestRecord = self.ApiReq.userLogin(self.Username,self.Password )
        res["user_login"]["bussData"] = data
        res["user_login"]["reqRes"] = requestRecord

        if requestRecord["http_res_code"] != 200 or data["code"] != 0:
            print("userLogin failed ",data,htmlData,requestRecord)
            return res

        self.UserLoginData = data
        self.HttpRequest.Headers = self.getCommonHeader()

        data, htmlData, requestRecord =  self.ApiReq.gameLogin()

        res["game_login"]["bussData"] = data
        res["game_login"]["reqRes"] = requestRecord

        if requestRecord["http_res_code"] != 200 or data["code"] != 0:
            print("gameLogin failed ",data,htmlData,requestRecord)
            return res



        data, htmlData, requestRecord = self.ApiReq.getWallet()
        res["get_wallet"]["bussData"] = data
        res["get_wallet"]["reqRes"] = requestRecord

        # if requestRecord["http_res_code"] != 200 or data["code"] != 0:
        #     print("getWallet failed ",data,htmlData,requestRecord)
        #     return res
        data, htmlData, requestRecord = self.ApiReq.gameBet(self.UserLoginData["data"]["userId"])
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
        # and self.userLoginData["data"] and self.userLoginData["data"]["token"]
        if self.UserLoginData:
            headers["Authorization"] = "Bearer "+ self.UserLoginData["data"]["token"]

        return headers

def get_swagger_yaml():
    yamlPath = "/Users/clarissechamley/data/gambl/thirdgame/thirdgame_tenant_api/docs/all.yaml"
    # open方法打开直接读出来
    f = open(yamlPath, 'r', encoding='utf-8')
    cfg = f.read()
    # print(type(cfg))  # 读出来是字符串
    # print(cfg)
    dataMap = yaml.load(cfg,Loader=yaml.FullLoader)   # 用load方法转字典
    return dataMap


username = "mqzhifu"
password ="mqzhifu123"
tenantId = 1000010
tenantCode = "brabxbwptnb"
# tenantId = 10049223
# tenantCode = "india"

classTestBase = TestBase(username,password,tenantId,tenantCode)
apiRes = classTestBase.testCaseGame()


# ============== http ========================================
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    print("flask app.route index")
    return render_template('index.html',username=username,tenantId=tenantId,tenantCode=tenantCode,apiRes=apiRes)

app.run(host='0.0.0.0', port=4444,debug=True)


print("finish..........")