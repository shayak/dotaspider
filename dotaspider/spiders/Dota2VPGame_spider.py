import scrapy
import json
from models import StartupData
from models import Xpaths
from dotaspider.utility import helper
from dotaspider.data import data
from dotaspider.items import DotaspiderItem, DotaSpiderResult

class Dota2VPGameSpider(scrapy.Spider):
    name=StartupData.name
    baseurl = StartupData.baseurl
    allowed_domains = StartupData.allowed_domains
    start_urls = StartupData.start_urls
    
    bets_list_xpath = Xpaths.bets_list

    def parse(self, response):
        pages_xpath = Xpaths.pager
        resp = response.xpath(pages_xpath)
        if len(resp)==0:
            yield scrapy.Request(self.start_urls[0], callback=self.parsepage)
        else:
            for sel in response.xpath(pages_xpath):
                path = sel.extract()[0]
                yield scrapy.Request(self.baseurl+path, callback=self.parsepage)

    def parsepage(self, response):
        items = []
        for sel in response.xpath(self.bets_list_xpath):
            item = DotaspiderItem()
            item['title'] = sel.xpath('@title').extract()
            item['link'] = sel.xpath('@href').extract()
            dic = zip(item['title'], item['link'])
            lst = [i for i in dic if not helper.nameMatch(data.gametags, i[0])]
            
            for tup in lst:
                yield scrapy.Request(self.baseurl+tup[1], callback=self.parsebetpage)
    
    def parsebetpage(self, response):
        handicap_link_xpath = Xpaths.handicap_link
        for sel in response.xpath(handicap_link_xpath):
            handicap_link = self.baseurl+sel.extract()
            yield scrapy.Request(handicap_link, callback=lambda r, l=handicap_link:self.parsebet(r, l))

    def parsebet(self, response, link):
        schedule_xpath = Xpaths.schedule
        handicap_xpath = Xpaths.handicap
        bestof_xpath = Xpaths.bestof

        if len(response.xpath(schedule_xpath+"/span[text()='Cleared']")) > 0:
            return
       
        starttime = helper.getStartTime(response.xpath(schedule_xpath+"/span[@class='mr-5']/text()").extract()[0])
        odds_xpath = Xpaths.odds
        teams_xpath = Xpaths.teams

        odds = map(lambda x: float(x.strip()), response.xpath(odds_xpath).extract())
        teams = response.xpath(teams_xpath).extract()
        
        h = response.xpath(handicap_xpath + '/text()').extract()[0]
        hteam = h[h.find("[")+1:h.find("-")].strip()
        hamount = float(h[h.find("-")+1:h.find("]")].strip())

        bestof = response.xpath(bestof_xpath).extract()[0]
        
        dic = DotaSpiderResult()
        dic['handicap_team'] = hteam
        dic['handicap'] = hamount
        dic['team1'] = teams[0]
        dic['odds1'] = odds[0]
        dic['team2'] = teams[1]
        dic['odds2'] = odds[1]
        dic['link'] = link
        dic['bestof'] = bestof
        dic['start'] = starttime
        
        yield dic

