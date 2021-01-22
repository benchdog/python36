# -*- coding: utf-8 -*-
# https://www.douban.com/group/opking/-------北京个人租房 （真房源|无中介）
# https://www.douban.com/group/beijingzufang/北京租房
# https://www.douban.com/group/26926/--------北京租房豆瓣
# https://www.douban.com/group/zhufang/------北京无中介租房
# https://www.douban.com/group/279962/-------北京租房（非中介）
# https://www.douban.com/group/257523/-------北京租房房东联盟(中介勿扰)
# https://www.douban.com/group/sweethome/----北京租房（密探）
# https://www.douban.com/group/252218/-------北京租房专家
# https://www.douban.com/group/625354/-------北京租房（真的没有中介）小组
# https://www.douban.com/group/550436/-------☀北京租房大全【推荐★★★★★】
# https://www.douban.com/group/465554/-------北京 租房 房东 直租（非中介）

import datetime

import bs4
import random
import requests

userAgent = [
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52"]

headers = {'User-agent': random.choice(userAgent)}
# group = ['opking', 'beijingzufang', '26926', 'zhufang', '279962', '257523',
group = ['267904']

publisher = []
PT = (datetime.datetime.now() - datetime.timedelta(days=30)).strftime("%Y-%m-%d %H:%M:%S")

for g in group:
    print('租房小组：'+ g)
    for page in range(0, 30):
        url = 'https://www.douban.com/group/' + g + '/discussion?start=' + str(page * 25)
        response = requests.get(url, headers=headers).text
        soup = bs4.BeautifulSoup(response, "html.parser")
        rent_info_list = soup.select('td[class="title"]')
        include = ['翟东小区', '谈固']  # 填入各种想要筛选的关键词
        exclude = ['单间']  # '单间','次卧','主卧','室友'

        for rent_info in rent_info_list:
            rent_title = (rent_info.a['title'].replace('\u2661',''))
            rent_link = (rent_info.a['href'])
            for i in include:
                if i in rent_title:
                    print(rent_title)
                    print(rent_link)
            #
            # # 将标题和租房信息整合
            # response = requests.get(rent_link, headers=headers).text
            # soup = bs4.BeautifulSoup(response, "html.parser")
            # post_title = soup.select('td[class="tablecc"]')
            # post_time = soup.select('span[class="from"]')
            # print(post_title.a['href'])
            # print(post_time)
            # w = []
            # for wb in wenben:
                # w.append(wb.text)
                # print('???' + wb.text)
                # print("!!!")
            # quanbu = '.'.join(w) + rent_title

            # 提取时间
            # SJ = []
            # sj = soup.select('span[class="color-green"]')
            # for page in sj:
            #     SJ.append(page.text)
            # shijian = ''.join(SJ)
            # # print(publisher)
            # # 提取发布人
            # fb = []
            # fbid = soup.select('span[class="from"]')
            # for rent_info in fbid:
            #     fb.append(rent_info.a['href'])
            # FBid = ''.join(fb)
            #
            # # 满足各种条件
            # if shijian > PT:
            #     # print(lianjie,biaoti)
            #     if all(abc not in quanbu for abc in exclude):  # 排除掉了室友这些
            #         for page in include:
            #             if page in quanbu:
            #                 if FBid not in publisher:
            #                     publisher.append(FBid)
                                # print(rent_title)
                                # print(rent_link + '\n===================')
        # time.sleep(random.randint(5,9))
