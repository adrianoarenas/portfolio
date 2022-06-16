#Upserting data into Tier 1 table (Raw data)
raw_upsert_query = """
INSERT INTO galapagos.tortuga_bay_raw (date, time, tempc, tempf, windspeedmiles, windspeedkmph,
winddirdegree, winddir16point, weathercode, visibilitykm, visibilitymiles, sigheight_m, swellheight_m,\
swellheight_ft, swelldir, swelldir16point, swellperiods_secs, watertempc, watertempf) \
SELECT "date"::date, "time"::int, "tempC"::int, "tempF"::int, "windspeedMiles"::int, "windspeedKmph"::int, \
"winddirDegree"::int, "winddir16Point", "weatherCode"::int, "visibility"::int, "visibilityMiles"::int, \
"sigHeight_m"::float, "swellHeight_m"::float, "swellHeight_ft"::float,"swellDir"::int,\
"swellDir16Point", "swellPeriod_secs"::float, "waterTemp_C"::int, "waterTemp_F"::int from public.temp_raw

ON CONFLICT (date, time) DO \

UPDATE SET tempc = EXCLUDED.tempC, tempf = EXCLUDED.tempF, windspeedmiles = EXCLUDED.windspeedMiles, \
windspeedkmph = EXCLUDED.windspeedKmph, winddirdegree = EXCLUDED.winddirDegree, \
winddir16point = EXCLUDED.winddir16Point, weathercode = EXCLUDED.weatherCode, visibilitykm = EXCLUDED.visibilitykm, \
visibilitymiles = EXCLUDED.visibilityMiles, sigheight_m = EXCLUDED.sigHeight_m, swellheight_m = EXCLUDED.swellHeight_m, \
swellheight_ft = EXCLUDED.swellHeight_ft, swelldir = EXCLUDED.swellDir, swelldir16point = EXCLUDED.swellDir16Point, \
swellperiods_secs = EXCLUDED.swellperiods_secs, watertempc = EXCLUDED.watertempc, watertempf = EXCLUDED.watertempf;
"""

#Deleting temp table created by pandas from the dataframe
drop_temp_query = """DROP TABLE IF EXISTS temp_raw;"""