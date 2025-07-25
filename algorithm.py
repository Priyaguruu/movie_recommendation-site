import requests


API_KEY = 'eab5bc108ab746f2c4b84dcdbcafd238'  
TMDB_BASE_URL = 'https://api.themoviedb.org/3'

def get_movie_id(movie_name, language='en-US'):

    url = f"{TMDB_BASE_URL}/search/movie"
    params = {'api_key': API_KEY, 'query': movie_name, 'language':language}
    response = requests.get(url, params=params)
    results = response.json().get('results', [])
    if results:
        return results[0]['id']
    return None

def get_recommendations(movie_id, language='en-US'):
    url = f"{TMDB_BASE_URL}/movie/{movie_id}/recommendations"
    params = {'api_key': API_KEY, 'language': language}
    response = requests.get(url, params=params)
    results = response.json().get('results', [])
    return [movie['title'] for movie in results[:5]] if results else []

def recommend_movies(title, language='en-US'):
    movie_id= get_movie_id(title, language='en-US')
    if movie_id is None:
        return [f"No movie found for '{title}'"]
    
    recommendations = get_recommendations(movie_id, language='en-US')
    return recommendations

# 🔁 Example usage:
if __name__ == "__main__":
    movie_title = "all the bright places"  # You can test with any movie
    language = "en-US"        
    recommendations = recommend_movies(movie_title, language)
    print("Recommendations:", recommendations)
