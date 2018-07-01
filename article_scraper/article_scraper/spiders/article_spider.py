import scrapy
import json
from article_scraper.items import ArticleItem, AnnotationItem, LocationItem
from scrapy.exceptions import CloseSpider


class ArticleSpider(scrapy.Spider):
    close_down = False
    name = "articles"
    article_url = "https://itemstore-cache-prod.inyourarea.co.uk/items/articles"
    annotation_url = "https://itemstore-cache-prod.inyourarea.co.uk/items/annotations"
    location_url = "https://itemstore-cache-prod.inyourarea.co.uk/items/locations"
    types = ["articles", "annotations", "locations"]

    def __init__(self, *args, **kwargs):
        super(ArticleSpider, self).__init__(*args, **kwargs)
        self.start_urls = [self.article_url, self.article_url + "?before=1530327500000"]
        self.ids_seen = {t: set() for t in self.types}

    def parse(self, response):
        json_response = json.loads(response.text)
        if json_response:
            for json_article in json_response:
                article = ArticleItem.from_dict(json_article)
                self.log(article)
                if article["iid"] not in self.ids_seen["articles"]:
                    self.ids_seen["articles"].add(article["iid"])
                    self.crawler.stats.inc_value("count.articles")
                    yield article

                for annotation_uri in article["annotation_uri"]:
                    yield response.follow(f"{self.annotation_url}?uri={annotation_uri}", self.parse_annotations)
                    yield response.follow(f"{self.location_url}?annotation_uri={annotation_uri}", self.parse_locations)

            last_modified_time = article.get("lastModifiedTime")
            yield response.follow(f"{self.article_url}?before={last_modified_time}", self.parse)

    def parse_annotations(self, response):
        json_response = json.loads(response.text)
        for json_annotation in json_response:
            annotation = AnnotationItem.from_dict(json_annotation)
            self.log(annotation)

            if annotation["iid"] not in self.ids_seen["annotations"]:
                self.ids_seen["annotations"].add(annotation["iid"])
                self.crawler.stats.inc_value("count.annotations")
                yield annotation

    def parse_locations(self, response):
        json_response = json.loads(response.text)
        for json_location in json_response:
            location = LocationItem.from_dict(json_location)
            self.log(location)

            if location["iid"] not in self.ids_seen["locations"]:
                self.ids_seen["locations"].add(location["iid"])
                self.crawler.stats.inc_value("count.locations")
                yield location

