import pandas as pd
df = pd.read_csv("Motor_Vehicle_Collisions_-_Crashes_20260430.csv")
print(df.shape)
print(df.head())

df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

print(df.columns)

df["crash_date"] = pd.to_datetime(df["crash_date"], errors="coerce")

df = df.dropna(subset=["crash_date"])

text_cols = [
    "borough",
    "zip_code",
    "on_street_name",
    "cross_street_name",
    "off_street_name",
    "contributing_factor_vehicle_1",
    "vehicle_type_code_1"
]

for col in text_cols:
    df[col] = df[col].fillna("Unknown")

num_cols = [
    "number_of_persons_injured",
    "number_of_persons_killed",
    "number_of_pedestrians_injured",
    "number_of_pedestrians_killed",
    "number_of_cyclist_injured",
    "number_of_cyclist_killed",
    "number_of_motorist_injured",
    "number_of_motorist_killed"
]

df[num_cols] = df[num_cols].fillna(0)

df = df.drop_duplicates()

print(df.shape)
print(df.head())

dim_date = df[["crash_date"]].drop_duplicates().copy()

dim_date["date_key"] = dim_date["crash_date"].dt.strftime("%Y%m%d").astype(int)
dim_date["full_date"] = dim_date["crash_date"].dt.date
dim_date["year"] = dim_date["crash_date"].dt.year
dim_date["quarter"] = dim_date["crash_date"].dt.quarter
dim_date["month"] = dim_date["crash_date"].dt.month
dim_date["day"] = dim_date["crash_date"].dt.day
dim_date["day_of_week"] = dim_date["crash_date"].dt.day_name()

dim_date = dim_date[[
    "date_key", "full_date", "year", "quarter", "month", "day", "day_of_week"
]]

print(dim_date.head())
print(dim_date.shape)

location_cols = [
    "borough",
    "zip_code",
    "latitude",
    "longitude",
    "on_street_name",
    "cross_street_name",
    "off_street_name"
]

dim_location = df[location_cols].drop_duplicates().reset_index(drop=True)
dim_location["location_key"] = dim_location.index + 1

dim_location = dim_location[[
    "location_key",
    "borough",
    "zip_code",
    "latitude",
    "longitude",
    "on_street_name",
    "cross_street_name",
    "off_street_name"
]]

print(dim_location.head())
print(dim_location.shape)

dim_vehicle = df[["vehicle_type_code_1"]].drop_duplicates().reset_index(drop=True)
dim_vehicle["vehicle_key"] = dim_vehicle.index + 1

dim_vehicle = dim_vehicle[[
    "vehicle_key",
    "vehicle_type_code_1"
]]

print(dim_vehicle.head())
print(dim_vehicle.shape)

dim_factor = df[["contributing_factor_vehicle_1"]].drop_duplicates().reset_index(drop=True)
dim_factor["factor_key"] = dim_factor.index + 1

dim_factor = dim_factor[[
    "factor_key",
    "contributing_factor_vehicle_1"
]]

print(dim_factor.head())
print(dim_factor.shape)

fact = df.copy()

fact["date_key"] = fact["crash_date"].dt.strftime("%Y%m%d").astype(int)

fact = fact.merge(
    dim_location,
    on=[
        "borough",
        "zip_code",
        "latitude",
        "longitude",
        "on_street_name",
        "cross_street_name",
        "off_street_name"
    ],
    how="left"
)

fact = fact.merge(
    dim_vehicle,
    on="vehicle_type_code_1",
    how="left"
)

fact = fact.merge(
    dim_factor,
    on="contributing_factor_vehicle_1",
    how="left"
)

fact["crash_fact_id"] = range(1, len(fact) + 1)

fact_crash = fact[[
    "crash_fact_id",
    "date_key",
    "location_key",
    "vehicle_key",
    "factor_key",
    "number_of_persons_injured",
    "number_of_persons_killed",
    "number_of_pedestrians_injured",
    "number_of_pedestrians_killed",
    "number_of_cyclist_injured",
    "number_of_cyclist_killed",
    "number_of_motorist_injured",
    "number_of_motorist_killed"
]]

print(fact_crash.head())
print(fact_crash.shape)

import os
os.makedirs("HW2/output", exist_ok=True)

dim_date.to_csv("HW2/output/dim_date.csv", index=False)
dim_location.to_csv("HW2/output/dim_location.csv", index=False)
dim_vehicle.to_csv("HW2/output/dim_vehicle.csv", index=False)
dim_factor.to_csv("HW2/output/dim_contributing_factor.csv", index=False)

fact_crash.to_csv("HW2/output/fact_crash.csv", index=False)

print("All files exported successfully")
