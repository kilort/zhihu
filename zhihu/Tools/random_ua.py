import random,linecache
#随机返回ua
def produce_ua():
    this_ua = linecache.getline("/home/hl/桌面/ubuntu/MINE/zhihu/zhihu/Tools/zhihu_ua.txt",random.randrange(1,80))
    return this_ua.strip()

if __name__ =="__main__":
    print(produce_ua())