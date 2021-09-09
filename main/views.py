from django.shortcuts import render
from django import views
from django.http import  Http404, HttpResponseRedirect
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

from main.utils.igdbapi import IgdbApi
from .models import GameData, UserMust
from .forms import LoginForm, RegistrationForm


class MainPage(views.View):
    template_name = 'catalog.html'

    def get(self, request, *args, **kwargs):

        username = None
        game_data = GameData.objects.all().order_by('-id')
        must_games_list = list()
        if request.user.is_authenticated:
            username = request.user.username
            try:
                must_games = UserMust.objects.get(username=username).must_game.get_queryset()
                for must in must_games:
                    must_games_list.append(must.data['id'])
            except:
                pass
        try:
            p = Paginator(game_data, 6)
            page_num = request.GET.get('p', 1)
            page_obj = p.page(page_num)
        except InvalidPage or EmptyPage:
            raise Http404()
        return render(request, 'main/catalog.html', {'games': page_obj, 'musts': must_games_list})

    def post(self, request, *args, **kwargs):

        username = None
        game_data = GameData.objects.all().order_by('-id')
        must_games_list = list()
        game_id = None
        if request.user.is_authenticated:
            username = request.user.username
            if request.method == 'POST' and 'must' in request.POST:
                game_id = int(request.POST.get('must', ''))
                gd = GameData.objects.get(id=game_id)
                user = UserMust.objects.get(username=username)
                gd.usermust_set.add(user)
                print(gd)
            if request.method == 'POST' and 'unmust' in request.POST:
                game_id = int(request.POST.get('unmust', ''))
                gd = GameData.objects.get(id=game_id)
                user = UserMust.objects.get(username=username)
                gd.usermust_set.remove(user)
                print(gd)
            try:
                must_games = UserMust.objects.get(username=username).must_game.get_queryset()
                for must in must_games:
                    must_games_list.append(must.data['id'])
            except:
                pass
        try:
            p = Paginator(game_data, 6)
            page_num = request.GET.get('p', 1)
            page_obj = p.page(page_num)
        except InvalidPage or EmptyPage:
            raise Http404()

        return render(request, 'main/catalog.html', {'games': page_obj, 'musts': must_games_list})


class MyMust(views.View):
    template_name = 'must.html'

    def get(self, request, *args, **kwargs):

        username = None
        must_data = None
        must_games_list = list()
        if request.user.is_authenticated:
            username = request.user.username
            try:
                must_data = UserMust.objects.get(username=username).must_game.order_by('-id')
                for must in must_data:
                    must_games_list.append(must.data['id'])
            except:
                pass
        try:
            p = Paginator(must_data, 6)
            page_num = request.GET.get('p', 1)
            page_obj = p.page(page_num)
        except InvalidPage or EmptyPage:
            raise Http404()
        return render(request, 'main/must.html', {'games': page_obj, 'musts': must_games_list})

    def post(self, request, *args, **kwargs):

        must_data = None
        must_games_list = list()
        game_id = None
        if request.user.is_authenticated:
            username = request.user.username
            if request.method == 'POST' and 'must' in request.POST:
                game_id = int(request.POST.get('must', ''))
                gd = GameData.objects.get(id=game_id)
                user = UserMust.objects.get(username=username)
                gd.usermust_set.add(user)
                print(gd)
            if request.method == 'POST' and 'unmust' in request.POST:
                game_id = int(request.POST.get('unmust', ''))
                gd = GameData.objects.get(id=game_id)
                user = UserMust.objects.get(username=username)
                gd.usermust_set.remove(user)
                print(gd)
            try:
                must_data = UserMust.objects.get(username=username).must_game.order_by('-id')
                for must in must_data:
                    must_games_list.append(must.data['id'])
            except:
                pass
        try:
            p = Paginator(must_data, 6)
            page_num = request.GET.get('p', 1)
            page_obj = p.page(page_num)
        except InvalidPage or EmptyPage:
            raise Http404()
        return render(request, 'main/must.html', {'games': page_obj, 'musts': must_games_list})


class UserProfile(views.View):
    template_name = 'profile.html'

    def get(self, request, *args, **kwargs):
        user_data = None
        username = None
        if request.user.is_authenticated:
            username = request.user
            user_data = User.objects.filter(username=username)
            print()
        else:
            raise Http404("You're not loggined")

        return render(request, 'main/profile.html', {'games': user_data})


class LoginView(views.View):

    def get(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        context = {
            'form': form
        }

        return render(request, 'main/login.html', context)

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return HttpResponseRedirect('/')
        context ={
            'form': form
        }
        return render(request, 'main/catalog.html', context)


class RegistrationView(views.View):

    def get(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST or None)
        context = {
            'form': form
        }

        return render(request, 'main/registration.html', context)

    def post(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST or None)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.username = form.cleaned_data['username']
            new_user.email = form.cleaned_data['email']
            new_user.first_name = form.cleaned_data['first_name']
            new_user.last_name = form.cleaned_data['last_name']
            new_user.birthday = form.cleaned_data['birthday']
            new_user.save()
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            login(request, user)
            return HttpResponseRedirect('/')
        context = {
            'form': form
        }
        return render(request, 'main/registration.html', context)


def search(request):
    search_query = request.GET.get('sq', '')
    must_games_list = list()
    if search_query:
        game_data = GameData.objects.filter(data__name__icontains=search_query).order_by('-id')
    else:
        game_data = GameData.objects.get_queryset().order_by('-id')

    if request.user.is_authenticated:
        username = request.user.username
        try:
            must_games = UserMust.objects.get(username=username).must_game.get_queryset()
            for must in must_games:
                must_games_list.append(must.data['id'])
        except:
            pass
    try:
        p = Paginator(game_data, 6)
        page_num = request.GET.get('p', 1)
        page_obj = p.page(page_num)
    except InvalidPage or EmptyPage:
        raise Http404()
    return render(request, 'main/search.html', {'games': page_obj, 'search_query': search_query, 'musts': must_games_list})


def page_game(request, game_id):
    game_data = GameData.objects.filter(data__id=game_id)
    game_info = game_data.get().data
    return render(request, 'main/game_page.html', {'info': game_info})


def test(request):
    stuff_data = GameData.objects.all()
    p = Paginator(stuff_data, 10)
    page = p.page(2)
    context = {'items': page }
    return render(request, 'main/test.html', context)






