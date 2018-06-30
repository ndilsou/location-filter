# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os
from scrapy.exceptions import DropItem
from scrapy.exporters import JsonLinesItemExporter


class AnnotationFilterPipeline(object):
    def process_item(self, item, spider):
        return item


class DuplicatesPipeline:
    types = ["articles", "annotations", "locations"]

    def __init__(self):
        self.ids_seen = {t: set() for t in self.types}

    def process_item(self, item, spider):
        if item['iid'] in self.ids_seen[item['type']]:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.ids_seen[item['type']].add(item['iid'])
            return item


class JsonLineItemDispatcherPipeline:
    save_types = ["articles", "annotations", "locations"]

    def __init__(self, output_dir):
        self.output_dir = output_dir
        self.files = {}
        self.exporters = {}

    def open_spider(self, spider):
        for save_type in self.save_types:
            self.files[save_type] = open(os.path.join(self.output_dir, f"{save_type}.jl"), "w+b")
            self.exporters[save_type] = JsonLinesItemExporter(self.files[save_type])

    def close_spider(self, spider):
        for save_type in self.save_types:
            self.exporters[save_type].finish_exporting()
            self.files[save_type].close()

    def process_item(self, item, spider):
        item_type = item.get("type")
        if item_type in self.save_types:
            self.exporters[item_type].export_item(item)

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        output_dir = settings.get("output-dir", ".")
        return cls(output_dir)
