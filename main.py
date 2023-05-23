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

@app.route('/profiles', methods=['GET'])
def get_profile():
    cur = conn.cursor()
    cur.execute("SELECT first_name, last_name, username, created_on, age, likedMovies FROM accounts")
    profile_data = cur.fetchone()
    cur.close()
    dataToReturn = []
    for profileRaw in profile_data:
        profile = {'first_name': profileRaw[0], 'last_name': profileRaw[1], 'username': profileRaw[2], 'created_on': profileRaw[3], 'age': profileRaw[4], 'likedMovies': profileRaw[5]}
        dataToReturn.append(profile)
    return jsonify(dataToReturn)

@app.route('/profile', methods=['POST'])
def create_profile():
    data = request.json
    age = data.get('age')
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    created_on = datetime.now()
    likedMovies = []

    if not age or not first_name or not last_name or not username or not email:
        return jsonify({'error': 'Invalid request. Write required fields.'}), 400
 
    cur = conn.cursor()
    cur.execute("INSERT INTO accounts (first_name, last_name, username, password, email, created_on, age,likedMovies) VALUES (%s, %s,%s, %s,%s, %s,%s, %s)", (first_name, last_name, username, password, email, created_on, age,likedMovies))
    conn.commit()
    cur.close()

    return jsonify({'message': 'Profile created'}), 201

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
