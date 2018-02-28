# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from zhihu.Tools.common import *


class ZhihuQuestionItem(scrapy.Item):
    question_id = scrapy.Field()
    question_url = scrapy.Field()
    question = scrapy.Field()
    content = scrapy.Field()
    comments_num = scrapy.Field()
    followers_num = scrapy.Field()
    watch_user_num = scrapy.Field()
    question_topics = scrapy.Field()
    question_created_time = scrapy.Field()
    question_updated_time = scrapy.Field()
    answer_num = scrapy.Field()
    crawl_time = scrapy.Field()
    crawl_update_time = scrapy.Field()


    def get_sql(self):
        sql_insert = '''insert into zhihu_question(question_id,question_url,question,content,comments_num,followers_num,watch_user_num,question_topics,question_updated_time,question_created_time,answer_num,crawl_time)
                        values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
        question_id = get_num(self.get("question_id",""))
        question_url = get_str(self.get("question_url",""))
        question = get_str(self.get("question",""))
        content = get_str(self.get("content",""))
        comments_num = get_num(self.get("comments_num",""))
        followers_num = get_num(self.get("followers_num",""))
        watch_user_num = get_num(self.get("watch_user_num",""))
        question_topics = get_str(self.get("question_topics,"))
        question_updated_time = get_datetime(self.get("question_updated_time",""))

        question_created_time = get_datetime(self.get("question_created_time",""))
        answer_num = get_num(self.get("answer_num",""))
        crawl_time = get_now()

        params = (question_id,question_url,question,content,
                  comments_num,followers_num,watch_user_num,
                  question_topics,question_updated_time,question_created_time,
                  answer_num,crawl_time)

        return sql_insert,params


class ZhihuAnswerItem(scrapy.Item):
    question = scrapy.Field()
    question_id = scrapy.Field()
    answer_id = scrapy.Field()
    answer_url = scrapy.Field()
    content = scrapy.Field()
    author_url_token = scrapy.Field()
    vote_num = scrapy.Field()
    comments_num = scrapy.Field()
    answer_created_time = scrapy.Field()
    answer_updated_time = scrapy.Field()
    crawl_time = scrapy.Field()
    crawl_update_time = scrapy.Field()


    def get_sql(self):
        sql_insert = '''insert into zhihu_answer(answer_id,answer_url,question_id,question,content,vote_num,comments_num,author_url_token,answer_created_time,answer_updated_time,crawl_time)
                                                      values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''

        answer_created_time = get_datetime(self.get("answer_created_time",""))
        answer_id = get_num(self.get("answer_id",""))
        answer_url = get_str(self.get("answer_url",""))
        author_url_token = get_str(self.get("author_url_token",""))
        comments_num = get_num(self.get("comments_num",""))
        content = get_str(self.get("content",""))
        question = get_str(self.get("question",""))
        question_id = get_num(self.get("question_id",""))
        vote_num = get_str(self.get("vote_num",""))
        answer_updated_time = get_datetime(self.get("answer_updated_time",""))
        crawl_time = get_now()

        params = (answer_id,answer_url,question_id,
                  question,content,vote_num,
                  comments_num,author_url_token,answer_created_time,
                  answer_updated_time,crawl_time)

        return sql_insert,params


class ZhihuUserItem(scrapy.Item):
    user_url = scrapy.Field()
    url_id = scrapy.Field()
    name = scrapy.Field()
    sex = scrapy.Field()
    introduce_yourself = scrapy.Field()
    career = scrapy.Field()
    educational_experience = scrapy.Field()
    get_vote_num = scrapy.Field()
    get_thanks = scrapy.Field()
    get_collection = scrapy.Field()
    followers = scrapy.Field()
    following = scrapy.Field()
    answer_num = scrapy.Field()
    questions_num = scrapy.Field()
    articles_num = scrapy.Field()
    columns_num = scrapy.Field()
    ideal_num = scrapy.Field()
    crawl_time = scrapy.Field()
    crawl_update_time = scrapy.Field()


    def get_sql(self):
        sql_insert = '''insert into zhihu_user(url_id,user_url,name,sex,career,educational_experience,introduce_yourself,get_vote_num,get_thanks,get_collection,followers,following,answer_num,questions_num,articles_num,columns_num,ideal_num,crawl_time)
                        values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''

        user_url = get_str(self.get("user_url",""))
        url_id = get_str(self.get("url_id",""))
        name = get_str(self.get("name",""))
        sex = get_str(self.get("sex",""))
        introduce_yourself = get_str(self.get("introduce_yourself",""))
        career = get_str(self.get("career",""))
        educational_experience = get_str(self.get("educational_experience",""))
        get_vote_num = get_num(self.get("get_vote_num",""))
        get_thanks = get_num(self.get("get_thanks",""))
        get_collection = get_num(self.get("get_collection",""))
        followers = get_num(self.get("followers",""))
        following = get_num(self.get("following",""))
        answer_num = get_num(self.get("answer_num",""))
        questions_num = get_num(self.get("questions_num",""))
        articles_num = get_num(self.get("articles_num",""))
        columns_num = get_num(self.get("columns_num",""))
        ideal_num = get_num(self.get("ideal_num",""))
        crawl_time = get_now()

        params = (url_id,user_url,name,
                  sex,career,educational_experience,
                  introduce_yourself,get_vote_num,get_thanks,
                  get_collection,followers,following,
                  answer_num,questions_num,articles_num,
                  columns_num,ideal_num,crawl_time)

        return sql_insert,params

























