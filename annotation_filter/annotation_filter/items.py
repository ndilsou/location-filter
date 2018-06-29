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
    pass


class LocationItem(Item):
    pass
