#coding=utf-8
matchRes = {
    "method=aa":{
        "a=1&b=1":"aaaheheda",
        "a=1&b=2":"aaaxiexie"
    },
    "method=bb":{
        "a=1&b=1": "bbbheheda",
        "a=1&b=2": "bbbxiexie"
    }

}

requestDic={}



#参数关键字配置，建议加上等号以避免匹配错误
keyPara="key="