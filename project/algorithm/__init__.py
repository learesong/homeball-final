from project.algorithm.settings import STATION_DISTANCE, BEDROOM_NUMBER, STATE, TYPE
from project.algorithm.helpers import get_price, clamp


def god_algorithm(options):
    price = int(get_price(options['postcode']))

    percentage = 0

    percentage += TYPE[options['type']]
    percentage += STATE[options['state']]

    bedrooms = clamp(options['bedrooms'], BEDROOM_NUMBER)
    if bedrooms is None:
        bedrooms = BEDROOM_NUMBER[max(BEDROOM_NUMBER.keys())]
    percentage += options['bedrooms'] * bedrooms

    distance = clamp(options['station_distance'], STATION_DISTANCE)
    if distance is None:
        distance = STATION_DISTANCE[max(STATION_DISTANCE.keys())]
    percentage += distance

    # print('Type', TYPE[options['type']])
    # print('State', STATE[options['state']])
    # print('Bedrooms', bedrooms)
    # print('Distance', distance)
    # print('Price', price)
    # print('Percentage', percentage)

    price += price * percentage

    return price
