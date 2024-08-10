import scrapy
from urllib.parse import urljoin

from ..items import JumiaItem


class JumiaSpiderSpider(scrapy.Spider):
    name = "jumia-spider"
    allowed_domains = ["jumia.co.ke"]
    start_urls = ["https://www.jumia.co.ke/groceries/"]
    base_url = 'https://www.jumia.co.ke'

    def parse(self, response):
        products = response.css('section.card.-fh div.-paxs article')

        for prod in products:
            rel_url = prod.css('a.core::attr(href)').get()
            url = urljoin(self.base_url, rel_url)

            yield response.follow(url, callback=self.parse_item)

        next_page_button = response.xpath('//a[@aria-label="Next Page"]')
        if next_page_button:
            next_rel_url = next_page_button.attrib['href']
            next_full_url = urljoin(self.base_url, next_rel_url)

            yield response.follow(next_full_url, callback=self.parse)

    def parse_item(self, response):
        item = JumiaItem()
        card_sec = response.css('div.row.card')

        name = card_sec.css('h1::text').get()
        brand = card_sec.css('div.-phs div.-pvxs a::text').extract_first()
        price = card_sec.css('span.-b::text').get()
        img_urls = card_sec.css('a.itm::attr(href)').extract()

        product_detail = response.css('div.card.aim div.markup').getall()[0]
        key_features = response.xpath('//h2[text()="Key Features"]/following-sibling::div').css('li::text').extract()

        sku = response.xpath('//span[text()="SKU"]/../text()').get()  # ': SO771FF1JVQTINAFAMZ'
        gtin = response.xpath('//span[text()="GTIN Barcode"]/../text()').get()  # ': 6161102170092'
        main_material = response.xpath('//span[text()="Main Material"]/../text()').get()  # ': -'
        weight = response.xpath('//span[text()="Weight (kg)"]/../text()').get()  # ': 10'
        prod_country = response.xpath('//span[text()="Production Country"]/../text()').get()

        item['name'] = name
        item['brand'] = brand
        item['price'] = price
        item['img_urls'] = img_urls
        item['product_detail'] = product_detail
        item['key_features'] = key_features
        item['sku'] = sku
        item['gtin'] = gtin
        item['material'] = main_material
        item['weight'] = weight
        item['country'] = prod_country

        yield item
