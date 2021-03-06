# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from .Tools.random_ua import produce_ua
from .Tools.return_proxy import produce_ip
from .Tools.return_cookies import produce_cookies

class ZhihuSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)



class RandomUAMiddleware(object):
    def process_request(self,request,spider):
        UA =  'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/63.0.3239.84 Chrome/63.0.3239.84 Safari/537.36'

        print(UA)
        request.headers.setdefault(b'User-Agent',UA)

#生成proxy并调用
class RandomProxyIPMiddlware(object):
    def process_request(self, request, spider):
        proxy =produce_ip()
        print(proxy)
        request.meta["proxy"] = proxy


class ZhihuCookiesMiddleware(object):
    #cookie
    def process_request(self,request,spider):
        cookies= produce_cookies()
        print(cookies)
        request.cookies = {'z_c0': '"MS4xTUZpRkFnQUFBQUFYQUFBQVlRSlZUWmZfZ0Z0cEU2T3BXWnlmY0RtVlQtMjdzWU1MSkxCOHh3PT0=|1519628696|d7901832ceda7407c6c9d86d024268a0f509628a"', 'l_n_c': '1'}
