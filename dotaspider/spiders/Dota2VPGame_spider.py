import scrapy
import json
import helper
import data
from dotaspider.items import DotaspiderItem, DotaSpiderResult

class Dota2VPGameSpider(scrapy.Spider):
    name="dota2vpgame"
    baseurl = "http://dota2.vpgame.com"
    allowed_domains = ["dota2.vpgame.com"]
    start_urls = [baseurl + "/guess.html"]
    bets_list_xpath = "//div[@class='items']/a"
    handicap_xpath = "//ul[@class='spinach-tap clearfix']//li/a[text()='Handicap']"

    def parse(self, response):
        pages_xpath = "//div[@class='pager']//li[starts-with(@class, 'page')]/a"
        for sel in response.xpath(pages_xpath):
            path = sel.xpath('@href').extract()[0]
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
        for sel in response.xpath(self.handicap_xpath):
            handicap_link = self.baseurl+sel.xpath('@href').extract()[0]
            yield scrapy.Request(handicap_link, callback=lambda r, l=handicap_link:self.parsebet(r, l))

    def parsebet(self, response, link):
        data_xpath = "//div[@class='spinach-corps-data']"
        handicap_xpath = "//div[@class='spinach-corps']//a[contains(@title,'handicap')]/span[@class='f-warning']"
        bestof_xpath = "//div[@class='spinach-corps']//div[@class='spinach-corps-vs']//span[@class='f-14']"
        
        odds_xpath = data_xpath + "//span[@class='vp-item-odds']/text()"
        teams_xpath = data_xpath + "//p[@class='spinach-corps-name ellipsis']/@title"

        odds = map(lambda x: float(x.strip()), response.xpath(odds_xpath).extract())
        teams = response.xpath(teams_xpath).extract()
        
        h = response.xpath(handicap_xpath + '/text()').extract()[0]
        hteam = h[h.find("[")+1:h.find("-")].strip()
        handicap = h[h.find("-")+1:h.find("]")].strip()

        bestof = response.xpath(bestof_xpath+"/text()").extract()[0]
        
        dic = DotaSpiderResult()
        dic['handicap_team'] = hteam
        dic['handicap'] = float(handicap)
        dic['team1'] = teams[0]
        dic['odds1'] = odds[0]
        dic['team2'] = teams[1]
        dic['odds2'] = odds[1]
        dic['link'] = link
        dic['bestof'] = bestof
        yield dic

