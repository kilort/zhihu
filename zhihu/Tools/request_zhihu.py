import re, requests,json,time
from zhihu.Tools.return_proxy import produce_ip
from zhihu.Tools.common import *
from scrapy.selector import Selector
question_api = "http://www.zhihu.com/api/v4/questions/19670177/answers?sort_by=default&include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cupvoted_followees%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cbadge%5B%3F%28type%3Dbest_answerer%29%5D.topics&limit=20&offset=0"
    # def start_requests(self):
    #     url = "https://www.zhihu.com/signup?next=%2F"

MAN_CODE = 'M3.025 10.64c-1.367-1.366-1.367-3.582 0-4.95 1.367-1.366 3.583-1.366 4.95 0 1.367 1.368 1.367 3.584 0 4.95-1.367 1.368-3.583 1.368-4.95 0zm10.122-9.368c-.002-.414-.34-.75-.753-.753L8.322 0c-.413-.002-.746.33-.744.744.002.413.338.75.75.752l2.128.313c-.95.953-1.832 1.828-1.832 1.828-2.14-1.482-5.104-1.27-7.013.64-2.147 2.147-2.147 5.63 0 7.777 2.15 2.148 5.63 2.148 7.78 0 1.908-1.91 2.12-4.873.636-7.016l1.842-1.82.303 2.116c.003.414.34.75.753.753.413.002.746-.332.744-.745l-.52-4.073z'
WOMAN_CODE = 'M6 0C2.962 0 .5 2.462.5 5.5c0 2.69 1.932 4.93 4.485 5.407-.003.702.01 1.087.01 1.087H3C1.667 12 1.667 14 3 14s1.996-.006 1.996-.006v1c0 1.346 2.004 1.346 1.998 0-.006-1.346 0-1 0-1S7.658 14 8.997 14c1.34 0 1.34-2-.006-2.006H6.996s-.003-.548-.003-1.083C9.555 10.446 11.5 8.2 11.5 5.5 11.5 2.462 9.038 0 6 0zM2.25 5.55C2.25 3.48 3.93 1.8 6 1.8c2.07 0 3.75 1.68 3.75 3.75C9.75 7.62 8.07 9.3 6 9.3c-2.07 0-3.75-1.68-3.75-3.75z'
JOB_CODE = 'M15 3.998v-2C14.86.89 13.98 0 13 0H7C5.822 0 5.016.89 5 2v2l-3.02-.002c-1.098 0-1.97.89-1.97 2L0 16c0 1.11.882 2 1.98 2h16.033c1.1 0 1.98-.89 1.987-2V6c-.007-1.113-.884-2.002-1.982-2.002H15zM7 4V2.5s-.004-.5.5-.5h5c.5 0 .5.5.5.5V4H7z'
EDUCATION = 'M11 0L0 3.94v.588l4.153 2.73v5.166C4.158 12.758 7.028 16 11 16c3.972 0 6.808-3.116 6.85-3.576l.006-5.163 4.13-2.732.014-.586L11 0z'
url="https://www.zhihu.com/api/v4/topics/19550994/feeds/top_activity?include=data%5B%3F%28target.type%3Dtopic_sticky_module%29%5D.target.data%5B%3F%28target.type%3Danswer%29%5D.target.content%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%3Bdata%5B%3F%28target.type%3Dtopic_sticky_module%29%5D.target.data%5B%3F%28target.type%3Danswer%29%5D.target.is_normal%2Ccomment_count%2Cvoteup_count%2Ccontent%2Crelevant_info%2Cexcerpt.author.badge%5B%3F%28type%3Dbest_answerer%29%5D.topics%3Bdata%5B%3F%28target.type%3Dtopic_sticky_module%29%5D.target.data%5B%3F%28target.type%3Darticle%29%5D.target.content%2Cvoteup_count%2Ccomment_count%2Cvoting%2Cauthor.badge%5B%3F%28type%3Dbest_answerer%29%5D.topics%3Bdata%5B%3F%28target.type%3Dtopic_sticky_module%29%5D.target.data%5B%3F%28target.type%3Dpeople%29%5D.target.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F%28type%3Dbest_answerer%29%5D.topics%3Bdata%5B%3F%28target.type%3Danswer%29%5D.target.content%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%3Bdata%5B%3F%28target.type%3Danswer%29%5D.target.author.badge%5B%3F%28type%3Dbest_answerer%29%5D.topics%3Bdata%5B%3F%28target.type%3Darticle%29%5D.target.content%2Cauthor.badge%5B%3F%28type%3Dbest_answerer%29%5D.topics%3Bdata%5B%3F%28target.type%3Dquestion%29%5D.target.comment_count&limit=10"

