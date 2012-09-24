# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html

from palces.models import Place
 
class PlacePipeline(object):

  def process_item(self, item, spider):
    item.save()
    return item
