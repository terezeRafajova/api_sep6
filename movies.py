import os
import requests

def get_movie_details(movie_id):
    api_key = '75add5038773025e1132ea7f985ec4b5'
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}'
    response = requests.get(url)

    if response.status_code == 200:
        movie_data = response.json()
        id = movie_data['id']
        language = movie_data['original_language']
        title = movie_data['title']
        poster_raw = movie_data['poster_path']
        image = f'https://image.tmdb.org/t/p/original/{poster_raw}'
        overview = movie_data['overview']
        release_date = movie_data['release_date']
        voting_avg = movie_data['vote_average']
        vote_count = movie_data['vote_count']
        #genres
        genres = []
        genresData = movie_data.get('genres', [])
        for genreRaw in genresData:
            genres.append(genreRaw['name'])
        #cast
        actors = []
        directors = []
        writers = []
        url1 = f'https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key={api_key}'
        responseCrew = requests.get(url1)
        if responseCrew.status_code == 200:
            dataCrew = responseCrew.json()
            resultsCrew = dataCrew.get('cast', [])
            for crewMember in resultsCrew:
                print(crewMember)
                if crewMember['known_for_department'] == 'Acting':
                    idActor = crewMember['id']
                    nameActor = crewMember['name']
                    character = crewMember['character']
                    actor = {'id': idActor, 'name': nameActor, 'character': character}
                    actors.append(actor)
                if crewMember['known_for_department'] == 'Directing':
                    idDirector = crewMember['id']
                    nameDirector = crewMember['name']
                    director = {'id': idDirector, 'name': nameDirector}
                    directors.append(director)
                if crewMember['known_for_department'] == 'Writing':
                    idWritor = crewMember['id']
                    nameWritor = crewMember['name']
                    writer = {'id': idWritor, 'name': nameWritor}
                    writers.append(writer)
        #make movie back
        movie = {'id': id, 'title': title, 'language': language, 'release_date': release_date,
        'image': image, 'overview': overview, 'voting_avg': voting_avg, 'vote_count': vote_count,
        'genres': genres,'actors': actors, 'directors': directors, 'writers': writers}
        return movie 
    else:
        return None

def get_movies():
    api_key = '75add5038773025e1132ea7f985ec4b5'
    url = f'https://api.themoviedb.org/3/movie/popular?api_key={api_key}'

    movies = []
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        results = data.get('results', [])
        if not results:
                movies
        for movie_data in results:
            #only take data we want 
            id = movie_data['id']
            language = movie_data['original_language']
            title = movie_data['title']
            poster_raw = movie_data['poster_path']
            image = f'https://image.tmdb.org/t/p/original/{poster_raw}'
            overview = movie_data['overview']
            release_date = movie_data['release_date']
            voting_avg = movie_data['vote_average']
            vote_count = movie_data['vote_count']
            movie = {'id': id, 'title': title, 'language': language, 'release_date': release_date,
            'image': image, 'overview': overview, 'voting_avg': voting_avg, 'vote_count': vote_count}
            movies.append(movie)
        return movies 
    else:
        return None