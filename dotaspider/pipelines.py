# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from dotaspider.emailSender import sendMail
from dotaspider.spiders.data import teams
from scrapy.exceptions import DropItem

class TeamConstraintPipeline(object):
    
    def process_item(self, item, spider):
        if item['team1'] in teams or item['team2'] in teams:
            sendMail(item)
            return item
        else:
            raise DropItem("Match {0} vs {1} failed teams contraint", item['team1'], item['team2'])
