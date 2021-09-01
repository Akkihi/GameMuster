from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponseNotFound, Http404
from main.utils.igdbapi import IgdbApi
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from .models import GameData


def catalog(request):
    game_data = GameData.objects.all().order_by('-id')
    try:
        p = Paginator(game_data, 6)
        page_num = request.GET.get('p', 1)
        page_obj = p.page(page_num)
    except InvalidPage or EmptyPage:
        raise Http404()
    return render(request, 'main/catalog.html', {'games': page_obj})


def search(request):
    search_query = request.GET.get('sq', '')
    if search_query:
        game_data = GameData.objects.filter(data__name__icontains=search_query)
    else:
        game_data = GameData.objects.all().order_by('-id')
    try:
        p = Paginator(game_data, 6)
        page_num = request.GET.get('p', 1)
        page_obj = p.page(page_num)
    except InvalidPage or EmptyPage:
        raise Http404()
    return render(request, 'main/search.html', {'games': page_obj, 'search_query': search_query})


def page_game(request, game_id):
    game_data = GameData.objects.filter(data__id=game_id)
    game_info = game_data.get().data
    return render(request, 'main/game_page.html', {'info': game_info})


'''
def search(request):
    search_query = request.GET.get('search', '')

    if search_query:
        game_data = GameData.objects.filter(data=search_query)
    else:
        game_data = GameData.objects.all().order_by('-id')

    p = Paginator(game_data, 6)
    page_num = request.GET.get('page', 1)
    page_obj = p.page(page_num)
    return render(request, 'main/catalog.html', {'games': page_obj})'''


def test(request):
    stuff_data = GameData.objects.all()
    p = Paginator(stuff_data, 10)
    page = p.page(2)
    context = {'items': page }
    return render(request, 'main/test.html', context)

