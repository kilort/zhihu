# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request,FormRequest
import json,re,time
from urllib import parse
from scrapy.loader import ItemLoader
from zhihu.items import ZhihuAnswerItem,ZhihuQuestionItem,ZhihuUserItem
from zhihu.settings import *
from zhihu.Tools.common import get_md5
from scrapy_redis.spiders import RedisSpider

class ZhihuSpiderSpider(RedisSpider):
    name = 'zhihu_spider'
    redis_key = 'Zhihu:start_urls'

    # allowed_domains = ['www.zhihu.com']
    # start_urls = ['https://www.zhihu.com']
    cookies = {"your_cookie"}
    topic_question_api = "http://www.zhihu.com/api/v4/topics/{0}/feeds/top_activity?include=data%5B%3F%28target.type%3Dtopic_sticky_module%29%5D.target.data%5B%3F%28target.type%3Danswer%29%5D.target.content%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%3Bdata%5B%3F%28target.type%3Dtopic_sticky_module%29%5D.target.data%5B%3F%28target.type%3Danswer%29%5D.target.is_normal%2Ccomment_count%2Cvoteup_count%2Ccontent%2Crelevant_info%2Cexcerpt.author.badge%5B%3F%28type%3Dbest_answerer%29%5D.topics%3Bdata%5B%3F%28target.type%3Dtopic_sticky_module%29%5D.target.data%5B%3F%28target.type%3Darticle%29%5D.target.content%2Cvoteup_count%2Ccomment_count%2Cvoting%2Cauthor.badge%5B%3F%28type%3Dbest_answerer%29%5D.topics%3Bdata%5B%3F%28target.type%3Dtopic_sticky_module%29%5D.target.data%5B%3F%28target.type%3Dpeople%29%5D.target.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F%28type%3Dbest_answerer%29%5D.topics%3Bdata%5B%3F%28target.type%3Danswer%29%5D.target.content%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%3Bdata%5B%3F%28target.type%3Danswer%29%5D.target.author.badge%5B%3F%28type%3Dbest_answerer%29%5D.topics%3Bdata%5B%3F%28target.type%3Darticle%29%5D.target.content%2Cauthor.badge%5B%3F%28type%3Dbest_answerer%29%5D.topics%3Bdata%5B%3F%28target.type%3Dquestion%29%5D.target.comment_count&limit={1}"
    question_api = "http://www.zhihu.com/api/v4/questions/{0}/answers?sort_by=default&include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cupvoted_followees%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cbadge%5B%3F%28type%3Dbest_answerer%29%5D.topics&limit={1}&offset={2}"
    user_answer_api = "https://www.zhihu.com/api/v4/members/{0}/answers?include=data%5B*%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Cmark_infos%2Ccreated_time%2Cupdated_time%2Creview_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cvoting%2Cis_author%2Cis_thanked%2Cis_nothelp%2Cupvoted_followees%3Bdata%5B*%5D.author.badge%5B%3F(type%3Dbest_answerer)%5D.topics&offset={1}&limit={2}&sort_by=created"



    # def start_requests(self):
    #     url = "https://www.zhihu.com/topics"
    #     yield Request(url=url, callback=self.parse)

    def parse(self, response):
        #提取知乎话题广场所有一级分类话题的url
        urls = response.xpath('//ul[@class="zm-topic-cat-main clearfix"]/li/a/@href').extract()
        if len(urls) > 0:
            for url in urls:
                url = parse.urljoin(response.url, url)
                yield Request(url=url, callback=self.parse_second, dont_filter=True,cookies=self.cookies)
                break
        '''topic_url是通过ajax传输的，在topics页面构造post请求，获取json数据，达到请求topic下面生成的ajax数据，
            最终获取到question_id,见注释部分的代码逻辑'''
        # topics_id = response.xpath('//ul[@class="zm-topic-cat-main clearfix"]/li/@data-id').extract()
        # url_topic = list(zip(url,topics_id))
        # for i in url_topic:
        #     if len(i) == 2:
        #         url = parse.urljoin(self.start_urls[0],i[0])
        #         topics_id = i[1]
        #         post_url = "https://www.zhihu.com/node/TopicsPlazzaListV2"
        #         post_data = {
        #         "topic_id": topics_id,
        #         "offset": 0,
        #         "hash_id": "825da520ff82d2d8d40497c8d87925c8"#用户 id
        #         }
        #         yield FormRequest(url=post_url,
        #                           ormdata=post_data,
        #                           callback=self.second_topic_api,
        #                           meta = {"topics_id":topics_id}
        #                           )

    # def second_topic_api(self,response):
    #     response_json = json.loads(response.text)
    #     msg = response_json["msg"]
    #     offset = int(len(response_json["msg"]))
    #     for i in msg:
    #         topic_key = re.compile('<a target.*?href="(.*?)"',re.DOTALL).findall(i)
    #         if len(topic_key) != 0:
    #             topic_key = topic_key[0]
    #             url = parse.urljoin(self.start_urls[0],topic_key)
    #             yield Request(url = url,callback=self.get_topic_key)
    #     post_url = "https://www.zhihu.com/node/TopicsPlazzaListV2"
    #     topics_id = response.meta.get("topics_id","")
    #     if topics_id is not None and offset != 0:
    #         post_data = {
    #             "topic_id": topics_id,
    #             "offset": offset,
    #             "hash_id": "825da520ff82d2d8d40497c8d87925c8"  # 用户 id
    #         }
    #         yield FormRequest(url=post_url,
    #                           ormdata=post_data,
    #                           callback=self.second_topic_api
    #                           )

    def parse_second(self,response):
        #提取一级分类话题下所有二级话题的前20url
        urls = response.xpath('//div[@class="zm-topic-cat-sub"]/div/div/div[@class="blk"]/a/@href').extract()
        if len(urls)>0:
            for url in urls:
                url = parse.urljoin(response.url, url)
                yield Request(url=url,callback=self.get_topic_key)


    def get_topic_key(self,response):
        #获取二级分类话题的key构造请求json数据
        topic_key = re.compile("\d+").findall(response.url)
        if len(topic_key) >0:
            topic_question_api = self.topic_question_api.format(topic_key[0],10)
            return [Request(url=topic_question_api,callback=self.get_question_id)]


    def get_question_id(self,response):
        #获取api中question的id构造question_url的request
        response_json = json.loads(response.text)
        for data in response_json["data"]:
            if "question" in data["target"]:
                #过滤掉非问答形式的文章
                question_id = data["target"]["question"]["id"]
                question_url = "https://www.zhihu.com/question/"+str(question_id)
                yield Request(url=question_url,callback=self.parse_question)

        if response_json["paging"]["is_end"] == False:
            next_topic_question_api = response_json["paging"]["next"]
            if next_topic_question_api is not None:
                yield Request(url = next_topic_question_api,callback=self.get_question_id)


    def parse_question(self,response):
        #QUESTION解析数据，将数据传递给下一层，并且构造访问question_api
        question_id = re.compile('\d+').findall(response.url)
        question_url = response.url
        content = response.xpath('//div/span[@class="RichText"]/text()').extract()
        question_topics = response.xpath('//span[@class="Tag-content"]/a/div/div/text()').extract()
        comments_num = response.xpath('//div[@class="QuestionHeader-Comment"]/button/text()').extract()
        followers_num = response.xpath('//button[@class="Button NumberBoard-item Button--plain"]/div/strong/text()').extract()
        watch_user_num = response.xpath('//div[@class="QuestionFollowStatus"]/div/div/div/strong/text()').extract()
        answer_num = response.xpath('//h4[@class="List-headerText"]/span/text()').extract()
        if len(question_id)>0:
            question_id =question_id[0]
            question_api = self.question_api.format(question_id, 20, 0)
            yield Request(url = question_api,
                          callback = self.parse_ans_and_que,
                          meta = {
                                "question_url":question_url,
                                "content":content,
                                "question_topics":question_topics,
                                "comments_num":comments_num,
                                "followers_num":followers_num,
                                "watch_user_num":watch_user_num,
                                "answer_num":answer_num
                                }
                          )


    def parse_ans_and_que(self,response):
        #解析answer和question的数据，并构造个人页面的url实行访问
        response_json = json.loads(response.text)
        if response_json["paging"]["is_start"] == True:
            #仅获取api中首页的第一个数据信息中的queston数据
            question_item = ZhihuQuestionItem()
            data = response_json["data"][0]
            question_item['question_id'] = data["question"]["id"]
            question_item['question_url'] = response.meta.get("question_url", "")
            question_item['question'] = data["question"]["title"]
            question_item['content'] = response.meta.get("content","")
            question_item['comments_num'] = response.meta.get("comments_num","")
            question_item['followers_num'] = response.meta.get("followers_num", "")
            question_item['watch_user_num'] = response.meta.get("watch_user_num", "")
            question_item['question_topics'] = response.meta.get("question_topics","")
            question_item['question_created_time'] = data["question"]["created"]
            question_item['question_updated_time'] = data["question"]["updated_time"]
            question_item['answer_num'] = response.meta.get("answer_num","")
            yield question_item


        #获取user_key，构造user_url,并且解析answer的数据
        for answer_data in response_json["data"]:
            # user_url.request
            answer_item = ZhihuAnswerItem()
            author_id =answer_data["author"]["url_token"]
            if author_id is not None:
                author_url = "https://www.zhihu.com/people/" + author_id +"/answers"
                yield Request(url=author_url, callback=self.parse_user,meta={"author_id":author_id})
            else:
                continue

            answer_item['question'] = answer_data["question"]["title"]
            answer_item['question_id'] = answer_data["question"]["id"]
            answer_item['answer_id'] =answer_data["id"]
            answer_item['answer_url'] = answer_data["url"]
            answer_item['content'] = answer_data["content"]
            answer_item['author_url_token'] = author_id
            answer_item['vote_num'] = answer_data["voteup_count"]
            answer_item['comments_num'] = answer_data["comment_count"]
            answer_item['answer_created_time'] = answer_data["created_time"]
            answer_item['answer_updated_time'] = answer_data["updated_time"]
            yield answer_item

        if response_json["paging"]["is_end"] == False:
            #判断此api是否有下一页，若有则request
            next_url = response_json["paging"]["next"]
            if next_url is not None:
              yield Request(url=next_url,callback=self.parse_ans_and_que)


    def parse_user(self,response):
        #user数据的解析
        item_loader = ItemLoader(item=ZhihuUserItem(), response=response)
        vote_pat = '<div class="IconGraf".*?</div>.*?获得.*?>([0-9,]+)<.*?次赞同.*?</div>'
        thanks_pat = '次赞同.*?<div.*?获得(.*?)次感谢'
        collection_pat = '次感谢.*?>([0-9,]+).*?次收藏'
        get_vote_num = re.compile(vote_pat,re.DOTALL).findall(response.text)
        get_thanks = re.compile(thanks_pat, re.DOTALL).findall(response.text)
        get_collection = re.compile(collection_pat, re.DOTALL).findall(response.text)
        answer_num = response.xpath('//li[@aria-controls="Profile-answers"]/a/span/text()').extract_first()
        inf_pat = '<div class="ProfileHeader-iconWrapper".*?</div>.*?>(.*?)<.*?(</div>|<div>)'
        code_pat = '<div class="ProfileHeader-iconWrapper".*?<svg.*?<path d="(.*?)".*?>'
        inf= re.compile(inf_pat,re.DOTALL).findall(response.text)
        code = re.compile(code_pat,re.DOTALL).findall(response.text)
        if inf and code is not None:
            inf_code = list(zip([i[0] for i in inf],code))
            for i in inf_code:
                if i[1] == MAN_CODE:
                    sex = "男"
                    item_loader.add_value('sex', sex)
                elif i[1] == WOMAN_CODE:
                    sex = "女"
                    item_loader.add_value('sex', sex)
                elif i[1] == JOB_CODE:
                    career = i[0]
                    item_loader.add_value('career', career)
                elif i[1] ==EDUCATION:
                    edu = i[0]
                    item_loader.add_value('educational_experience', edu)

        item_loader.add_value('user_url',response.url)
        item_loader.add_value('url_id',get_md5(response.url))
        item_loader.add_xpath('name','//h1[@class="ProfileHeader-title"]/span[1]/text()')
        item_loader.add_xpath('introduce_yourself','//h1[@class="ProfileHeader-title"]/span[2]/text()')
        item_loader.add_value('get_vote_num',get_vote_num)
        item_loader.add_value('get_thanks',get_thanks)
        item_loader.add_value('get_collection',get_collection)
        item_loader.add_xpath('followers','//div[@class="Card FollowshipCard"]/div/a[2]/div/strong/text()')
        item_loader.add_xpath('following','//div[@class="Card FollowshipCard"]/div/a[1]/div/strong/text()')
        item_loader.add_value('answer_num',answer_num)
        item_loader.add_xpath('questions_num','//li[@aria-controls="Profile-asks"]/a/span/text()')
        item_loader.add_xpath('articles_num','//li[@aria-controls="Profile-posts"]/a/span/text()')
        item_loader.add_xpath('columns_num','//li[@aria-controls="Profile-columns"]/a/span/text()')
        item_loader.add_xpath('ideal_num', '//li[@aria-controls="Profile-pins"]/a/span/text()')

        author_item = item_loader.load_item()
        yield author_item

        author_id = response.meta.get("author_id","")
        if author_id is not None and answer_num is not None and answer_num !='0':
            user_answer_url = self.user_answer_api.format(author_id,0,20)
            yield Request(url=user_answer_url,callback=self.recursion_question)

    def recursion_question(self,response):
        response_json = json.loads(response.text)
        if response_json["paging"]["is_end"] ==False:
            next_url = response_json["paging"]["next"]
            if next_url is not None:
                yield Request(url=next_url,callback=self.recursion_question)

        for data in response_json["data"]:
            question_id = data["question"]["id"]
            question_url = "https://www.zhihu.com/question/"+str(question_id)
            yield Request(url=question_url,callback=self.parse_question)
























