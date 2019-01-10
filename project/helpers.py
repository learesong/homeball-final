import requests

def get_distance(origin, dest):
    d = ','.join([str(dest['lat']), str(dest['lng'])])

    data = requests.get('https://maps.googleapis.com/maps/api/distancematrix/json', params={
        'units': 'imperial',
        'origins': origin,
        'destinations': d,
        'mode': 'walking',
    	'key': 'AIzaSyAaKaZGr8pvM2-sCitY_2tIfaCX90o6t0w'
    })

    return data.json()['rows'][0]['elements'][0]['distance']['value']


def get_nearby_stations(location, limit=3):
    data = requests.get('https://maps.googleapis.com/maps/api/place/nearbysearch/json', params={
    	'location': location,
        'type': 'subway_station',
        'keyword': 'station',
        'rankby': 'distance',
        'name': 'station',
    	'key': 'AIzaSyAaKaZGr8pvM2-sCitY_2tIfaCX90o6t0w'
    })

    data = data.json()

    stations = []

    for station in data['results'][0:limit]:
        formatted = {
            'name': station['name'],
            'location': station['geometry']['location'],
            'distance': get_distance(location, station['geometry']['location'])
        }

        stations.append(formatted)

    return stations


def get_nearby(location, type, keyword=None, limit=3):
    params = {
    	'location': location,
        'type': type,
        'rankby': 'distance',
    	'key': 'AIzaSyAaKaZGr8pvM2-sCitY_2tIfaCX90o6t0w'
    }

    if keyword:
        params['keyword'] = keyword

    data = requests.get('https://maps.googleapis.com/maps/api/place/nearbysearch/json', params=params)

    data = data.json()

    places = []

    for place in data['results'][0:limit]:
        formatted = {
            'name': place['name'],
            'location': place['geometry']['location'],
            'distance': get_distance(location, place['geometry']['location'])
        }

        places.append(formatted)

    return places


def get_best(location, type, radius=750, keyword=None, limit=3):
    params = {
    	'location': location,
        'type': type,
        'radius': radius,
    	'key': 'AIzaSyAaKaZGr8pvM2-sCitY_2tIfaCX90o6t0w'
    }

    if keyword:
        params['keyword'] = keyword

    data = requests.get('https://maps.googleapis.com/maps/api/place/nearbysearch/json', params=params)

    data = data.json()

    places = []

    for place in data['results'][0:limit]:
        formatted = {
            'name': place['name'],
            'location': place['geometry']['location'],
            'rating': place['rating'] if 'rating' in place else 0,
            'distance': get_distance(location, place['geometry']['location'])
        }

        places.append(formatted)

    return sorted(places, key=lambda s: s['rating'], reverse=True)
