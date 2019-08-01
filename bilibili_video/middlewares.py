# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import time

import random
import scrapy
import time

from bilibili_video.user_agents import agents
# from selenium import webdriver


class RandomUserAgentMiddleware(object):
    def process_request(self, request, spider):
        agent = random.choice(agents)
        request.headers["User-Agent"] = agent
        return None


# class ChromeDynamicMiddleware(object):
#     def process_request(self, request, spider):
#         url = '/anime/index'
#         if url in request.url:
#             opts = webdriver.ChromeOptions()
#             opts.add_argument('--headers')
#             driver = webdriver.Chrome(chrome_options=opts)
#             # driver = webdriver.Chrome()
#             driver.get(request.url)
#             time.sleep(1)
#             html_data = driver.page_source
#             driver.quit()
#             return scrapy.http.HtmlResponse(url=request.url, body=html_data, encoding="UTF-8", request=request)
#         else:
#             return None
