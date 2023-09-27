import apitest as at
import  os

def main():
    pwd = os.getcwd()
    print(pwd)

    apiTest = at.ApiTest("127.0.0.1","1111","http","D:/project/zpy/data/swagger.json")
    apiTest.run()

if  __name__ == "__main__" :
    main()
