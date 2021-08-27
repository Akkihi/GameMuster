from django.shortcuts import render
from django.http import HttpResponse
from main.utils.igdbapi import IgdbApi


def catalog(request):
    game_list = IgdbApi().get_games()
    return render(request, 'main/catalog.html', {'games': game_list})


def page_game(request, game_id):
    game_info = IgdbApi().get_game_by_id(game_id)
    return render(request, 'main/game_page.html', {'game_info': game_info})