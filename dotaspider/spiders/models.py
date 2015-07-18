class StartupData:
    name = "dota2vpgame"
    baseurl = "http://dota2.vpgame.com"
    allowed_domains = ["dota2.vpgame.com"]
    start_urls = [baseurl + "/guess.html"]

class SelectorXPaths:
    #guess.html
    pager = "//div[@class='pager']//li[@starts-with(@class, 'page')]/a/@href"

    #match listings page
    bets_list = "//div[@class='items']/a"

    #individual match base page
    handicap = "//ul[@class='spinach-tap clearfix']//li/a[text()='Handicap']/@href"

    #individual bet page
    schedule = "//div[@class='spinach-corps']//div[@class='spinach-item-tt']/p[@class='pull-right']"
    odds = "//div[@class='spinach-corps-data']//span[@class='vp-item-odds']/text()"
    teams = "//div[@class='spinach-corps-data']//p[@class='spinach-corps-name ellipsis']/@title"
    handicap_amt = "//div[@class='spinach-corps']//a[contains(@title,'handicap')]/span[@class='f-warning']"
    bestof = "//div[@class='spinach-corps']//div[@class='spinach-corps-vs']//span[@class='f-14']/text()"
