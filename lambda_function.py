# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals

import re
import json
import boto3
import logging
import pystache
import unicodedata
from elasticsearch import Elasticsearch

import settings

logger = logging.getLogger()
logger.setLevel(settings.LOG_LEVEL)


class Event(dict):
    def __getattr__(self, name):
        if name in self:
            return self[name]
        return None

    def __setattr__(self, name, value):
        self[name] = value

    def __delattr__(self, name):
        if name in self:
            del(self[name])

    @property
    def normalized_query(self):
        def _normalize(query):
            return unicodedata.normalize('NFKC', query)

        def _normalize_whitespace(query):
            return re.sub(r'\s{2,}', '\u0020', query)

        query = self['query']
        if query is None:
            return ''

        query = _normalize(query)
        query = _normalize_whitespace(query)
        return query.lower()

    @property
    def include_prefix(self):
        num = len(self.normalized_query.split(' '))
        if num == 1:
            return ""

        return "{} ".format(
            " ".join(self.normalized_query.split(' ')[:num-1])
        )

    @property
    def exclude_pattern(self):
        pattern = self['exclude_pattern']
        if pattern is None:
            return ''
        return pattern

    @property
    def max_size(self):
        size = self['size']
        if size is None or size > settings.MAX_SUGGEST_SIZE:
            return settings.DEFAULT_SUGGEST_SIZE
        return self['size']

    @property
    def body(self):
        context = {
            'query': self.query,
            'exclude_pattern': self.exclude_pattern,
            'include_prefix': self.include_prefix,
            'max_size': self.max_size
        }
        return pystache.render(settings.QUERY_TEMPLATE, context)


def lambda_handler(event, context):
    event = Event(event)
    client = Elasticsearch(event.host)

    try:
        response = client.search(
            index=event.index, doc_type=event.doc_type, body=event.body)
    except Exception as e:
        logger.error(e)
        return {'items': []}

    logger.debug(response)
    items = {'items': response['aggregations']['keywords']['buckets']}
    logger.debug(json.dumps(items, ensure_ascii=False, indent=2))
    return items
