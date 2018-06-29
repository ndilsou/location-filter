import scrapy
import json
from annotation_filter.items import ArticleItem, AnnotationItem, LocationItem

DEBUG_LIMIT = 5


class ArticleSpider(scrapy.Spider):
    name = "articles"
    article_url = "https://itemstore-cache-prod.inyourarea.co.uk/items/articles"
    annotation_url = "https://itemstore-cache-prod.inyourarea.co.uk/items/annotations"
    location_url = "https://itemstore-cache-prod.inyourarea.co.uk/items/locations"
    start_urls = [article_url]

    def parse(self, response):
        json_response = json.loads(response.text)
        DEBUG_I = 0
        for json_article in json_response:
            article = ArticleItem.from_dict(json_article)
            self.log(article)
            for annotation_uri in article["annotation_uri"]:
                yield response.follow(f"{self.annotation_url}?uri={annotation_uri}", self.parse_annotations)
                yield response.follow(f"{self.location_url}?annotation_uri={annotation_uri}", self.parse_locations)

            DEBUG_I += 1
            if DEBUG_I >= DEBUG_LIMIT:
                break

    def parse_annotations(self, response):
        json_response = json.loads(response.text)
        for json_annotation in json_response:
            annotation = AnnotationItem.from_dict(json_annotation)
            self.log(annotation)

    def parse_locations(self, response):
        json_response = json.loads(response.text)
        json_response = json.loads(response.text)
        for json_location in json_response:
            location = LocationItem.from_dict(json_location)
            self.log(location)
