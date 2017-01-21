from django.shortcuts import render
from django_web.models import AfficheNewsList
from django_web.models import ImportNewsList
from django_web.models import ScienceNewsList
from django_web.models import TrendsNewsList
# Create your views here.
from django.core.paginator import Paginator
from django.http import JsonResponse

limit = 20
def affiche_json_info(request):

    news_info = AfficheNewsList.objects[:limit]


    pagintor_news_info = Paginator(news_info, limit)
    page = request.GET.get('page', 1)

    load_news_info = pagintor_news_info.page(page)

    context = {
        'news_affiche': load_news_info
    }
    arr = []
    for i in range(0, limit, 1):
        json_info = {
            'title': context['news_affiche'][i].title,
            'time': context['news_affiche'][i].time,
            'url': context['news_affiche'][i].url,
            'tag': context['news_affiche'][i].tag
        }
        arr.append(json_info)
    response = JsonResponse(dict(news_affiche=list(arr)))
    return response



def trends_json_info(request):

    news_info = TrendsNewsList.objects[:limit]

    pagintor_news_info = Paginator(news_info, limit)
    page = request.GET.get('page', 1)

    load_news_info = pagintor_news_info.page(page)

    context = {
        'news_trends': load_news_info
    }

    arr = []
    for i in range(0, limit, 1):
        json_info = {
        'title': context['news_trends'][0].title,
        'time': context['news_trends'][0].time,
        'url': context['news_trends'][0].url,
        'tag': context['news_trends'][0].tag
        }
        arr.append(json_info)
    response = JsonResponse(dict(news_trends=list(arr)))
    return response

def import_json_info(request):

    news_info = ImportNewsList.objects[:limit]

    pagintor_news_info = Paginator(news_info, limit)
    page = request.GET.get('page', 1)

    load_news_info = pagintor_news_info.page(page)

    context = {
        'news_import': load_news_info
    }
    arr = []
    for i in range(0, limit, 1):
        json_info = {
            'title': context['news_import'][0].title,
            'time': context['news_import'][0].time,
            'url': context['news_import'][0].url,
            'tag': context['news_import'][0].tag
        }
        arr.append(json_info)
    response = JsonResponse(dict(news_import=list(arr)))
    return response

def science_json_info(request):

    news_info = ScienceNewsList.objects[:limit]

    pagintor_news_info = Paginator(news_info, limit)
    page = request.GET.get('page', 1)

    load_news_info = pagintor_news_info.page(page)

    context = {
        'news_science': load_news_info
    }
    arr = []
    for i in range(0, limit, 1):
        json_info = {
            'title': context['news_science'][0].title,
            'time': context['news_science'][0].time,
            'url': context['news_science'][0].url,
            'tag': context['news_science'][0].tag
        }
        arr.append(json_info)
    response = JsonResponse(dict(news_science=list(arr)))
    return response



