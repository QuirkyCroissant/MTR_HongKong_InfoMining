import math
import pandas as pd

# Earths radius in kilometers
RADIUS = 6371

edges_set = pd.read_csv("datasets/MTR_Edges_Data.csv")
stations_set = pd.read_csv("datasets/Stations_With_Coords_And_Maps.csv")

# drops distances feature, if it is already included in the dataset
if 'edge_distance_km' in edges_set.columns:
    edges_set = edges_set.drop('edge_distance_km', axis=1)

# retrieve the coordinates of each station
station_coords = {row['station_eng']: (row['lat'], row['long']) for _, row in stations_set.iterrows()}

def haversine(a, b):
    """ Haversine formula, used to calculate the orthodromic distance between 2 geographical points on earth 
    Source: https://en.wikipedia.org/wiki/Haversine_formula"""

    lat_a, long_a = station_coords[a]
    lat_b, long_b = station_coords[b]

    delta_lat = math.radians(lat_b - lat_a)
    delta_long = math.radians(long_b - long_a)

    a = math.sin(delta_lat / 2)**2 + \
        math.cos(math.radians(lat_a)) * \
        math.cos(math.radians(lat_b)) * \
        math.sin(delta_long / 2)**2 
    
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return RADIUS * c

# evaluating distance of every edge, and if stations are in our records(station_coords) 
# than we append them in the distances list, if not we append None. This way we can just
# include the data as a column to the old dataframe and overwrite it with the distances.
distances = []
for _, row in edges_set.iterrows():
    start_node = row['start_eng']
    end_node = row['end_eng']

    if start_node in station_coords and end_node in station_coords:
        dist = haversine(start_node, end_node)
        distances.append(dist)
    else:
        distances.append(None)

edges_set['edge_distance_km'] = distances

edges_set.to_csv("datasets/MTR_Edges_Data.csv", index=False)
print(edges_set.head())
print("Distances of edges included and csv file modified.")
    

