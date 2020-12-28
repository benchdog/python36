# -*- coding: utf-8 -*-
from elasticsearch6 import Elasticsearch

es = Elasticsearch(['127.0.0.1:9200','127.0.0.1:9201'])
film_body = {'film_name':'终极大审判','film_attr':'[大陆] [剧情] [战争]','film_desc':'这是一部不可多得点精彩高分电影杰作'}
res = es.index(index='films', doc_type='basic_info', id=2,body=film_body)
print(res['result'])
