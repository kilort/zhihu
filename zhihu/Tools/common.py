import re,datetime
from zhihu.settings import *
import hashlib


def get_md5(obj):
    #获取md5形式的数据
    if isinstance(obj,str):
        url = obj.encode("utf-8")  # 将uncoide编码的url转化为utf-8
        m = hashlib.md5()
        m.update(url)
        return m.hexdigest()  # 提取出md5的值
        

def get_str(obj):
    #字符串提取
    if isinstance(obj,list):
        if len(obj)>0:
            obj = ','.join(obj).strip()
            tag = re.compile(r'<[^>]+>', re.S)
            obj = tag.sub('', obj)
            return obj
        else:
            return "None"
    elif isinstance(obj,str):
        obj = obj.strip()
        tag = re.compile(r'<[^>]+>', re.S)
        obj = tag.sub('', obj)
        return obj
    
    elif isinstance(obj,int):
         return obj
    else:
        return "None"


def get_num(obj):
    #数字提取
    if isinstance(obj,list):
        obj = get_str(obj)
        if ',' in obj:
            obj = obj.replace(',','')
        else:
            obj = obj
        num = '[0-9]+'
        obj = re.compile(num).findall(obj)
        if len(obj)>0:
            num = int(obj[0])
            return num
        else:
            return 0
        
    elif isinstance(obj,int):
        return obj

    elif isinstance(obj,str):
        if ',' in obj:
            obj = obj.replace(',','')
        else:
            obj = obj
        num = '[0-9]+'
        obj = re.compile(num).findall(obj)
        if len(obj)>0:
            num = int(obj[0])
            return num
        else:
            return 0
    else:
        return 0

def get_now():
    return datetime.datetime.now().strftime(SQL_DATETIME_FORMAT1)

def get_datetime(obj):
    #时间提取
    if isinstance(obj,int):
        #int类型的datetime转换
        this_datetime = datetime.datetime.fromtimestamp(obj).strftime(SQL_DATETIME_FORMAT1)

    else:
        this_datetime = datetime.datetime.strptime(ERROR_DATETIME,SQL_DATETIME_FORMAT2).date()
    return this_datetime

if __name__=="__main__":
    print(get_num(12121))
    print(get_datetime("sdadada"))
    print(get_now())
