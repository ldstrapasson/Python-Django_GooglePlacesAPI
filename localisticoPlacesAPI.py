from googleplaces import GooglePlaces
import requests
import json


class GooglePlacesApi(object):
    def __init__(self, apiKey):
        self.apiKey = apiKey

    def search_places_by_name(self, location, name):
        google_places = GooglePlaces(self.apiKey)
        if len(name) > 20:
            print(
                "Error: The maximum lenght of 'name' needs to be less than 20 characters")
        else:
            query_result = google_places.nearby_search(
                location=location, keyword=name)
            for place in query_result.places:
                print(place.name)
                print(place.place_id)
                # To get further details ref (https://developers.google.com/maps/documentation/javascript/reference/places-service#PlacesService.findPlaceFromQuery)
                # get_details() needs to be called in this case
                place.get_details()
                # get_details() needs to be called or will raise googleplaces.GooglePlacesAttributeError.
                print(place.international_phone_number)

    def search_places_by_coordinate(self, location, radius, name):
        endpoint_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
        places = []
        params = {
            'location': location,
            'radius': radius,
            'name': name,
            'key': self.apiKey,
        }
        # get request to endpoint with params dict
        res = requests.get(endpoint_url, params=params)
        # deserializing json and putting into dict obj
        results = json.loads(res.text)
        # apending results into places where 'results' is a key value pair
        places.extend(results['results'])
        return places

    def get_place_details(self, place_id, fields):
        endpoint_url = "https://maps.googleapis.com/maps/api/place/details/json"
        params = {
            'placeid': place_id,
            # list of comma separated strings (fields)
            'fields': ",".join(fields),
            'key': self.apiKey
        }
        # get request to endpoint with params dict
        res = requests.get(endpoint_url, params=params)
        # deserializing json and putting into dict obj
        place_details = json.loads(res.text)
        return place_details

    def print_places(self, fields, places):
        for place in places:  # for each place get details, exception key, print selected key fields
            details = api.get_place_details(place['place_id'], fields)
            try:
                name = details['result']['name']
            except KeyError:
                name = ""
            try:
                place_id = details['result']['place_id']
            except KeyError:
                place_id = ""
            try:
                phone_number = details['result']['international_phone_number']
            except KeyError:
                phone_number = ""

            print("Name:", name)
            print("Place ID", place_id)
            print("Phone Number", phone_number)


if __name__ == '__main__':
    api = GooglePlacesApi("Your_key_here")  # APIkey
    places = api.search_places_by_coordinate("51.510765, -0.136588",
                                             "100", "localistico")
    fields = ['name', 'international_phone_number',
              'place_id']  # list of selected fileds
    print('--------------Search by coordinate------------')
    api.print_places(fields, places)
    print('--------------Search by name------------------')
    api.search_places_by_name(
        'London', 'localistico')
