import random
import linecache
import json
def produce_cookies():
    with open("/home/hl/桌面/ubuntu/MINE/zhihu/zhihu/Tools/cookies.txt","r")as f:
        cookies = f.readline()
        f.close()

    return cookies


if __name__ =="__main__":
    print(produce_cookies())