create table galapagos.tortuga_bay_raw 
(
    "date" date,
    time int,
    tempc int,
    tempf int,
    windspeedmiles int,
    windspeedkmph int,
    winddirdegree int,
    winddir16point varchar(10),
    weathercode int,
    visibilitykm int,
    visibilitymiles int,
    sigheight_m float,
    swellheight_m float,
    swellheight_ft float,
    swelldir int,
    swelldir16point varchar(10),
    swellperiods_secs float,
    watertempc int,
    watertempf int,
    
    CONSTRAINT tortuga_bay_raw_pkey PRIMARY KEY (date, time)
);