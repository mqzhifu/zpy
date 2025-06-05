import random
import time
import uuid
import sys

class ApiReq:
    HttpRequest = None
    TenantCode = ""
    TenantId  = 0
    PlatformConfig = None

    def __init__(self, httpRequest,tenantCode,tenantId,platformConfig = None):
        self.HttpRequest = httpRequest
        self.TenantCode = tenantCode
        self.TenantId = tenantId
        self.PlatformConfig = platformConfig

        print("======ApiReq init:", tenantId,tenantCode)
        # print("======",platformConfig)

    def userAccountLogin(self,username,password):
        uri = "api/v1/client/ssocenter/sso/login"
        reqData = {"source": 3, "account": username, "password": password}

        htmlData, requestRecord = self.HttpRequest.req(uri, "POST", {}, reqData, "application/json")
        if requestRecord["http_res_code"] != 200:
            print(sys._getframe().f_code.co_name," failed HttpRequest:")
            return None, htmlData, requestRecord

        bussRes = self.HttpRequest.processBussData(htmlData)
        if (bussRes["code"] != 0):
            print(sys._getframe().f_code.co_name,"failed processBussData：", bussRes)
            return bussRes, htmlData, requestRecord

        print(sys._getframe().f_code.co_name," ok,token:", bussRes["data"]["token"])
        return bussRes, htmlData, requestRecord

    def userSmsRegisterV3(self,username):
        uri = "api/v1/client/usercenter/registerV3"
        reqData =  {
            "passwordLogin": False,
            "phone": username,
            "verifyCode": "123456",
            "userId": "",
            "countryCode": "91",
            "source": 2,
            "password": "1749030948637",
            "channel": "basic"
        }

        htmlData, requestRecord = self.HttpRequest.req(uri, "POST", {}, reqData, "application/json")
        if requestRecord["http_res_code"] != 200:
            print(sys._getframe().f_code.co_name, " failed HttpRequest:")
            return None, htmlData, requestRecord

        bussRes = self.HttpRequest.processBussData(htmlData)
        if (bussRes["code"] != 0):
            print(sys._getframe().f_code.co_name, "failed processBussData：", bussRes)
            return bussRes, htmlData, requestRecord

        return bussRes, htmlData, requestRecord


    def userSmsLogin(self,username):
        uri = "api/v1/client/ssocenter/sso/login/phone/code"
        reqData = {
            "phone": username,
            "verifyCode": "123456",
            "userId": "",
            "countryCode": "91",
            "source": 2,
            "password": "1749032896367"
        }

        htmlData, requestRecord = self.HttpRequest.req(uri, "POST", {}, reqData, "application/json")
        if requestRecord["http_res_code"] != 200:
            print(sys._getframe().f_code.co_name, " failed HttpRequest:")
            return None, htmlData, requestRecord

        bussRes = self.HttpRequest.processBussData(htmlData)
        if (bussRes["code"] != 0):
            print(sys._getframe().f_code.co_name, "failed processBussData：", bussRes)
            return bussRes, htmlData, requestRecord

        return bussRes, htmlData, requestRecord

    def sendSms(self,phoneNumber):
        uri ="api/v1/client/usercenter/verify-code/send"
        reqData = {"source": 2,"email": "","countryCode": "91","phoneNo": phoneNumber}

        htmlData, requestRecord = self.HttpRequest.req(uri, "POST", {}, reqData, "application/json")
        if requestRecord["http_res_code"] != 200:
            print(sys._getframe().f_code.co_name, " failed HttpRequest:")
            return None, htmlData, requestRecord

        bussRes = self.HttpRequest.processBussData(htmlData)
        if (bussRes["code"] != 0):
            print(sys._getframe().f_code.co_name, "failed processBussData：", bussRes)
            return bussRes, htmlData, requestRecord

        return bussRes, htmlData, requestRecord

    # def getGameId(self):
    #     gameId = 1657027833
    #     if self.TenantCode == "india":
    #         gameId = 117018
    #     return gameId
    # def getGameCode(self):
    #     gameCode = "vs25rlbank"
    #     if self.TenantCode == "india":
    #         gameCode = "8911"
    #
    #     return gameCode


    def gameLogin(self,gameId,gameCode):
        uri =  "api/v1/client/game/login"
        # gameId = 1657027833
        # gameCode = "vs25rlbank"
        # if self.TenantCode == "india":
        #     gameId = 117018
        #     gameCode = "8911"
        print("======",gameId,gameCode)
        reqData = {
            # "gameId": self.getGameId(),
            # "gameCode": self.getGameCode(),
            "gameId": int(gameId),
            "gameCode": gameCode,
            "isMobile": True,
            "language": "zh_CN",
            "platformCode": self.getPlatformConfigOne("platform_code").upper(),
            "backUrl": "https://client-h5-dev.3333d.vip"
        }

        htmlData, requestRecord = self.HttpRequest.req(uri, "POST", {}, reqData, "application/json")
        if requestRecord["http_res_code"] != 200:
            print(sys._getframe().f_code.co_name," failed")
            return None,htmlData, requestRecord

        bussRes = self.HttpRequest.processBussData(htmlData)
        if (bussRes["code"] != 0):
            print(sys._getframe().f_code.co_name," failed processBussData：", bussRes)

        return bussRes, htmlData, requestRecord

    def getPlatformConfigOne(self,key):
        return self.PlatformConfig[self.TenantCode][key]

    def getWallet(self,uid,gameId):
        playerName = self.getUserGameName(uid)
        uri =  "api/v1/thirdgame/callback/"+self.getPlatformConfigOne("platform_code").lower()+"/"+self.TenantCode+"/Cash/Get?"
        # para = "game_id=8912&operator_token=3ef6c9b25ce74669af5865d45a0eb87d&player_name=CG1000010_14397010&secret_key=4a846e274ee4448390553913d30da060"
        # para = "game_id="+str(self.getGameId())+"&operator_token="+self.getPlatformConfigOne("token")+"&player_name="+playerName+"&secret_key="+self.getPlatformConfigOne("public_key")
        para = "game_id=" + gameId + "&operator_token=" + self.getPlatformConfigOne(
            "token") + "&player_name=" + playerName + "&secret_key=" + self.getPlatformConfigOne("public_key")

        # para +=  "&trace_id=67d164b9-83e6-4821-adb2-8cb6061198b2"
        para += "&trace_id="+str(uuid.uuid4())
        uri = uri + para

        htmlData, requestRecord = self.HttpRequest.req(uri, "POST", {}, {},"application/json")
        if requestRecord["http_res_code"] != 200:
            print(sys._getframe().f_code.co_name," failed")
            return None,htmlData, requestRecord

        data, htmlData,requestRecord =  self.HttpRequest.processCallbackBussData(htmlData, requestRecord)
        # if (data["code"] != 0):
        #     print("get_wallet failed：",data)
        #     return None,data, requestRecord

        return data,htmlData, requestRecord

    def getUserGameName(self, uid):
        return self.getPlatformConfigOne("platform_code").upper() + str(self.TenantId) + "_" + uid

    def gameBet(self,uid,gameCode):
        uri = "api/v1/thirdgame/callback/"+self.getPlatformConfigOne("platform_code").lower()+"/"+self.TenantCode+"/Cash/TransferInOut"
        betId = "333344" +str( int(round(time.time() * 1000)) )
        # playName = "CG"+str(self.TenantId) +"_" + uid
        playerName = self.getUserGameName(uid)
        transaction_id = "99999-8"+str(random.randint(1000,9999)) + "-7" +str(random.randint(10,99)) +"-6"

        currency_code = "BRL"
        if self.TenantCode == "india":
            currency_code = "IN"
        data ={
            "transfer_amount":-4.00,
            "bet_amount":4.00,
            "win_amount":0.00,
            "bet_id":betId,
            "bet_type":1,
            "create_time":int(round(time.time() * 1000)),
            "updated_time":int(round(time.time() * 1000)),
            "currency_code":currency_code,
            # "game_id":self.getGameCode(),
            "game_id":gameCode,
            "is_feature":False,
            "is_minus_count":True,
            "operator_token":self.getPlatformConfigOne("token"),
            "secret_key":self.getPlatformConfigOne("public_key"),
            "transaction_id":transaction_id,
            "parent_bet_id":betId,
            "player_name": playerName,
            "wallet_type":"C",
            "trace_id":str(uuid.uuid4()),
        }
        #     # htmlData, requestRecord = self.HttpRequest.req(uri, "POST", {}, {}, "multipart/form-data")
        htmlData, requestRecord = self.HttpRequest.req(uri, "POST", {}, data, "application/x-www-form-urlencoded")
        # print(htmlData)
        # print(requestRecord)
        if requestRecord["http_res_code"] != 200:
            print(sys._getframe().f_code.co_name," failed")
            return None, htmlData, requestRecord

        data, htmlData, requestRecord = self.HttpRequest.processCallbackBussData(htmlData, requestRecord)
        return data,htmlData, requestRecord
