
__name__ = '调试文件'
from scrapy.cmdline import execute
import sys
import os


print(os.path.dirname(os.path.abspath(__file__)))
# 调用本地文件的位置
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
execute(["scrapy","crawl","zhihu_spider"])

