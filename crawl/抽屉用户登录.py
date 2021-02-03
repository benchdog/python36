import requests

headers = {
    'authority': 'https://dig.chouti.com/login',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Mobile Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate',
    'Referer': 'https://dig.chouti.com/',
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
}
post_dict={
    'phone': '86 11位手机号','password': 'pwd','oneMonth': 1
}
response1 = requests.get(url='https://dig.chouti.com/')
cookies_1 = response1.cookies.get_dict()
print(cookies_1)

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