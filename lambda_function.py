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

logger = logging.getLogger(__name__)
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

        query = self.get('query', '')
        query = _normalize(query)
        query = _normalize_whitespace(query)
        return query.lower()

    @property
    def cleaned_query(self):
        return self.get('query', '')

    @property
    def cleaned_include_prefix(self):
        num = len(self.normalized_query.split(' '))
        if num == 1:
            return ""

        return "{} ".format(
            " ".join(self.normalized_query.split(' ')[:num-1])
        )

    @property
    def cleaned_exclude_pattern(self):
        return self.get('exclude_pattern', '')

    @property
    def cleaned_size(self):
        size = self.get('size', settings.DEFAULT_SUGGEST_SIZE)
        if size > settings.MAX_SUGGEST_SIZE:
            return settings.DEFAULT_SUGGEST_SIZE
        return size

    @property
    def body(self):
        context = {
            'query': self.cleaned_query,
            'exclude_pattern': self.cleaned_exclude_pattern,
            'include_prefix': self.cleaned_include_prefix,
            'size': self.cleaned_size
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
