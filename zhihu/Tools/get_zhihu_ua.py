import requests,time

#获取zhihu可用的最新ua

cookies = {'z_c0': '"MS4xTUZpRkFnQUFBQUFYQUFBQVlRSlZUVkxrZ0Z1RjB6bEFoZl9Udk4yYVE4U2lMeHpSWDhZb29nPT0=|1519621714|0c95f8a4d1c2001f22eac3f93b0c363d848c39a6"', 'l_n_c': '1'}
with open("/home/hl/桌面/ubuntu/MINE/zhihu/zhihu/Tools/ua.txt","r")as f:
    ua = f.readlines()
    f.close()

for i in ua:
    headers ={"User-Agent":i.strip()}
    response = requests.get(url = "https://www.zhihu.com/topic/19550994",headers =headers,cookies =cookies )

    print(i.strip())
    print(response.url)
    print("\n")
    time.sleep(3)
    if response.url !='https://www.zhihu.com/compatibility/index.html':
        with open("zhihu_ua.txt",'a')as f:
            f.write(i.strip()+'\n')
            f.close()