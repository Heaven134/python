import json

obj= { 'error_code': 22000, 'result': [ { [ { 'actid': 1, 'itemid': 2, 'userid': 3, 'score': 10, 'time':1234567 }, { 'actid': 1, 'itemid': 3, 'userid': 4, 'score': 9, 'time':1233567 } ] } ] }
encodedjson = json.dumps(obj)
decodejson = json.loads(encodedjson)
print decodejson['result']
