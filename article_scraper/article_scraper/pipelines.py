# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os
from collections import Counter
from scrapy.exceptions import DropItem
import logging

from article_scraper.exporters import JsonLinesGzipItemExporter
from scrapy.exporters import JsonLinesItemExporter

logger = logging.getLogger('pipeline')


class CounterPipeline:
    types = ["articles", "annotations", "locations"]

    def __init__(self, stats):
        self.stats = stats
        self.ids_seen = {t: set() for t in self.types}

    def tally(self):
        return {k: len(v) for k, v in self.ids_seen.items()}

    def process_item(self, item, spider):
        logger.info(f"COUNTER: {{  {self.tally()} }}")
        self.ids_seen[item['type']].add(item['iid'])
        self.stats.inc_value(f"count.{item['type']}")
        return item

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.stats)


class SpiderClosePipeline:
    types = ["articles", "annotations", "locations"]

    def __init__(self, crawler, limited_type="articles", limit=5):
        self.crawler = crawler
        self.limited_type = limited_type
        self.limit = limit
        self.counter = Counter()

    def process_item(self, item, spider):
        if item is not None:
            self.counter[item["type"]] += 1

        logger.debug(self.counter)

        if self.limited_type and self.counter[self.limited_type] > self.limit:
            self.crawler.engine.close_spider(spider, "download_limit_reached")

        return item

    @classmethod
    def from_crawler(cls, crawler):
        limited_type = crawler.settings.get("LIMITED_TYPE")
        limit = int(crawler.settings.get("LIMIT", 0))

        return cls(crawler, limited_type, limit)


class JsonLinesGzipItemDispatcherPipeline:
    save_types = ["articles", "annotations", "locations"]

    def __init__(self, output_dir, stats):
        self.stats = stats
        self.output_dir = output_dir
        self.files = {}
        self.exporters = {}

    def open_spider(self, spider):
        for save_type in self.save_types:
            self.files[save_type] = open(os.path.join(self.output_dir, f"{save_type}.jl.gz"), "ab")
            self.exporters[save_type] = JsonLinesGzipItemExporter(self.files[save_type])

    def close_spider(self, spider):
        for save_type in self.save_types:
            self.files[save_type].close()

    def process_item(self, item, spider):
        item_type = item.get("type")
        if item_type in self.save_types:
            self.exporters[item_type].export_item(item)

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        output_dir = settings.get("OUTPUT_DIR", ".")
        return cls(output_dir, crawler.stats)
