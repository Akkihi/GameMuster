import requests
import json
from gamewebsite.settings import CLIENT_ID, CLIENT_SECRET


class IgdbApi:
    MAIN_FIELDS = ['name', 'screenshots.url', 'aggregated_rating', 'platforms.abbreviation']  # todo platforms genres user rating default

    FIELDS = ['name', 'screenshots.url', 'summary', 'release_dates.date', 'rating', 'aggregated_rating',
              'genres.name', 'platforms.abbreviation', 'rating_count', 'tags', 'updated_at',
              'aggregated_rating_count']  # todo game by id
    SEARCH = ['character', 'company', 'description', 'game', 'name', 'platform']

    def __init__(self):
        api_url = "https://api.igdb.com/v4/"
        grant_type = 'client_credentials'
        r = requests.post(
            f"https://id.twitch.tv/oauth2/token?client_id={CLIENT_ID}&client_secret={CLIENT_SECRET}&grant_type={grant_type}")
        access_token = json.loads(r.content)['access_token']
        print(access_token)
        self.__api_url = api_url
        self.__query_header = {'Client-ID': CLIENT_ID,
                               'Authorization': ('Bearer %s' % access_token)}

    def get_games(self, limit=200):
        url = self.__api_url + "games/"
        data = f"fields {','.join(self.FIELDS)}; sort rating desc; limit {limit};"
        response = requests.post(url, headers=self.__query_header, data=data)
        if response.ok:
            games = json.loads(response.text)
            for game in games:
                if 'screenshots' in game.keys():
                    game['screenshot_url'] = game['screenshots'][0]['url'].replace('t_thumb', 't_screenshot_huge')
            return games
        else:
            return None

    def get_game_by_id(self, game_id):
        url = self.__api_url + "games/"
        data = f"fields {','.join(self.FIELDS)}; where id ={game_id};"
        response = requests.post(url, headers=self.__query_header, data=data)
        print(response.text)
        if response.ok:
            game_info = json.loads(response.text)
            return game_info
        else:
            return None
