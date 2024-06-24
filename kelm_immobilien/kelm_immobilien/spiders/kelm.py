import scrapy
from scrapy.loader import ItemLoader
from kelm_immobilien.items import KelmImmobilienItem

class KelmSpider(scrapy.Spider):
    name = 'kelm'
    allowed_domains = ['kelm-immobilien.de']
    start_urls = ['https://kelm-immobilien.de/immobilien']

    def parse(self, response):
        for property in response.css('div.property'):
            loader = ItemLoader(item=KelmImmobilienItem(), selector=property)
            loader.add_css('url', 'h3.property-title a::attr(href)')
            loader.add_css('title', 'h3.property-title ::text')
            loader.add_css('status', 'div.row.data-verfuegbar_ab div.dd.col-xs-7::text')
            
            # For fields not provided in the question
            loader.add_css('pictures', 'div.property-images img::attr(src)')
            loader.add_css('rent_price', 'div.property-rent span.price::text')
            loader.add_css('description', 'div.property-description ::text')
            loader.add_css('phone_number', 'div.contact-phone span.value::text')
            loader.add_css('email', 'div.contact-email a::attr(href)')

            yield loader.load_item()
        
        # Follow pagination links
        next_page = response.css('a.next::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)