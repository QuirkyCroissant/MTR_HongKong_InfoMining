import pandas as pd
import matplotlib.pyplot as plt
import contextily as ctx
import matplotlib.image as mpimg

edges_set = pd.read_csv("datasets/MTR_Edges_Data.csv")
stations_set = pd.read_csv("datasets/Stations_With_Coords_And_Maps.csv")


# Load the custom background image
background_img = mpimg.imread('media/hk_custom_background.png')

fig, ax = plt.subplots(figsize=(30, 30))

#ax.set_aspect('equal')
# min_long, max_long, min_lat, max_lat
ax.imshow(background_img, extent=[113.8994, 114.2791, 22.2014, 22.5321])


stations_set['x'] = stations_set['long']
stations_set['y'] = stations_set['lat']

# plotting the station nodes 
for _, row in edges_set.iterrows():
    
    start_station = stations_set.loc[
        (stations_set['station_eng'] == row['start_eng']) &
        (stations_set['line'] == row['line'])
    ].iloc[0]

    end_station = stations_set.loc[
        (stations_set['station_eng'] == row['end_eng']) &
        (stations_set['line'] == row['line'])
    ].iloc[0]

    if not start_station.empty and not end_station.empty:
        ax.plot([start_station['x'], end_station['x']],
                 [start_station['y'], end_station['y']],
                 color=row['color'], linewidth=2)
    else:
        print(f"Missing station data for edge: {row['start_eng']} to {row['end_eng']} on line {row['line']}")


cur_printed_names = set()

# Plot each station as a white dot and its corresponding name
for _, row in stations_set.iterrows():

    ax.plot(row['x'], row['y'], 'wo', markersize=10, markerfacecolor='grey')

    offset_x = 0.002
    offset_y = 0.002

    if row['station_eng'] not in cur_printed_names:

        new_x_coord = offset_x + row['x']
        new_y_coord = offset_y + row['y']

        if row['line'] == 'Island':
            ax.text(new_x_coord, new_y_coord, row['station_eng'], color='white', fontsize=8, rotation=-50, ha='right')
            cur_printed_names.add(row['station_eng'])

        elif row['line'] in ['Airport Express', 'Disneyland Resort', 'Tung Chung']:
            ax.text(new_x_coord, new_y_coord, row['station_eng'], color='white', fontsize=8, ha='right')
            cur_printed_names.add(row['station_eng'])

        else:
            ax.text(new_x_coord, new_y_coord, row['station_eng'], color='white', fontsize=8, rotation=-45, ha='right')
            cur_printed_names.add(row['station_eng'])
    

#ctx.add_basemap(ax, crs='EPSG:4326', source=ctx.providers.OpenStreetMap.Mapnik)
#ax.set_facecolor('#1d1d1d')

plt.grid(False)
plt.axis('off')

plt.savefig('media/hong_kong_mtr_map.png', bbox_inches='tight', pad_inches=0)
