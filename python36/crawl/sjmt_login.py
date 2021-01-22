import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36','Referer': 'http://10.41.77.13/sjmt/login','Accept':'application/json','Accept-Encoding':'gzip, deflate','Accept-Language':'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
'Connection':'keep-alive','Content-Length':'65','Content-Type':'application/json','Host':'10.41.77.13',
}
post_dict={'userName': 'sjmt','password': '1'}
# res = requests.get(url='http://10.41.77.13/mt-api/login')
res = requests.post(url='http://10.41.77.13/mt-api/login',data=post_dict,headers=headers)

# cookies_1 = res.cookies.get_dict()
# print(cookies_1)
print(res.text)

# response2 = requests.post(url='https://dig.chouti.com/login',data=post_dict,headers=headers)
# cookies_2 = response2.cookies.get_dict()
# # print(response2.text)
# print(cookies_2)

# post_dict3={'linksId':'20696451'}
# response3 = requests.post(url='https://dig.chouti.com/link/vote',cookies={'gpsd':'0ac31f5be58bc5b7107db2338c24dcd5'},data=post_dict3,headers=headers)
# print(response3.text)
# # print(response3.cookies.get_dict())

# response4 = requests.get(url='https://dig.chouti.com/profile',cookies={'gpsd':'0ac31f5be58bc5b7107db2338c24dcd5'},headers=headers)
# print(response4.text)