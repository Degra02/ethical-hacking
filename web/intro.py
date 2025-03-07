import requests as r


base_url = "http://cyberchallenge.disi.unitn.it:7900"

s = r.Session()

# response = s.get(base_url + "/api/get")
# data = response.json()
#
#
# res = s.head(base_url + "/api/head_request_123") 
#
#
# res = s.post(base_url + "/api/post_456_request", json={"secret_payload": "a_JSON_payload"}, headers={"Content-Type": "application/json"})
#
#
# res = s.get(base_url + "/api/cookie", cookies={"secret": "this_is_the_secret_cookie"})
#
#
# res = s.get(base_url + "/api/query", params={"secret": "secret_query_parameter"})
#
#
res = s.get(base_url + "/api/header_78_9", headers={"X-Secret": "this_is_the_secret_header"})

print(res.json()['flag'])
