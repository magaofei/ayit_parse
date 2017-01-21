from django.db import models
# from mongoengine import connect
from mongoengine import connect
from mongoengine import StringField
from mongoengine import Document
connect('ayit_news', host='127.0.0.1', port=27017)
# Create your models here.
from django.db import models

# table_news_import = ayit_news['news_import']   #表
# table_news_trends = ayit_news['news_trends']   #表
# table_news_affiche = ayit_news['news_affiche']   #表
# table_news_science = ayit_news['news_science']   #表


class AfficheNewsList(Document):
    title = StringField()
    time = StringField()
    url = StringField()
    tag = StringField()

    meta = {
        'collection': 'news_affiche'
    }


class ImportNewsList(Document):
    title = StringField()
    time = StringField()
    url = StringField()
    tag = StringField()

    meta = {
        'collection': 'news_import'
    }


class TrendsNewsList(Document):
    title = StringField()
    time = StringField()
    url = StringField()
    tag = StringField()

    meta = {
        'collection': 'news_trends'
    }


class ScienceNewsList(Document):
    title = StringField()
    time = StringField()
    url = StringField()
    tag = StringField()

    meta = {
        'collection': 'news_science'
    }


# for i in AfficheNewsList.objects[:200]:   #[:2] 相当于mongo中的limit功能
#     print(i.title, i.url, i.time, i.tag)






