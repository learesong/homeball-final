import os
import csv

from project.settings import APP_STATIC

def get_price(postcode):
    with open(os.path.join(APP_STATIC, 'dataset.csv'), mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter='\t')

        for row in csv_reader:
            if row['postcode'] == postcode:
                return row['price']

    return None


def clamp(value, dictionary):
    prev = None

    for k, v in dictionary.items():
        if value == k or (value < k and not prev):
            return v
        elif value < k:
            prev = (k, v)
        elif value > k and prev:
            return prev[1]

    return None
