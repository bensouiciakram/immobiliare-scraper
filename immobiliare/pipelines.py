
from itemadapter import ItemAdapter
import os, os.path
from scrapy.pipelines.images import ImagesPipeline
from datetime import datetime
import pathlib
import shutil
from scrapy.exporters import JsonLinesItemExporter
from scrapy import signals

class ImmobiliarePipeline:
    
    def process_item(self, item, spider):
        item['path'] = spider.asset_image_path
        return item



class DynamicImagesPipeline(ImagesPipeline):
    

    def item_completed(self, results, item, info):
        for result in [x for ok, x in results if ok]:
            image_path = pathlib.Path( __file__ ).parents[1].joinpath('images')
            img_path =  image_path.joinpath(result['path'])
            property_path = item['path'].joinpath(str(item['listing'][0]['id']))
            property_path.mkdir(exist_ok=True)
            target_path = property_path.joinpath(img_path.name)    
            shutil.copy(img_path,target_path)
            if self.IMAGES_RESULT_FIELD in item.fields:
                result['path'] = target_path
                item[self.IMAGES_RESULT_FIELD].append(result)

        return item




class MultiCSVItemPipeline(object):

    @classmethod
    def from_crawler(cls,crawler):
        feed_path = crawler.settings.get('FEED_PATH')
        crawler.signals.connect(cls(feed_path).process_item,signal=signals.item_scraped)
        return cls(feed_path)

    def __init__(self,feed_path):
        self.feed_path = feed_path

    def process_item(self,item,spider):
        filename = str(item['listing'][0]['id']) + '.jl'
        with open(filename,'wb') as file :
            exporter = JsonLinesItemExporter(file,fields_to_export=['listing','trovokasa'])
            exporter.start_exporting()
            exporter.export_item(item)
            exporter.finish_exporting()
            pathlib.Path(__file__).parents[1].joinpath(filename).rename(self.feed_path.joinpath(filename))
        return item
