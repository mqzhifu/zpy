import  json
import util.common
import logging

class ParserSwagger :
    path = ""
    data = []
    logLevel = 0

    def __init__(self, path,debug):
        self.path = path
        self.logLevel = debug

        # logging.basicConfig(format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s',level=logging.DEBUG)  # 配置输出格式、配置日志级别
        logging.basicConfig(format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s',level=logging.INFO)  # 配置输出格式、配置日志级别

        logging.info("swagger file:"+ path +", debug:"+ str(debug))

    # 读取 swagger 配置文件中的内容
    def loadSwaggerContent(self):
        with open(self.path, 'rb') as file:
            content = file.read()

        # 读取文件内容，解析 json 到 py 的变量中
        self.data = json.loads(content)

        if (not self.data):
            exit("swagger file content len = 0")

        logging.debug(self.data.keys())



    def checkFileContent(self):
        if(not util.common.key_exist_return_value(self.data,"info")):
            exit("swagger key empty:info")

        if(not util.common.key_exist_return_value(self.data,"paths")):
            exit("swagger key empty:paths")

        if(not util.common.key_exist_return_value(self.data,"definitions")):
            exit("swagger key empty:definitions")

        if(not util.common.key_exist_return_value(self.data,"securityDefinitions")):
            exit("swagger key empty:securityDefinitions")

        if(not util.common.key_exist_return_value(self.data,"tags")):
            exit("swagger key empty:tags")

    def startRun(self):
        logging.info("startRun:")

        self.loadSwaggerContent()
        self.checkFileContent()
        # 保存，最终解析好的所有数据
        final_data = []
        for path, methods in self.data["paths"].items():
            logging.debug("url: "+path)
            function_info = {"path":path,"method":"","header":{},"body":{},"desc":"","produces":"","consumes":"","security":""}
            for method, details in methods.items():
                # logging.debug("method:"+method)

                description = util.common.key_exist_return_value(details,"")
                produces = util.common.key_exist_return_value(details,"produdescriptionces")
                summary = util.common.key_exist_return_value(details,"summary")
                tags = util.common.key_exist_return_value(details,"tags")

                function_info["desc"] = description
                function_info["produces"] = "".join(produces)
                function_info["method"] = method.upper()
                function_info["tags"] =  ''.join(tags)
                function_info["summary"] = summary

                if(util.common.key_exist_return_value(details,"consumes")):
                    function_info["consumes"] = "".join(details ["consumes"])

                if(util.common.key_exist_return_value(details,"security")):
                    function_info["security"] = details["security"]

                # logging.debug(function_info)

                parameters = util.common.key_exist_return_value(details, "parameters")
                if (parameters):
                    function_info = self.processParameters(parameters,function_info)
                else :
                    logging.error("no parameters")

                logging.debug(function_info)

            final_data.append(function_info)

        data = {"securityDefinitions":self.data["securityDefinitions"],"list":final_data}
        # self.show(final_data)
        return data

    # 处理一个函数的，所有请求的参数
    def processParameters(self,parameters,function_info):

        for parameter in parameters:
            # 参数是一个大json 对象
            if ('schema' in parameter.keys()):
                refObjectName = self.getSchemaRef(parameter["schema"]["$ref"])
                function_info["body"] = self.processDefinitions(self.data["definitions"][refObjectName])
            # 参数是一个普通类型
            else:
                parameterType = parameter["in"]
                key = parameter["name"]
                logging.debug(__name__ +" key:" + key + " type:" + parameterType)
                if (parameterType == "header"):
                    function_info["header"][key] = self.parserOneParaTypeValue(parameter)
                elif (parameterType == "path"):
                    function_info["path"] = function_info["path"].replace("{"+key+"}", "unknow")
                elif (parameterType == "formData"):
                    function_info["body"][key] = self.parserOneParaTypeValue(parameter)
                else:
                    logging.error("err1:========", parameterType)
                    exit()

        return function_info

    def processDefinitions(self,definitions):
        if definitions["type"] != "object":
            logging.error("err2 in processDefinitions, no object")
            exit()

        properties = util.common.key_exist_return_value(definitions, "properties")
        if ( not properties):
            logging.error("err3:no properties")
            return ""

        ob = {}
        for key,definition in properties.items():
            # logging.info(key,definition)
            ob[key] = self.parserOneParaTypeValue(definition)

        return ob

    def getSchemaRef(self,ref):
        # ref = parameter["$ref"]
        logging.debug("schema $ref:" +  ref)
        refSplit = ref.split("/")
        return refSplit[2]

    def parserOneParaTypeValue(self,parameter):
        prefix = "parserOneParaTypeValue type:"
        if(util.common.key_exist_return_value(parameter,"$ref")):

            refObjectName = self.getSchemaRef(parameter["$ref"])
            return self.processDefinitions(self.data["definitions"][refObjectName ])

        if (parameter['type'] == "string"):
            logging.debug(__name__ + "string")
            return ""
        elif (parameter['type'] == "integer"):
            return 0
            logging.debug(__name__ +"integer")
        elif (parameter['type'] == "boolean"):
            return False
            logging.debug(prefix,"bool")
        elif (parameter['type'] == "file"):
            logging.debug(__name__ +"err5 file")
            return "file"
        elif (parameter['type'] == "array"):
            logging.debug(__name__ +"array:",parameter)
            self.parserOneParaTypeValue(parameter["items"])
        elif (parameter['type'] == "object"):
            logging.debug(__name__ +"object:", parameter)
            if(prefix,util.common.key_exist_return_value(parameter,"additionalProperties")):
                #这是种特殊类型，是一个 map
                logging.debug("additionalProperties")
            else:
                logging.error("err6 object")
                exit()
        else:
            logging.error("err7:", parameter)
            exit()

    def show(self,data):
        self.pp("=========")
        self.pp("=========")
        self.pp("=========")
        self.pp("=========")
        self.pp("=========")

        for row in data:
            self.pp(row)


    def pp (self,*args):
        if(self.logLevel <= 0 ):
            return

        print(*args)