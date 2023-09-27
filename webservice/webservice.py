import  os
from flask import  Flask
from flask import  render_template

import  autotest.apitest as at

def main():
    pwd = os.getcwd()
    print(pwd)



    app=Flask("webservice")
    app.jinja_env.filters['getDefaultValue'] = getDefaultValue
    app.jinja_env.filters['filterUrlPrefix'] = filterUrlPrefix



    @app.route('/')
    def index():
        return 'welcome to my webpage!'

    @app.route('/favicon.ico')
    def favicon():
        return ''

    @app.route('/apitest')
    def apitest():
        apiTest = at.ApiTest("127.0.0.1","1111","http","D:/project/zpy/data/swagger.json")
        tableDataList,tableHeader,metrics = apiTest.run()

        urlPrefix = apiTest.getUrlPrefix()
        return render_template("apitest.html",tableDataList=tableDataList,tableHeader=tableHeader,metrics=metrics,exceptApiPath=apiTest.exceptApiPath,urlPrefix=urlPrefix,filterUrlPrefix=filterUrlPrefix)


    app.run(port=2020,host="127.0.0.1",debug=True)

def getDefaultValue(value):
    if (value):
        return value

    if isinstance(value,str):
        return "-"

    return value

def filterUrlPrefix(value,urlprefix):
    if (not value):
        return value


    if isinstance(value,str):
        return value.replace(urlprefix,"")

    return value



if  __name__ == "__main__" :
    main()
