import os
import apitest

def main():
    pwd = os.getcwd()
    data_path = pwd + "/data/"

    print("im in main ,  path:",pwd)

    api = apitest.ApiTest(data_path)
    api.start()

if  __name__ == "__main__" :
    main()
