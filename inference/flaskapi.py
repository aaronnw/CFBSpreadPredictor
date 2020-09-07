from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import logging

app = Flask(__name__)
CORS(app, resources={r'/*': {'origins': '*'}})


@app.route('/fetch-game-id', methods=['GET'])
def fetch_game_id():
    year = request.args.get('year')
    week = request.args.get('week')
    home_team = request.args.get('home_team')
    headers = {
        'accept': 'application/json',
    }
    params = (
        ('year', str(year)),
        ('week', str(week)),
        ('home', str(home_team)),
    )
    try:
        response = requests.get('https://api.collegefootballdata.com/games', headers=headers, params=params)
        game = response.json()
        return jsonify(int(game[0]['id']))
    except ConnectionError as error:
        logging.error(error)
        return jsonify(repr(error))


@app.route('/game/<game_id>', methods=['GET'])
def fetch_game_details(game_id):
    # TODO main screen to pick game id from year/week/hometeam
    headers = {
        'accept': 'application/json',
    }
    params = (
        ('gameId', game_id),
    )
    try:
        response = requests.get('https://api.collegefootballdata.com/game/box/advanced', headers=headers, params=params)
        game_details = response.json()
        return jsonify(game_details)
    except ConnectionError as error:
        logging.error(error)
        return jsonify(repr(error))


@app.route('/games', methods=['GET'])
def fetch_all_games():
    year = request.args.get('year')
    week = request.args.get('week')
    headers = {
        'accept': 'application/json',
    }
    params = (
        ('year', str(year)),
        ('week', str(week)),
    )
    try:
        response = requests.get('https://api.collegefootballdata.com/games', headers=headers, params=params)
        return jsonify(response.json())
    except ConnectionError as error:
        logging.error(error)
        return jsonify(repr(error))


if __name__ == '__main__':
    app.debug = True
    app.run()
