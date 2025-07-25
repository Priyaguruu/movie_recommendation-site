import requests

api_key = 'eab5bc108ab746f2c4b84dcdbcafd238'
url = f'https://api.themoviedb.org/3/configuration/languages?api_key={api_key}'

response = requests.get(url)
languages = response.json()

for lang in languages:
    print(f"{lang['english_name']} ({lang['iso_639_1']})")
