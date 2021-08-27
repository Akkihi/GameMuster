import requests
import json

client_id = 'naqphvp3h2zlw73zteu5v57y7n43lc'
client_secret = 'hsyhd8a3vjgzjqozbrxwpjc5gyyhdc'
grant_type= 'client_credentials'


def get_token():
    r = requests.post(
        f"https://id.twitch.tv/oauth2/token?client_id={client_id}&client_secret={client_secret}&grant_type={grant_type}")
    access_token = json.loads(r.content)['access_token']
    return access_token