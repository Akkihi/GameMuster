from celery import shared_task
from main.utils import igdbapi
from main.models import GameData


@shared_task
def update_db():
    print('Celery update db')
    results = igdbapi.IgdbApi().get_games()
    for result in results:
        try:
            GameData.objects.create(id=result['id'], data=result)
        except:
            print('no added')
            pass