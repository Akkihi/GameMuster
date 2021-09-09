from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views
from .views import RegistrationView, LoginView, MainPage, MyMust, UserProfile, Search, GamePage

urlpatterns = [
    path('', MainPage.as_view(template_name='main/catalog.html'), name='catalog'),
    path('my_must', MyMust.as_view(template_name='main/must.html'), name='must'),
    path('profile', UserProfile.as_view(template_name='main/profile.html'), name='profile'),
    path('game-id<int:game_id>/', GamePage.as_view(template_name='main/game_page.html'), name='game_page'),
    path('catalog', Search.as_view(template_name='main/search.html'), name='catalog_search'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('register/', RegistrationView.as_view(), name='register')
]

