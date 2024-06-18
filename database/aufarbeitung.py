#%%
import json
import pandas as pd
from tinydb import TinyDB, Query
#%%
db = TinyDB('db.json')

def get_entries_for_topic(db, topic):
    try:
        # Load the entire JSON data
        with open(db.storage._handle.name) as f:
            data = json.load(f)

        # Retrieve the entries for the given topic
        entries = data.get(topic, {})
        return entries
    except Exception as e:
        print(f"An error occurred: {e}")
        return {}

def create_disp_df(db, topic):
    entries = get_entries_for_topic(db, topic)
    disp = F"fill_level_grams-{entries["1"]["dispenser"]}"
    df = pd.DataFrame(columns=["bottle", "time", disp])
    for key in entries:
        df.loc[len(df)] = [entries[key]['bottle'], entries[key]['time'], entries[key]['fill_level_grams']]
    return df

def create_disp_vibration_df(db, topic):
    entries = get_entries_for_topic(db, topic)
    disp = F"vibration-index-{entries["1"]["dispenser"]}"
    df = pd.DataFrame(columns=["bottle", "time", disp])

    for key in entries:
        df.loc[len(df)] = [entries[key]['bottle'], entries[key]['time'], entries[key]['vibration-index']]
    return df
def create_temp_df(db, topic):
    df = pd.DataFrame(columns=["time", "temperature_C"])
    entries = get_entries_for_topic(db, topic)
    for key in entries:
        df.loc[len(df)] = [entries[key]['time'], entries[key]['temperature_C']]
    return df

def create_ground_df(db, topic):
    df = pd.DataFrame(columns=["bottle", "is_cracked"])
    entries = get_entries_for_topic(db, topic)
    for key in entries:
        df.loc[len(df)] = [entries[key]['bottle'], entries[key]['is_cracked']]
    return df

def create_vibration_df(db, topic):
    df = pd.DataFrame()
    entries = get_entries_for_topic(db, topic)
    for key in entries:
        df[entries[key]['bottle']] = entries[key]['drop_vibration']
    return df

def create_weight_df(db, topic):
    df = pd.DataFrame(columns=["bottle", "time", "final_weight"])
    entries = get_entries_for_topic(db, topic)
    for key in entries:
        df.loc[len(df)] = [entries[key]['bottle'], entries[key]['time'], entries[key]['final_weight']]
    return df

fill_disp_red = create_disp_df(db, "iot1/teaching_factory_fast/dispenser_red")
fill_disp_blue = create_disp_df(db, "iot1/teaching_factory_fast/dispenser_blue")
fill_disp_green = create_disp_df(db, "iot1/teaching_factory_fast/dispenser_green")

fill_disp_red_vibration = create_disp_vibration_df(db, "iot1/teaching_factory_fast/dispenser_red/vibration")
fill_disp_blue_vibration = create_disp_vibration_df(db, "iot1/teaching_factory_fast/dispenser_blue/vibration")
fill_disp_green_vibration = create_disp_vibration_df(db, "iot1/teaching_factory_fast/dispenser_green/vibration")

temperatures = create_temp_df(db, "iot1/teaching_factory_fast/temperature")
ground_truth = create_ground_df(db, "iot1/teaching_factory_fast/ground_truth")

vibrations = create_vibration_df(db, "iot1/teaching_factory_fast/drop_vibration")

final_weight = create_weight_df(db, "iot1/teaching_factory_fast/scale/final_weight")

#print(fill_disp_red.head())
#print(fill_disp_red_vibration.head())
#print(temperatures.head())

combined_df = pd.merge(fill_disp_red.drop(['time'], axis=1), fill_disp_blue.drop(['time'], axis=1), on='bottle')
combined_df = pd.merge(combined_df, fill_disp_green.drop(['time'], axis=1), on='bottle')
combined_df = pd.merge(combined_df, fill_disp_red_vibration.drop(['time'], axis=1), on='bottle')
combined_df = pd.merge(combined_df, fill_disp_blue_vibration.drop(['time'], axis=1), on='bottle')
combined_df = pd.merge(combined_df, fill_disp_green_vibration.drop(['time'], axis=1), on='bottle')
#combined_df = pd.merge(combined_df, temperatures.drop(['time'], axis=1), on='bottle')

print(combined_df)

data = pd.DataFrame(["temp_mean_C","vibration-red-vibration","vibration-blue-vibration","vibration-green-vibration",
                     "fill_level_grams-red","fill_level_grams-blue","fill_level_grams-green"])