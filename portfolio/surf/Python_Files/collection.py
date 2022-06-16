import requests
import json
from datetime import datetime

import boto3
from secrets import access_key, secret_access_key, api_key


def api_connection(tide, format, lat, lon, tp, api_key):
    base_url = 'http://api.worldweatheronline.com'
    
    api_values = {'tide': tide,
                  'format': format,
                  'lat': lat,
                  'lon': lon,
                  'tp': tp,
                  'api_key': api_key}
    
    api = '/premium/v1/marine.ashx?key={api_key}&format={format}&q={lat},{lon}&tide={tide}&tp={tp}'\
    .format(api_key = api_values['api_key'],\
            format = api_values['format'],\
            lat = api_values['lat'],\
            lon = api_values['lon'],\
            tide = api_values['tide'],\
            tp = api_values['tp'])
    
    url = base_url + api
    response = requests.get(url)
    json_text = response.json()
    
    json_string = json.dumps(json_text)
    
    return(json_string)

def s3_load(bucket, access_key, secret_access_key, json_string):
    utcs_now = datetime.utcnow().strftime('%Y%m%d_%H%M')
    bucket = bucket
    client = boto3.client('s3',
                     aws_access_key_id = access_key,
                     aws_secret_access_key = secret_access_key)
    key = 'not_processed/surf_data_{}.json'.format(utcs_now)
    client.put_object(Body = json_string, 
                  Bucket = bucket, 
                  Key = key)

if __name__ == '__main__':
    json_string = api_connection('yes', 'json', -0.763184, -90.332251, 1, api_key)
    s3_load('galapagos-surf-eu-west-2', access_key, secret_access_key, json_string)