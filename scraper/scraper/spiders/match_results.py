from scrapy.selector import HtmlXPathSelector
from scrapy.spider import BaseSpider
from scrapy.http import Request
from scraper.items import MatchResult

class MatchResultsSpider(BaseSpider):
    name            = 'match_results'
    allowed_domains = ['eredivisielive.nl']
    start_urls      = ['http://eredivisielive.nl/eredivisie/programma/']

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        selector = '//*[@id="select-playround"]/option/@value'
        for path in hxs.select(selector).extract():
            url = 'http://eredivisielive.nl' + path
            yield Request(url, callback = self.parse_results)

    def parse_results(self, response):
        hxs = HtmlXPathSelector(response)
        li_selector     = '//li[@class="past"]'
        teams_selector  = './/*[@class="match-info"]/text()[position()=2]'
        scores_selector = './/*[@class="score"]/text()'
        for li in hxs.select(li_selector):
            teams= li.select(teams_selector)[0].extract().strip("\n\r\t ")
            scores = li.select(scores_selector)[0].extract().strip("\n\r\t ")
            a_name, _, b_name = teams.partition(' - ')
            a_score, _, b_score = scores.partition(' - ')
            yield MatchResult(
                a_name  = a_name.strip(),
                b_name  = b_name.strip(),
                a_score = int(a_score.strip()),
                b_score = int(b_score.strip())
            )
