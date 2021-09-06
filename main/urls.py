from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views
from .views import RegistrationView, LoginView, MainPage

urlpatterns = [
    path('', MainPage.as_view(template_name='main/catalog.html'), name='catalog'),
    path('game-id<int:game_id>/', views.page_game, name='game_page'),  # slug from igdb will be better
    path('catalog', views.search, name='catalog_search'),
    path('test', views.test),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('register/', RegistrationView.as_view(), name='register')
]

