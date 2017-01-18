from django.db import models
# from mongoengine import connect
from mongoengine import *
connect('ayit_news', host='127.0.0.1', port=27017)
# Create your models here.
from django.db import models


class NewsList(Document):
    title = StringField()
    time = StringField()
    url = StringField()
    tag = StringField()

    meta = {
        'collection': 'news_list'
    }

# for i in NewsList.objects[:4]:   #[:2] 相当于mongo中的limit功能
#     print(i.title, i.url, i.time, i.tag)






