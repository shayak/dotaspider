# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DotaspiderItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    link = scrapy.Field()

class DotaSpiderResult(scrapy.Item):
    handicap = scrapy.Field()
    handicap_team = scrapy.Field()
    team1 = scrapy.Field()
    team2 = scrapy.Field()
    odds1 = scrapy.Field()
    odds2 = scrapy.Field()
    link = scrapy.Field()
    bestof = scrapy.Field()