headers = {"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/63.0.3239.84 Chrome/63.0.3239.84 Safari/537.36"}
cookies = {'z_c0': '"MS4xTUZpRkFnQUFBQUFYQUFBQVlRSlZUVkxrZ0Z1RjB6bEFoZl9Udk4yYVE4U2lMeHpSWDhZb29nPT0=|1519621714|0c95f8a4d1c2001f22eac3f93b0c363d848c39a6"', 'l_n_c': '1'}
#
# with open("/home/hl/桌面/ubuntu/MINE/zhihu/zhihu/Tools/ua.txt","r")as f:
#     ua = f.readlines()
#     f.close()
#
# for  i in ua:
#     i =i.strip()
#     headers ={"User-Agent":i}
# response = requests.get(url="https://www.zhihu.com/question/265793577",headers = headers)
# # print(response.text)
# response = Selector(text=response.text)
# # followers_num = response.xpath('//div[@class="List-item"]/div/h2/div/a/@href').extract()
# content = response.xpath('//div/span[@class="RichText"]/text()').extract()
# question_topics = response.xpath('//span[@class="Tag-content"]/a/div/div/text()').extract()
# comments_num = response.xpath('//div[@class="QuestionHeader-Comment"]/button/text()').extract()
# followers_num = response.xpath('//button[@class="Button NumberBoard-item Button--plain"]/div/div/text()').extract()
# watch_user_num = response.xpath('//div[@class="QuestionFollowStatus"]/div/div/div/strong/text()').extract()
# answer_num = response.xpath('//h4[@class="List-headerText"]/span/text()').extract()
# print(followers_num)

# content = selector.xpath('//div/span[@class="RichText"]/text()').extract()
# question_topics = selector.xpath('//span[@class="Tag-content"]/a/div/div/text()').extract()
# comments_num = selector.xpath('//div[@class="QuestionHeader-Comment"]/button/text()').extract()
# followers_num = selector.xpath('//button[@class="Button NumberBoard-item Button--plain"]/div/strong/text()').extract()
# watch_user_num = selector.xpath('//div[@class="QuestionFollowStatus"]/div/div/div/strong/text()').extract()
# answer_num = int(selector.xpath('//h4[@class="List-headerText"]/span/text()').extract_first(""))
# answer_num = re.compile('[\d]+]', re.DOTALL).findall(answer_num)
# print(content,question_topics,comments_num,followers_num,watch_user_num,answer_num)
# response_json = json.loads(response.text)
# print(response_json["data"])
# if "question" in response_json["data"][0]:
#     print(response_json["data"][0]["question"]["id"])


    #     print('\n')
        # if u[1] == MAN_CODE:
        #     sex = "nam"
        # elif u[1] == WOMAN_CODE:
        #     sex = "wonam"
        # elif u[1] == JOB_CODE:
        #     job = u[0]
        # elif u[1] ==EDUCATION:
        #     edu = u[0]
        # else:
        #     pass
        #
        # print(sex,job,edu)


    # print(len(get_vote_num))
    # for i in [MAN_CODE,WOMAN_CODE,JOB_CODE,EDUCATION]:
    #     if i in get_vote_num:
    #         num.append(get_vote_num.index(i))
    # print(sorted(num))





