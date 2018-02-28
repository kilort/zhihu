import random

def produce_ip():
    #返回代理ip
    with open("/home/hl/桌面/share/share_ip.txt") as f:
     ip = random.choice(f.readlines())
    proxy = "http://"+str(ip)
    return proxy

if __name__=="__main__":
    print(produce_ip())