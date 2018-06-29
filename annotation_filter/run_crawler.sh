#!/usr/bin/env bash
pipenv run scrapy crawl articles -s JOBDIR=crawls/articles -o articles.json
