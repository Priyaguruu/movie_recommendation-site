from flask import Flask, render_template, request
import requests
from algorithm import recommend_movies


app = Flask(__name__)

TMDB_API_KEY = 'b5bc108ab746f2c4b84dcdbcafd238'  
TMDB_API_URL = 'https://api.themoviedb.org/3'

# Function to search movie and get its ID
def get_movie_id(movie_name, language='en-US'):
    search_url =f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY }&query={movie_name}&language=en-US"

    params = {
        'api_key': TMDB_API_KEY,
        'query': movie_name,
        'language': language
    }
    response = requests.get(search_url, params=params)
    
    # Check for valid response
    if response.status_code != 200:
        print("TMDB API error:", response.json())  # for debugging
        return None, None

    data = response.json()
    results = data.get('results', [])

    if results:
        return results[0]['id'], results[0].get('title', 'Unknown Title')
    return None, None


# Function to get recommendations by movie ID
def get_recommendations(movie_id, language='en-US'):
    rec_url = f"{TMDB_API_URL}/movie/{movie_id}/recommendations"
    params = {
        'api_key': TMDB_API_KEY,
        'language': language
    }
    response = requests.get(rec_url, params=params)

    if response.status_code != 200:
        print("Error fetching recommendations:", response.json())
        return ["Error fetching recommendations."]
    
    data = response.json()
    results = data.get('results', [])

    recommendations = []
    for movie in results[:5]:  # <- fixed this line
        title = movie.get('title') or movie.get('name') or 'Unknown Title'
        recommendations.append(title)
    return recommendations


@app.route('/')
def home():
    return render_template('form.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    title = request.form['title'].strip()
    language = request.form['language']
    
    print("Movie title received:", title)
    print("Language received:", language)

    recommendations = recommend_movies(title, language)
    return render_template('result.html', title=title, recommendations=recommendations)


if __name__ == '__main__':
    app.run(debug=True)
