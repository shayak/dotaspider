# -*- coding: utf-8 -*-

# Scrapy settings for dotaspider project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'dotaspider'

SPIDER_MODULES = ['dotaspider.spiders']
NEWSPIDER_MODULE = 'dotaspider.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'dotaspider (+http://www.yourdomain.com)'
ITEM_PIPELINES = {
    'dotaspider.pipelines.TeamConstraintPipeline':300
}
MAIL_FROM = 'dotaspider007@gmail.com'
MAIL_TO = 'shayak007@gmail.com'
MAIL_SUBJECT = 'Dota Bet Matched'
MAIL_HOST = 'smtp.gmail.com'
MAIL_PORT = '587'
MAIL_USER = 'dotaspider007@gmail.com'
MAIL_PASS = 'dotapass'

