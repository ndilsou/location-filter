import scrapy
import json
from annotation_filter.items import ArticleItem


class ArticleSpider(scrapy.Spider):
    name = "articles"
    article_url = "https://itemstore-cache-prod.inyourarea.co.uk/items/articles"
    annotation_url = "https://itemstore-cache-prod.inyourarea.co.uk/items/annotations"
    location_url = "https://itemstore-cache-prod.inyourarea.co.uk/items/locations"
    start_urls = [article_url]

    def parse(self, response):
        json_response = json.loads(response.text)
        for json_article in json_response:
            article = ArticleItem.from_dict(json_article)
            self.log(article)
            for annotation_uri in article["annotation_uri"]:
                yield response.follow(f"{self.annotation_url}?uri={annotation_uri}", self.parse_annotations)
                yield response.follow(f"{self.location_url}?annotation_uri={annotation_uri}", self.parse_locations)

    def parse_annotations(self, response):
        json_response = json.loads(response.text)
        self.log(f"Annotation{{ {json_response} }}")

    def parse_locations(self, response):
        json_response = json.loads(response.text)
        self.log(f"Location{{ {json_response} }}")
