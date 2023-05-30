from flask import Flask,Blueprint, jsonify, request  #pip3 install flask  
from flask_cors import CORS
import psycopg2   #pip install psycopg2  
from datetime import datetime
import movies

app = Flask(__name__)
# Enable CORS for all routes
CORS(app)

conn = psycopg2.connect(
    host= '35.228.156.220',  
    database= 'postgres',
    user= 'postgres',
    password= 'database123'
)    

@app.route('/')
def home():       
    return("<h1>SEP 6 python API</h1>"+"</h3>write your request</h3>")
#---------------profiles----------------------
@app.route('/profiles', methods=['GET'])
def get_profiles():
    try:
        cur = conn.cursor()
        cur.execute("SELECT first_name, last_name, username, created_on, age, likedMovies, likedProfiles FROM profiles")
        profile_data = cur.fetchall()
        cur.close()

        dataToReturn = []
        for profileRaw in profile_data:
            profile = {
                'first_name': profileRaw[0],
                'last_name': profileRaw[1],
                'username': profileRaw[2],
                'created_on': profileRaw[3],
                'age': profileRaw[4],
                'likedMovies': profileRaw[5],
                'likedProfiles': profileRaw[6]
            }
            dataToReturn.append(profile)
        return jsonify(dataToReturn)
    except (psycopg2.Error, Exception) as error:
        # Handle the error
        print("An error occurred:", error)
        return jsonify({'error': "error"}), 400

@app.route('/profile/<string:username>', methods=['GET'])
def get_profile_by_username(username):
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM profiles WHERE username = %s", (username,))
        profile_data = cur.fetchall()
        cur.close()

        dataToReturn = []
        for profileRaw in profile_data:
            profile = {
                'first_name': profileRaw[0],
                'last_name': profileRaw[1],
                'username': profileRaw[2],
                'created_on': profileRaw[3],
                'age': profileRaw[4],
                'likedMovies': profileRaw[5],
                'likedProfiles': profileRaw[6]
            }
            dataToReturn.append(profile)
        return jsonify(dataToReturn)
    except (psycopg2.Error, Exception) as error:
        # Handle the error
        print("An error occurred:", error)
        return jsonify({'error': "error"}), 400

@app.route('/profile', methods=['POST'])
def create_profile():
    try:
        data = request.json
        age = data.get('age')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        username = data.get('username')

        if not age or not first_name or not last_name or not username:
            return jsonify({'error': 'Invalid request. Write required fields.'}), 400
    
        cur = conn.cursor()
        cur.execute("INSERT INTO profiles (first_name, last_name, username, age) VALUES (%s,%s,%s,%s)", (first_name, last_name, username, age))
        conn.commit()
        cur.close()
        return jsonify({'message': 'Profile created'}), 201
    
    except (psycopg2.Error, Exception) as error:
        # Handle the error
        print("An error occurred:", error)
        return jsonify({'error': "error"}), 400

@app.route('/profile/like', methods=['POST'])
def like_profile():
    try:
        data = request.json
        current_username = data.get('current_username')
        liked_username = data.get('liked_username')
        
        if not current_username or not liked_username:
            return jsonify({'error': 'Invalid request. Write required fields.'}), 400

        # Check if the user has already liked the profile
        cur = conn.cursor()
        cur.execute("SELECT * FROM profiles WHERE username = %s AND %s = any (likedProfiles)", (current_username, liked_username))
        existing_like = cur.fetchone()
        cur.close()

        if existing_like:
            return jsonify({'message': 'You have already liked this movie.'}), 200
        cur = conn.cursor()
        cur.execute("SELECT likedProfiles FROM profiles WHERE username = %s", (current_username,))
        profile_data = cur.fetchone()
        cur.close()
        if profile_data is not None:
            liked_profiles = profile_data[0] if profile_data[0] is not None else []
            liked_profiles.append(liked_username)
        else:
            liked_profiles = [liked_username]

        cur = conn.cursor()
        cur.execute("UPDATE profiles SET likedProfiles = %s WHERE username = %s", (liked_profiles, current_username))
        conn.commit()
        cur.close()
        return jsonify({'message': 'Profile liked'}), 201

    except (psycopg2.Error, Exception) as error:
        # Handle the error
        print("An error occurred:", error)
        return jsonify({'error': "error"}), 400

