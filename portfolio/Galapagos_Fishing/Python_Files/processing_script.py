import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
import contextily as cx
import math
from shapely.geometry import LineString, Polygon
import os
from pyproj import Transformer
import json

import boto3


## S3 keys ##
from secrets import access_key, secret_access_key


def list_not_processed_files(bucket, prefix):
    """
    Reading json files in bucket
    """
    bucket = bucket
    prefix = prefix
    files = []

    for key in s3.list_objects(Bucket=bucket, Prefix = prefix)['Contents']:
        files.append(key['Key'])
    
    return files


def import_map(LON_min, LAT_min, LON_max, LAT_max):
    """
    Importing map with defined coordinates
    """
    glpgs_img, glpgs_ext = cx.bounds2img(LON_min,
                                        LAT_min,
                                        LON_max,
                                        LAT_max,
                                        ll=True,
                                        source=cx.providers.OpenStreetMap.DE
                                        )
    return(glpgs_img, glpgs_ext)



def normalise_column_names(df, lat, lon):
    """
    Normalising the latitude and longitude column names in the dataframe
    """
    df.rename(columns={lat: "latitude", lon: "longitude"}, inplace = True)
    return df


def transform_to_web_mercator(row):
    """
    Coordinates come in as decimal, as we use a flat projected map we need to transform to pseudp web mercator (epsg:3857)
    """
    transformer = Transformer.from_crs("epsg:4326", "epsg:3857")
    return (transformer.transform(row.latitude, row.longitude))


def apply_web_mercantor(df):
    """
    Applying transformation to dataframe
    """
    transformation = df.apply(transform_to_web_mercator, axis=1)
    transformation_df = transformation.apply(pd.Series)
    transformation_df.columns=['longitude_wm','latitude_wm']
    return transformation_df

def marine_reserve_polygon(file_name):
    """
    Applying the transformation to the marine reserve coordinates and creating a polygon
    """
    marine_reserve_coords = pd.read_csv('{}.csv'.format(file_name))
    marine_reserve_coords = normalise_column_names(marine_reserve_coords, 'latitude', 'longitude')
    marine_reserve_wm = apply_web_mercantor(marine_reserve_coords)

    polygon_coords = []
    for index, row in marine_reserve_wm.iterrows():
        polygon_coords.append(tuple(row))
    polygon_coords.append(polygon_coords[0])

    return Polygon(polygon_coords)


def direction_line(df):
    ref_angle = (df['HEADING'] + 90)%360
    dist_intersection = 500000
    dist_map = 40000
            
    angle_rad = math.radians(ref_angle)
    
    #This lat and lon are longers as its just drawing a straight line to see if intersects
    longitude_2_intersection = df['longitude_wm'] + dist_intersection * math.cos(angle_rad)
    latitude_2_intersection = df['latitude_wm'] + dist_intersection * math.sin(angle_rad)
    
    line = LineString([(df['longitude_wm'], df['latitude_wm']), (longitude_2_intersection, latitude_2_intersection)])
    intersects = line.intersects(mr_polygon)
    
    
    #This lat and lon are shorter and will be added to the DF just for plotting purposes in the map
    longitude_2_map = df['longitude_wm'] + dist_map * math.cos(angle_rad)
    latitude_2_map = df['latitude_wm'] + dist_map * math.sin(angle_rad)
    
    return (longitude_2_map, latitude_2_map, intersects)




if __name__ == '__main__':
    s3 = boto3.client('s3',
                    aws_access_key_id = access_key,
                    aws_secret_access_key = secret_access_key)

    mr_polygon = marine_reserve_polygon('galapagos_marine_reserve')

    not_processed = list_not_processed_files(bucket = 'galapagos-fishing-vessels-eu-west-1', prefix='not_processed')

    for file in not_processed:
        response = s3.get_object(Bucket='galapagos-fishing-vessels-eu-west-1', Key=file)
        contentBody = response.get("Body").read().decode('utf-8')
        data = pd.read_json(contentBody)
        normalise_column_names(data, 'LAT', 'LON')

        #transforming to wm coordinates
        data_wm_coords = pd.concat([data, apply_web_mercantor(data)], axis = 1)

        #getting 
        second_coords = data_wm_coords.apply(direction_line, axis=1)
        second_coords_wm = second_coords.apply(pd.Series)
        second_coords_wm.columns=['longitude_wm_2','latitude_wm_2','intersects']

        final_data = pd.concat([data_wm_coords, second_coords_wm], axis = 1)

        print(final_data)
