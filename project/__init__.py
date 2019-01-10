from flask import Flask, render_template, request, jsonify
import requests

from project.algorithm import god_algorithm
from project.algorithm.helpers import get_price

from project.helpers import get_distance, get_nearby_stations, get_best, get_nearby

app = Flask(__name__)
# app.config['DEBUG'] = True

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/map')
def entry_point():
    return render_template('map.html')


@app.route('/choice', methods=['POST'])
def choice():
    # Longtitude and latitude in XXX,XXX format
    location = request.form.get('latlng')

    station = get_nearby_stations(location, limit=1)[0]

    # return jsonify(stations)

    r = requests.get('https://maps.googleapis.com/maps/api/geocode/json', params={
    	'latlng': location,
    	'key': 'AIzaSyAaKaZGr8pvM2-sCitY_2tIfaCX90o6t0w'
    })

    r = r.json()

    add_comps = r['results'][0]['address_components']

    postcode = None

    for idx, comp in enumerate(add_comps):
        if comp['types'][0] == 'postal_code':
            postcode = comp['long_name'].split(' ')[0]
            break

    return render_template('choice.html', postcode=postcode, station_dist=station['distance'], location=location)

import locale

@app.route('/result', methods=['POST', 'GET'])
def evaluate():
    location = request.form.get('location')

    extras = {
        'subway_stations': get_nearby(location, 'subway_station'),
        'train_stations': get_nearby(location, 'train_station'),
        'supermarkets': get_nearby(location, 'supermarket', limit=5),
        'cafes': get_best(location, 'cafe'),
        'restaurants': get_best(location, 'restaurant'),
        'hospitals': get_nearby(location, 'hospital'),
        'dentists': get_nearby(location, 'dentist'),
        'schools': get_nearby(location, 'school', limit=5),
        'bars': get_best(location, 'bar', limit=6)
    }

    user_input = {
        'postcode': request.form.get('postcode'),
        'type': request.form.get('type'),
        'station_distance': int(request.form.get('station_dist')),
        'state': request.form.get('state'),
        'bedrooms': int(request.form.get('bedrooms'))
    }

    price = god_algorithm(user_input)

    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
    price = locale.currency(price, grouping=True)
    price = '£' + price[1:-3]

    # return jsonify(extras)

    # first = r['results'][0]['address_components'][0]['long_name']
    # second = r['results'][0]['address_components'][1]['long_name']

    return render_template('result.html', extras=extras, price=price)

    # return jsonify([user_input['postcode'], price])
