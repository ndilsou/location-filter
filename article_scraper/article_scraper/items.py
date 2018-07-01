# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field


def fill_field(field, from_, to_):
    to_[field] = from_.get(field)


class ArticleItem(Item):
    iid = Field()
    lastModifiedTime = Field()
    publisher = Field()
    published_time = Field()
    annotation_uri = Field()
    id = Field()
    articleid = Field()
    url = Field()
    previous_id = Field()
    type = Field()
    title = Field()
    cleantitle = Field()
    description = Field()
    body = Field()

    @classmethod
    def from_dict(cls, data):
        item = cls()
        fill_field('iid', data, item)
        fill_field('lastModifiedTime', data, item)
        fill_field('publisher', data, item)
        fill_field('published_time', data, item)
        fill_field('annotation_uri', data, item)
        fill_field('id', data, item)
        fill_field('url', data["item"], item)
        fill_field('articleid', data, item)
        fill_field('previous_id', data, item)
        fill_field('type', data, item)
        fill_field('title', data["item"], item)
        fill_field('cleantitle', data["item"], item)
        fill_field('description', data["item"], item)
        fill_field('body', data["item"], item)
        return item

    def __repr__(self):
        return f"Article{{ publication: {self['publisher']}, title: {self['title']} }}"


class AnnotationItem(Item):
    iid = Field()
    label = Field()
    origin_types = Field()
    uri = Field()
    lastModifiedTime = Field()
    publishedTime = Field()
    alternateLabels = Field()
    id = Field()
    type = Field()
    title = Field()
    lod = Field()
    abstract = Field()
    categories = Field()

    @classmethod
    def from_dict(cls, data):
        item = cls()
        fill_field('iid', data, item)
        fill_field('id', data, item)
        fill_field('label', data, item)
        fill_field('origin_types', data, item)
        fill_field('uri', data, item)
        fill_field('lastModifiedTime', data, item)
        fill_field('publishedTime', data, item)
        fill_field('alternateLabels', data, item)
        fill_field('type', data, item)
        fill_field('title', data, item)
        fill_field('lod', data["item"], item)
        fill_field('abstract', data["item"], item)
        fill_field('categories', data["item"], item)
        return item

    def __repr__(self):
        return f"Annotation{{ title: {self['title']} }}"


class LocationItem(Item):
    iid = Field()
    council_annotation_uri = Field()
    county = Field()
    local_government_area = Field()
    nuts_region = Field()
    lng = Field()
    lat = Field()
    country = Field()
    name = Field()
    lastModifiedTime = Field()
    origin_type = Field()
    annotation_uri = Field()
    id = Field()
    type = Field()
    postcode_sector = Field()

    @classmethod
    def from_dict(cls, data):
        item = cls()
        fill_field('iid', data, item)
        fill_field('council_annotation_uri', data, item)
        fill_field('county', data, item)
        fill_field('local_government_area', data, item)
        fill_field('nuts_region', data, item)
        fill_field('lng', data, item)
        fill_field('lat', data, item)
        fill_field('country', data, item)
        fill_field('name', data, item)
        fill_field('lastModifiedTime', data, item)
        fill_field('origin_type', data, item)
        fill_field('annotation_uri', data, item)
        fill_field('id', data, item)
        fill_field('type', data, item)
        fill_field('postcode_sector', data, item)
        return item

    def __repr__(self):
        return f"Location{{ title: {self['name']}, loc:[{self['lng']},{self['lat']}]}}"
