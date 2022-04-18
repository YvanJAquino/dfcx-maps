import json
import googlemaps

API_KEY = 'AIzaSyA3XwIfGzcj1V868dJfsXhXkB5AHx0Bke0'
ADDRESS = '20166'
# Load a list of addresses stored as JSON
with open('addresses.json', 'r') as src:
    DESTINATIONS = json.load(src)

gmaps = googlemaps.Client(key=API_KEY)

distance_matrix = gmaps.distance_matrix(origins=ADDRESS, destinations=DESTINATIONS, mode='driving')
print(json.dumps(distance_matrix['rows'][0]['elements'], indent=2))
print(len(distance_matrix['rows'][0]['elements']))
sorted_matrix = [(
            distance_matrix['destination_addresses'][idx], 
            distance_matrix['rows'][0]['elements'][idx]['distance']['value'],
            distance_matrix['rows'][0]['elements'][idx]['duration']['value']
        ) for idx in range(len(DESTINATIONS))]
sorted_matrix.sort(key=lambda r: r[2])
print(json.dumps(sorted_matrix, indent=2))


# def find_nearest_facilities(address: str):
#     import googlemaps
#     API_KEY = 'AIzaSyA3XwIfGzcj1V868dJfsXhXkB5AHx0Bke0'
#     gmaps = googlemaps.Client(key=API_KEY)
#     distance_matrix = gmaps.distance_matrix(origins=ADDRESS, destinations=DESTINATIONS, mode='driving')
#     sorted_matrix = [(
#             distance_matrix['destination_addresses'][idx], 
#             distance_matrix['rows'][0]['elements'][idx]['distance']['value'],
#             distance_matrix['rows'][0]['elements'][idx]['duration']['value']
#         ) for idx in range(len(DESTINATIONS))]
#     sorted_matrix.sort(key=lambda r: r[2])
#     return sorted_matrix

