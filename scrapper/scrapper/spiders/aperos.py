from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapper.items import PlaceItem

class AperosSpider(CrawlSpider):
    name = "aperos"
    allowed_domains = ["lesamisdelapero.fr"]
    start_urls = [
        "http://www.lesamisdelapero.fr/paris/classement-bars",
    ]
    rules = (
        Rule(SgmlLinkExtractor(allow=('/paris/bars', )), callback='parse_bar'),
    )
    

    def parse_bar(self, response):
      self.log("Got a bar on %s" % response.url)
      hxs = HtmlXPathSelector(response)
      item = PlaceItem()
      item['name'] = hxs.select('//h1/span/text()').extract()[0]
      item['address'] = hxs.select("//span[@property='v:street-address']/a/text()").extract()[0]

      return item