from django.urls import path
from . import views

urlpatterns = [
    path('', views.catalog, name='catalog'),
    path('game-id<int:game_id>/', views.page_game, name='game_page'),  # slug from igdb will be better
    path('catalog', views.search, name='catalog_search'),
    path('test', views.test)
]

