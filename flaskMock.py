#coding=utf-8
from time import sleep

from flask import Flask
from flask import jsonify
from flask import request
from configFile import *
import os


from werkzeug.routing import BaseConverter
class RegexConverter(BaseConverter):
    def __init__(self, map, *args):
        self.map = map
        self.regex = args[0]
configDic = {}
app = Flask(__name__)
app.url_map.converters['regex'] = RegexConverter


# @app.route('/view/<regex("[a-zA-Z0-9]+"):uuid>/')
@app.route('/mock/<regex(".*"):apiUri>',methods=["POST","GET"])
# def mock(apiUri):
#     print apiUri
#     return 'Hello World !'
def postService(apiUri):
    res = "nothing matched"
    requestBody = request.data if request.data else request.get_data()
    print "requestBody is:",requestBody
    requestBodyParse = requestBody.strip().split("&")
    if apiUri in configDic.keys():
        for key in configDic[apiUri].keys():
            print key.split("&")
            keyPicList = key.split("&")
            ######找出请求消息体最匹配哪个需要返回的消息
            for para in requestBodyParse:
                if para in keyPicList:
                    keyPicList.remove(para)
                if not keyPicList :
                    res = configDic[apiUri][key]
                    print type(res)
                    if "timeout" in res:

                        sleepTime = int(res.strip("timeout").strip("s"))
                        sleep(sleepTime)
                        return res
                    return res
    return  res

def resolveConfig():
    parPath = os.path.dirname(__file__)
    configFilePath = os.path.join(parPath,"simpleConfig.py")
    with open(configFilePath,"r") as f:
        for line in f:
            twoParts = line.rstrip().split("===")
            if ":" in twoParts[0]:
                (uri,condition) = twoParts[0].split(":")
            else:
                (uri, condition) = twoParts[0],"noCondition"
            if configDic.has_key(uri):
                pass
            else:
                configDic[uri] = {}
            configDic[uri][condition] = twoParts[1]
    return configDic


if __name__ == '__main__':
    resolveConfig()
    print configDic
    app.run(host="0.0.0.0",debug=True)
