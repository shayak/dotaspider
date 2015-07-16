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
            lst = [i for i in dic if helper.nameMatch(data.gametags, i[0])]
            
            for tup in lst:
                yield scrapy.Request(self.baseurl+tup[1], callback=self.parsebetpage)
    
    def parsebetpage(self, response):
        for sel in response.xpath(self.handicap_xpath):
            handicap_link = self.baseurl+sel.xpath('@href').extract()[0]
            yield scrapy.Request(handicap_link, callback=lambda r, l=handicap_link:self.parsebet(r, l))

    def parsebet(self, response, link):
        data_xpath = "//div[@class='spinach-corps-data']"
        lst = response.xpath(data_xpath+"/p/text()").extract()
        clean_lst = map(lambda x: x.strip(), lst)
        dic = DotaSpiderResult()
        dic['team1'] = clean_lst[0]
        dic['odds1'] = clean_lst[1]
        dic['team2'] = clean_lst[2]
        dic['odds2'] = clean_lst[3]
        dic['link'] = link
        
        yield dic

