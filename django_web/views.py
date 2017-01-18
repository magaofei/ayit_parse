from django.shortcuts import render
from django_web.models import NewsList
# Create your views here.
from django.core.paginator import Paginator
from django.http import JsonResponse


def json_info(request):
    limit = 4
    print(limit)
    news_info = NewsList.objects[:4]

    pagintor_news_info = Paginator(news_info, limit)
    page = request.GET.get('page', 1)

    load_news_info = pagintor_news_info.page(page)

    context = {
        'news_info': load_news_info
    }
    response = JsonResponse({
        'title': context['news_info'][0].title,
        'time': context['news_info'][0].time,
        'url': context['news_info'][0].url,
        'tag': context['news_info'][0].tag
    })

    return response



