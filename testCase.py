import requests,unittest


# url ="http://localhost:5000/mock/a/b"
#
# data =  "method=testmethod"
#
# r = requests.post(url=url, data=data)
# print r.text
class nothingRes(unittest.TestCase):
    def testGssLogTest(self):
        url = "http://localhost:5000/mock/a/b"
        data = "method=testmethodasdfasd"
        result = "nothing matched"
        realResult = requests.post(url=url, data=data).text

        self.failUnless(result == realResult,
                        "realResult is {realResult}".format(realResult=realResult))

if __name__ == '__main__':
    unittest.main()