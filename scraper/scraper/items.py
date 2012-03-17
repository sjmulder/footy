# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class MatchResult(Item):
    a_name  = Field()
    b_name  = Field()
    a_score = Field()
    b_score = Field()
