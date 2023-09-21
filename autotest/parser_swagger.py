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

        logging.basicConfig(format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s',
                            level=logging.INFO)  # 配置输出格式、配置日志级别

        logging.info("swagger file:"+ path +", debug:"+ str(debug))

    def startRun(self):
        logging.info("startRun:")
        # 打开源文件
        with open(self.path, 'rb') as file:
            content = file.read()
        # 读取文件内容，解析 json 到 py 的变量中
        self.data = json.loads(content)

        logging.debug(self.data.keys())
        # print(self.data["definitions"])

        final_data = []
        paths = self.data["paths"]
        for path, methods in paths.items():
            logging.debug("url: "+path)
            function_info = {"path":path,"method":"","header":{},"body":{},"desc":"","produces":"","consumes":""}
            for method, details in methods.items():
                logging.debug("method:"+method)
                function_info["method"] = method.upper()

                description = util.common.key_exist_return_value(details,"")
                produces = util.common.key_exist_return_value(details,"produdescriptionces")
                summary = util.common.key_exist_return_value(details,"summary")
                tags = util.common.key_exist_return_value(details,"tags")

                logging.debug("desc:"+description +  ',produces:'.join(produces)   + ",summary:"+ summary +  ''.join(tags))

                function_info["desc"] = description
                function_info["produces"] = "".join(produces)

                if(util.common.key_exist_return_value(details,"consumes")):
                    function_info["consumes"] = "".join(details ["consumes"])

                parameters = util.common.key_exist_return_value(details, "parameters")
                if (parameters):
                    function_info = self.processParameters(parameters,function_info)
                else :
                    logging.error("no parameters")

                logging.debug(function_info)

            final_data.append(function_info)

        # self.show(final_data)
        return final_data

    def processParameters(self,parameters,function_info):

        for parameter in parameters:
            if ('schema' in parameter.keys()):
                ref = parameter["schema"]["$ref"]
                logging.debug(__name__ + " schema $ref:" + ref)
                refSplit = ref.split("/")

                function_info["body"] = self.processDefinitions(self.data["definitions"][refSplit[2]])
            else:
                parameterType = parameter["in"]
                key = parameter["name"]
                logging.debug(__name__ +" key:" + key + " type:" + parameterType)
                if (parameterType == "header"):
                    function_info["header"][key] = self.parserOneParaTypeValue(parameter)
                elif (parameterType == "path"):
                    # print(function_info["path"],self.parserOneParaTypeValue(parameter),"{"+key+"}")
                    function_info["path"] = function_info["path"].replace("{"+key+"}", "unknow")
                    # print(function_info["path"])
                elif (parameterType == "formData"):
                    function_info["body"][key] = self.parserOneParaTypeValue(parameter)
                else:
                    logging.error("err1:========", parameterType)
                    exit()

        return function_info
        # exit()
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

    def parserOneParaTypeValue(self,parameter):
        prefix = "parserOneParaTypeValue type:"
        if(util.common.key_exist_return_value(parameter,"$ref")):
            ref = parameter["$ref"]
            logging.debug("schema $ref:" +  ref)
            refSplit = ref.split("/")

            # self.pp(prefix," error4:",refSplit)

            return self.processDefinitions(self.data["definitions"][refSplit[2]])



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