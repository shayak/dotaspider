# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from dotaspider.emailSender import sendMail
from dotaspider.spiders import data
from scrapy.exceptions import DropItem

class ConstraintPipeline(object):
    
    def process_item(self, item, spider):
        if item['team1'] in data.teams and item['odds1'] > data.return_threshold or \
        item['team2'] in data.teams and item['odds2'] > data.return_threshold:
            sendMail(item)
            return item
        
        raise DropItem("Match {0} vs {1} failed contraint", item['team1'], item['team2'])
