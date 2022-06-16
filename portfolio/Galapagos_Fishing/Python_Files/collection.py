import requests
import json
from datetime import datetime

import boto3
from secrets import access_key, secret_access_key, api_key


def api_connection(version, timespan, message, file_format, ship, api_key):
    base_url = 'https://services.marinetraffic.com/api'
    api_values = {'version': version,
                'timespan': timespan,
                'message': message,
                'file_format': file_format,
                'ship': ship,
                'api_key': api_key}

    api = '/exportvessels/{api_key}?v={version}&timespan={timespan}&msgtype={message}&protocol={file_format}&shiptype={ship}'\
    .format(version = api_values['version'],\
            api_key = api_values['api_key'],\
            timespan = api_values['timespan'],\
            message = api_values['message'],\
            file_format = api_values['file_format'],\
            ship = api_values['ship'])

    url = base_url + api
    response = requests.get(url)
    json_string = json.dumps(response)
    return(json_string)

def s3_load(bucket, access_key, secret_access_key, json_string):
    utcs_now = datetime.utcnow().strftime('%Y%m%d_%H%M')
    bucket = bucket
    client = boto3.client('s3',
                     aws_access_key_id = access_key,
                     aws_secret_access_key = secret_access_key)
    key = 'not_processed/fishing_vessels_{}.json'.format(utcs_now)
    client.put_object(Body = json_string, 
                  Bucket = bucket, 
                  Key = key)

if __name__ == '__main__':
    json_string = api_connection(8, 5, 'extended', 'json', 2, api_key)
    s3_load('galapagos-fishing-vessels-eu-west-1', access_key, secret_access_key, json_string)