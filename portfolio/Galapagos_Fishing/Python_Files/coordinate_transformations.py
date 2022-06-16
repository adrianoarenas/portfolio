from pyproj import Transformer
import pandas as pd
 
def normalise_column_names(df, lat, lon):
    df.rename(columns={lat: "latitude", lon: "longitude"}, inplace = True)
    return df

def transform_to_web_mercator(row):
    transformer = Transformer.from_crs("epsg:4326", "epsg:3857")
    return (transformer.transform(row.latitude, row.longitude))

def apply_web_mercantor(df):
    transformation = df.apply(transform_to_web_mercator, axis=1)
    transformation_df = transformation.apply(pd.Series)
    transformation_df.columns=['longitude_wm','latitude_wm']
    return transformation_df
