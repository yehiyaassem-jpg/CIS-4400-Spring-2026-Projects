Snow flake data warehouse table creation script:

CREATE OR REPLACE DATABASE CIS4400_HW2;
USE DATABASE CIS4400_HW2;

CREATE OR REPLACE SCHEMA CRASH_DW;
USE SCHEMA CRASH_DW;

CREATE OR REPLACE TABLE dim_date (
    date_key INT,
    full_date DATE,
    year INT,
    quarter INT,
    month INT,
    day INT,
    day_of_week STRING
);

CREATE OR REPLACE TABLE dim_location (
    location_key INT,
    borough STRING,
    zip_code STRING,
    latitude FLOAT,
    longitude FLOAT,
    on_street_name STRING,
    cross_street_name STRING,
    off_street_name STRING
);

CREATE OR REPLACE TABLE dim_vehicle (
    vehicle_key INT,
    vehicle_type_code_1 STRING
);

CREATE OR REPLACE TABLE dim_contributing_factor (
    factor_key INT,
    contributing_factor_vehicle_1 STRING
);

CREATE OR REPLACE TABLE fact_crash (
    crash_fact_id INT,
    date_key INT,
    location_key INT,
    vehicle_key INT,
    factor_key INT,
    number_of_persons_injured INT,
    number_of_persons_killed INT,
    number_of_pedestrians_injured INT,
    number_of_pedestrians_killed INT,
    number_of_cyclist_injured INT,
    number_of_cyclist_killed INT,
    number_of_motorist_injured INT,
    number_of_motorist_killed INT
);