@app.route('/movies/<string:username>/liked', methods=['GET'])
def getLikedMovies(username):
    try:
        cur = conn.cursor()
        cur.execute("SELECT likedMovies FROM profiles WHERE username = %s", (username,))
        movie_ids_data = cur.fetchone()
        cur.close()
        
        moviesToReturn = []
        if movie_ids_data and movie_ids_data[0] is not None:
            for movie_id in movie_ids_data[0]:
                movie = movies.get_movie_no_details(movie_id)
                moviesToReturn.append(movie)
        return jsonify(moviesToReturn)
        
    except (psycopg2.Error, Exception) as error:
        # Handle the error
        print("An error occurred:", error)
        return jsonify({'error': "error"}), 400

@app.route('/movie/like', methods=['POST'])
def likeMovie():
    try:
        data = request.json
        likedMovie = data.get('likedMovie')
        username = data.get('username')
        
        if not likedMovie or not username:
            return jsonify({'error': 'Invalid request. Write required fields.'}), 400
    
        # Check if the user has already liked the movie
        cur = conn.cursor()
        cur.execute("SELECT * FROM profiles WHERE username = %s AND %s = any (likedMovies)", (username, likedMovie))
        existing_like = cur.fetchone()
        cur.close()

        if existing_like:
            return jsonify({'message': 'You have already liked this movie.'}), 200
        
        cur = conn.cursor()
        cur.execute("SELECT likedMovies FROM profiles WHERE username = %s", (username,))
        movie_data = cur.fetchone()
        cur.close()
        if movie_data is not None:
            liked_movies = movie_data[0] if movie_data[0] is not None else []
            liked_movies.append(likedMovie)
        else:
            liked_movies = [likedMovie]

        cur = conn.cursor()
        cur.execute("UPDATE profiles SET likedMovies = %s WHERE username = %s", (liked_movies, username))
        conn.commit()
        cur.close()
        return jsonify({'message': 'Movie liked'}), 201

    except (psycopg2.Error, Exception) as error:
        # Handle the error
        print("An error occurred:", error)
        return jsonify({'error': "error"}), 400    

@app.route('/profiles/<string:username>/liked', methods=['GET'])
def getLikedProfiles(username):
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM profiles WHERE username = ANY (SELECT unnest(likedProfiles) FROM profiles WHERE username = %s)", (username,))
        profile_data = cur.fetchall()
        cur.close()

        dataToReturn = []
        for profileRaw in profile_data:
            profile = {
                'first_name': profileRaw[0],
                'last_name': profileRaw[1],
                'username': profileRaw[2],
                'created_on': profileRaw[3],
                'age': profileRaw[4],
                'likedMovies': profileRaw[5],
                'likedProfiles': profileRaw[6]
            }
            dataToReturn.append(profile)
        return jsonify(dataToReturn)

    except (psycopg2.Error, Exception) as error:
        # Handle the error
        print("An error occurred:", error)
        return jsonify({'error': "error"}), 400

#--------------------reviews-------------------
@app.route('/review', methods=['POST'])
def create_review():
    try:
        data = request.json
        movie_id = data.get('movie_id')
        movie_title = movies.get_movie_no_details(movie_id)['title']
        username = data.get('username')
        description = movie_title +": " + data.get('description')
        rating = data.get('rating')

        #check if review already exists 
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM reviews WHERE movie_id = %s AND username = %s", (movie_id, username))
        review_count = cur.fetchone()[0]
        if review_count > 0:
            cur.close()
            return jsonify({'error': 'Review already exists'}), 409

        if not movie_id or not username or not description or not rating:
            return jsonify({'error': 'Invalid request. Write required fields.'}), 400
    
        cur = conn.cursor()
        cur.execute("INSERT INTO reviews (movie_id, username, description, rating) VALUES (%s,%s,%s,%s)", (movie_id, username, description, rating))
        conn.commit()
        cur.close()
        return jsonify({'message': 'Review created'}), 201

    except (psycopg2.Error, Exception) as error:
        # Handle the error
        print("An error occurred:", error)
        return jsonify({'error': "error"}), 400    

