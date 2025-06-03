import random
import time
import uuid


class ApiReq:
    HttpRequest = None
    TenantCode = ""
    TenantId  = 0
    def __init__(self, httpRequest,TenantCode,TenantId):
        self.HttpRequest = httpRequest
        self.TenantCode = TenantCode
        self.TenantId = TenantId

    def userLogin(self,username,password):
        uri = "api/v1/client/ssocenter/sso/login"
        reqData = {"source": 3, "account": username, "password": password}

        htmlData, requestRecord = self.HttpRequest.req(uri, "POST", {}, reqData, "application/json")
        if requestRecord["http_res_code"] != 200:
            print("userLogin failed HttpRequest:")
            return None, htmlData, requestRecord

        data, requestRecord = self.HttpRequest.processBussData(htmlData, requestRecord)
        if (data["code"] != 0):
            print("userLogin failed processBussData：", data)
            return data, htmlData, requestRecord

        # print("userLogin ok, data :" ,data)
        print("userLogin ok,token:", data["data"]["token"])
        return data, htmlData, requestRecord



    def gameLogin(self):
        uri =  "api/v1/client/game/login"
        reqData = {
            "gameId": 1657027833,
            "gameCode": "vs25rlbank",
            "isMobile": True,
            "language": "zh_CN",
            "platformCode": "PP",
            "backUrl": "https://client-h5-dev.3333d.vip"
        }

        htmlData, requestRecord = self.HttpRequest.req(uri, "POST", {}, reqData, "application/json")
        if requestRecord["http_res_code"] != 200:
            print("gameLogin failed")
            return None,htmlData, requestRecord

        data, requestRecord = self.HttpRequest.processBussData(htmlData, requestRecord)
        if (data["code"] != 0):
            print("userLogin failed processBussData：", data)
            return data, htmlData, requestRecord

        return data, htmlData, requestRecord


    def getWallet(self):
        uri =  "api/v1/thirdgame/callback/cg/"+self.TenantCode+"/Cash/Get?"
        para = "game_id=8912&operator_token=3ef6c9b25ce74669af5865d45a0eb87d&player_name=CG1000010_14397010&secret_key=4a846e274ee4448390553913d30da060"
        para +=  "&trace_id=67d164b9-83e6-4821-adb2-8cb6061198b2"
        uri = uri + para

        htmlData, requestRecord = self.HttpRequest.req(uri, "POST", {}, {},"application/json")
        if requestRecord["http_res_code"] != 200:
            print("gameLogin failed")
            return None,htmlData, requestRecord

        data, htmlData,requestRecord =  self.HttpRequest.processCallbackBussData(htmlData, requestRecord)
        # if (data["code"] != 0):
        #     print("get_wallet failed：",data)
        #     return None,data, requestRecord

        return data,htmlData, requestRecord




    def gameBet(self,uid):
        uri = "api/v1/thirdgame/callback/cg/"+self.TenantCode+"/Cash/TransferInOut"

        betId = "333344" +str( int(round(time.time() * 1000)) )
        playName = "CG"+str(self.TenantId) +"_" + uid
        # 'trace_id="4216eb15-6014-403d-8bcd-4c97e9671c91"'
        print("================ gameBet ==========")
        #                "06581-00936-106-2"
        transaction_id = "99999-8"+str(random.randint(1000,9999)) + "-7" +str(random.randint(10,99)) +"-6"
        data ={
            "transfer_amount":-4.00,
            "bet_amount":4.00,
            "win_amount":0.00,
            "bet_id":betId,
            "bet_type":1,
            "create_time":int(round(time.time() * 1000)),
            "updated_time":int(round(time.time() * 1000)),
            "currency_code":"BRL",
            "game_id":8912,
            "is_feature":False,
            "is_minus_count":True,
            "operator_token":"3ef6c9b25ce74669af5865d45a0eb87d",
            "secret_key":"4a846e274ee4448390553913d30da060",
            "transaction_id":transaction_id,
            "parent_bet_id":betId,
            "player_name": playName,
            "wallet_type":"C",
            "trace_id":str(uuid.uuid4()),
        }
        #     # htmlData, requestRecord = self.HttpRequest.req(uri, "POST", {}, {}, "multipart/form-data")
        htmlData, requestRecord = self.HttpRequest.req(uri, "POST", {}, data, "application/x-www-form-urlencoded")
        # print(htmlData)
        # print(requestRecord)
        # if requestRecord["http_res_code"] != 200:
        #     print("gameLogin failed")
        #     return None, htmlData, requestRecord
        #
        data, htmlData, requestRecord = self.HttpRequest.processCallbackBussData(htmlData, requestRecord)
        return data,htmlData, requestRecord
