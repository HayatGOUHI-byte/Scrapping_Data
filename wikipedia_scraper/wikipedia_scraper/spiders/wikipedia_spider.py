import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class WikipediaCrawlSpider(CrawlSpider):
    name = "wikipedia_crawler"
    allowed_domains = ["fr.wikipedia.org"]
    start_urls = ["https://fr.wikipedia.org/wiki/Beni_Affet"]

    # Définir les règles pour suivre les liens
    rules = (
        Rule(LinkExtractor(allow=r'/wiki/'), callback='parse_page', follow=True),
    )

    def parse_page(self, response):
        title = response.xpath('//h1[@class="firstHeading"]/text()').get()
        paragraphs = response.xpath('//div[@class="mw-parser-output"]/p/text()').getall()

        yield {
            'url': response.url,
            'title': title,
            'paragraphs': paragraphs
        }





class ShampooingsSpider(scrapy.Spider):
    name = 'shampooings'
    start_urls = ['https://parachezvous.ma/product-category/cheveux-hygiene-intime/shampooings-cheveux/']

    def parse(self, response):
        # Extraire les produits
        for product in response.css('li.product'):
            yield {
                'name': product.css('h2.woocommerce-loop-product__title::text').get(),
                'price': product.css('span.woocommerce-Price-amount::text').get(),
                'url': product.css('a::attr(href)').get(),
                'image': product.css('img::attr(src)').get()
            }

        # Suivre les liens vers les pages suivantes (pagination)
        next_page = response.css('a.next::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse)
