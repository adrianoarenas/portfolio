import pandas as pd
import boto3
import json
from sqlalchemy import create_engine, text

from secrets import username, password_db, host, port, dbname,\
    access_key, secret_access_key

from queries import raw_upsert_query, drop_temp_query


def list_not_processed_files(bucket, prefix):
    """
    Reading json files in bucket
    """
    files = []
    
    my_bucket = s3.Bucket(bucket)
    
    for object_name in my_bucket.objects.filter(Prefix="{}/".format(prefix)):
        files.append(object_name.key)
    
    return files

def surf_file_to_df(bucket, key):
    response = s3.Object(bucket, key)
    contentBody = response.get()['Body'].read().decode('utf-8')
    surf_json = json.loads(contentBody)
    df = pd.json_normalize(surf_json['data']['weather'], ['hourly'], ['date'])
    df_upload = df[['date','time', 'tempC', 'tempF', 'windspeedMiles', 'windspeedKmph',
               'winddirDegree', 'winddir16Point', 'weatherCode', 'visibility',
               'visibilityMiles', 'sigHeight_m', 'swellHeight_m', 'swellHeight_ft',
               'swellDir', 'swellDir16Point', 'swellPeriod_secs', 'waterTemp_C',
               'waterTemp_F']]
    return(df_upload)

def moving_s3_file(bucket, old_prefix, new_prefix, file_name):
    
    old_name = "{0}/{1}/{2}".format(bucket, old_prefix, file_name)
    
    old_key = "{0}/{1}".format(old_prefix, file_name)
    new_key = "{0}/{1}".format(new_prefix, file_name)
    
    s3.Object(bucket, new_key).copy_from(CopySource=old_name)
    s3.Object(bucket, old_key).delete()


if __name__ == '__main__':
    #S3 Resource
    s3 = boto3.resource('s3',
                aws_access_key_id = access_key,
                aws_secret_access_key = secret_access_key)
    
    #DB connection
    engine = create_engine('postgresql://{username}:{password_db}@{host}:{port}/{dbname}'.format(username = username,\
                                                                                            password_db = password_db,\
                                                                                            host = host,\
                                                                                            port = port,\
                                                                                            dbname = dbname))
    bucket = 'galapagos-surf-eu-west-2'

    not_processed = list_not_processed_files(bucket, 'not_processed')
    
    for key in not_processed:

        file_name = key.split('/')[-1]

        df = surf_file_to_df(bucket, key)

        df.to_sql('temp_raw', con=engine)
        engine.execute(raw_upsert_query)
        engine.execute(drop_temp_query)

        print("Processed file: " + key)

        moving_s3_file(bucket, 'not_processed', 'processed', file_name)