@app.route('/reviews/movie/<int:movie_id>', methods=['GET'])
def getReviewsForMovie(movie_id):
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM reviews WHERE movie_id = %s", (movie_id,))
        review_data = cur.fetchall()
        cur.close()

        dataToReturn = []
        for reviewRaw in review_data:
            review = {
                'movie_id': reviewRaw[0],
                'username': reviewRaw[1],
                'description': reviewRaw[2],
                'created_on': reviewRaw[3],
                'rating': reviewRaw[4]
            }
            dataToReturn.append(review)
        return jsonify(dataToReturn)

    except (psycopg2.Error, Exception) as error:
        # Handle the error
        print("An error occurred:", error)
        return jsonify({'error': "error"}), 400 

@app.route('/reviews/username/<string:username>', methods=['GET'])
def getReviewsOfFollowers(username):
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM reviews WHERE username = ANY (SELECT unnest(likedProfiles) FROM profiles WHERE username = %s)", (username,))
        review_data = cur.fetchall()
        cur.close()

        dataToReturn = []
        for reviewRaw in review_data:
            review = {
                'movie_id': reviewRaw[0],
                'username': reviewRaw[1],
                'description': reviewRaw[2],
                'created_on': reviewRaw[3],
                'rating': reviewRaw[4]
            }
            dataToReturn.append(review)
        return jsonify(dataToReturn)

    except (psycopg2.Error, Exception) as error:
        # Handle the error
        print("An error occurred:", error)
        return jsonify({'error': "error"}), 400 

@app.route('/reviews/username/<string:username>/mine', methods=['GET'])
def getMyReviews(username):
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM reviews WHERE username =  %s", (username,))
        review_data = cur.fetchall()
        cur.close()

        dataToReturn = []
        for reviewRaw in review_data:
            review = {
                'movie_id': reviewRaw[0],
                'username': reviewRaw[1],
                'description': reviewRaw[2],
                'created_on': reviewRaw[3],
                'rating': reviewRaw[4]
            }
            dataToReturn.append(review)
        return jsonify(dataToReturn)

    except (psycopg2.Error, Exception) as error:
        # Handle the error
        print("An error occurred:", error)
        return jsonify({'error': "error"}), 400

@app.route('/reviews/username/<string:username>/average', methods=['GET'])
def getMyAvarageReview(username):
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM reviews WHERE username =  %s", (username,))
        review_data = cur.fetchall()
        cur.close()

        sumAvr = 0
        n = 0
        for reviewRaw in review_data:
            rating = reviewRaw[4] #getRating
            sumAvr+= rating
            n+=1
        avarage = sumAvr/n
        return jsonify({'avarage': avarage})

    except (psycopg2.Error, Exception) as error:
        # Handle the error
        print("An error occurred:", error)
        return jsonify({'error': "error"}), 400 
#-------------------------------------------------------movies---------------

@app.route('/movies', methods=['GET'])
def get_movies():
    movie_data = movies.get_movies()
    if movie_data is None:
        return jsonify({'error': 'Movie not found'}), 404
    return jsonify(movie_data)

@app.route('/movie/<int:movie_id>', methods=['GET'])
def get_movie(movie_id):
    movie_data = movies.get_movie_details(movie_id)
    if movie_data is None:
        return jsonify({'error': 'Movie not found'}), 404
    return jsonify(movie_data)

@app.route('/searchmovie/<string:movie_title>', methods=['GET'])
def search_movies(movie_title):
    movie_data = movies.search_movies(movie_title)
    if movie_data is None:
        return jsonify({'error': 'Movie not found'}), 404
    return jsonify(movie_data)

if   __name__ ==   "__main__" :   
        app.run( host='127.0.0.1', port=8080, debug=False)
