import geopandas as gpd
import numpy as np
from shapely.geometry import box

# Load world dataset and filter for USA
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
us = world[world['name'] == 'United States of America']

# Reproject to an equal-area projection
us = us.to_crs({'proj': 'cea'})

# Calculate the total area in square kilometers
total_area = us.geometry.area.iloc[0] / 10**6  # Convert from square meters to square kilometers

print(f"Total US area: {total_area:.2f} km²")

# Define latitude range (approximate for continental US)
lat_min, lat_max = 24, 49
lat_step = 0.5  # Smaller step for more granularity

# Initialize dictionary to store areas
areas = {}

# Calculate area for each latitude strip
for lat in np.arange(lat_min, lat_max, lat_step):
    # Create a box for the current latitude strip in the same CRS as the reprojected geometries
    bbox = box(-119, lat, -64, lat + lat_step)  # Adjusted longitudes to better fit the US
    bbox = gpd.GeoSeries([bbox], crs="EPSG:4326").to_crs(us.crs).iloc[0]

    # Calculate the fraction of US area in this strip
    intersection = us.geometry.iloc[0].intersection(bbox)
    if not intersection.is_empty:
        fraction = intersection.area / us.geometry.iloc[0].area
        # Calculate area in square kilometers
        area = fraction * total_area
    else:
        area = 0

    # Store the area
    areas[lat] = area

# Print results
for lat, area in areas.items():
    print(f"Latitude {lat:.2f}°-{lat+lat_step:.2f}°: {area:.2f} km²")

# Total calculated area
print(f"Total calculated area: {sum(areas.values()):.2f} km²")
