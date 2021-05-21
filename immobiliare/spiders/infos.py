import scrapy
from scrapy import Request 
from scrapy.loader import ItemLoader
from immobiliare.items import ImmobiliareItem
import chompjs 
from nested_lookup import nested_lookup,nested_delete
from scrapy.shell import inspect_response
from datetime import datetime
import os 
from scrapy import signals 
import pathlib
import shutil

class InfosSpider(scrapy.Spider):
    name = 'infos'
    allowed_domains = ['immobiliare.it']
    start_urls = ['http://immobiliare.it/vendita-case/san-benedetto-del-tronto/']



    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(InfosSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.create_asset_folder, signal=signals.spider_opened)
        crawler.signals.connect(spider.clean_up,signal=signals.spider_closed)
        spider.asset_root = crawler.settings.get('ASSET_ROOT')
        spider.asset_data_path = crawler.settings.get('FEED_PATH')
        return spider

    def create_asset_folder(self):
        date = datetime.now()
        date_string = '{}-{}-{}'.format(date.year,date.month,date.day)
        self.asset_path = self.asset_root.joinpath(date_string)
        self.asset_path.mkdir(exist_ok=True)
        self.asset_image_path = self.asset_path.joinpath('images')
        self.asset_image_path.mkdir(exist_ok=True)
        self.asset_data_path.mkdir(exist_ok=True)

    def clean_up(self):
        shutil.rmtree(pathlib.Path(__file__).parents[2].joinpath('images'))
        pathlib.Path(__file__).parents[2].joinpath('infos.jl').rename(self.asset_path.joinpath('infos.jl'))
    
    def parse(self, response):

        # generating properties requests 
        properties_urls = response.xpath('//p[@class="titolo text-primary"]/a/@href').getall()
        
        for url in properties_urls[:3]:
            yield Request(
                url,
                callback=self.parse_infos
            )

        #send the next page request if it exists 
        # next = response.xpath('//a[contains(@title,"Pagina successiva")]/@href').get()
        # if next :
        #    yield Request(
        #        next,
        #    )


    def parse_infos(self,response):
        data_string = data = response.xpath('//script[@id="js-hydration"]/text()').get()
        data = chompjs.parse_js_object(data_string,json_params={'strict':False})
        loader = ItemLoader(ImmobiliareItem(),response)
        # inspect_response(response, self)
        loader.add_value('image_urls',nested_lookup('medium',data))
        data = nested_delete(data,'multimedia')
        listing = nested_delete(nested_lookup('listing',data)[0],'type')
        listing = nested_delete(listing,'title')
        loader.add_value('listing',listing)
        loader.add_value('trovokasa',nested_lookup('trovakasa',data))
        yield loader.load_item()



    
