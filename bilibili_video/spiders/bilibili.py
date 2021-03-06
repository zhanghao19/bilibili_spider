# -*- coding: utf-8 -*-
import json
import re
from datetime import datetime
import scrapy
from scrapy.spiders import CrawlSpider
from bilibili_video.items import BilibiliSpiderItem


class BilibiliSpider(CrawlSpider):
    name = 'bilibili'
    allowed_domains = ['bilibili.com']

    # 索引页的ajax
    request_url = 'https://bangumi.bilibili.com/media/web_api/search/result?page={}&season_type=1&pagesize=20'
    page = 1
    start_urls = [request_url.format(page)]

    # 番剧信息的ajax请求
    season_url = 'https://bangumi.bilibili.com/ext/web_api/season_count?season_id={}&season_type=1&ts={}'

    # 番剧详情页的ajax请求
    media_url = 'https://www.bilibili.com/bangumi/media/md{}'

    def parse(self, response):
        # if self.page == 2:  # 限制爬取页数，用于测试爬取状态
        #     return
        list_data = json.loads(response.text).get('result').get('data')
        if list_data is None:  # 如果响应中没有数据，则结束执行
            return

        for data in list_data:
            ts = datetime.timestamp(datetime.now())
            yield scrapy.Request(url=self.season_url.format(data.get('season_id'), ts),
                                 callback=self.parse_details,
                                 meta=data)
        self.page += 1  # 生成下一页的请求
        yield scrapy.Request(url=self.request_url.format(self.page),
                             callback=self.parse)

    def parse_details(self, response):
        item = BilibiliSpiderItem()

        meta_data = response.meta
        item['season_id'] = meta_data.get('season_id')
        item['media_id'] = meta_data.get('media_id')
        item['title'] = meta_data.get('title')
        item['index_show'] = meta_data.get('index_show')
        item['is_finish'] = meta_data.get('is_finish')
        item['video_link'] = meta_data.get('link')
        item['cover'] = meta_data.get('cover')
        item['pub_real_time'] = meta_data.get('order').get('pub_real_time')
        item['renewal_time'] = meta_data.get('order').get('renewal_time')

        resp_data = json.loads(response.text).get('result')
        item['favorites'] = resp_data.get('favorites')
        item['coins'] = resp_data.get('coins')
        item['views'] = resp_data.get('views')
        item['danmakus'] = resp_data.get('danmakus')
        yield scrapy.Request(url=self.media_url.format(item['media_id']),
                             callback=self.parse_media,
                             meta=item)

    def parse_media(self, response):
        item = response.meta

        resp = response.xpath('//div[@class="media-info-r"]')
        item['media_tags'] = resp.xpath('//span[@class="media-tags"]/span/text()').extract()
        item['score'] = resp.xpath('//div[@class="media-info-score-content"]/text()').extract()[0]
        item['cm_count'] = resp.xpath('//div[@class="media-info-review-times"]/text()').extract()[0]
        yield item
