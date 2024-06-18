#%%
import json
import pandas as pd
from tinydb import TinyDB, Query
#%%
db = TinyDB('./database/db.json')

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
    df = pd.DataFrame(columns=["index", "bottle", "time", "fill_level_grams"])
    entries = get_entries_for_topic(db, topic)
    for key in entries:
        df.loc[len(df)] = [key, entries[key]['bottle'], entries[key]['time'], entries[key]['fill_level_grams']]
    return df

def create_temp_df(db, topic):
    df = pd.DataFrame(columns=["index", "time", "temperature_C"])
    entries = get_entries_for_topic(db, topic)
    for key in entries:
        df.loc[len(df)] = [key, entries[key]['time'], entries[key]['temperature_C']]
    return df

def create_ground_df(db, topic):
    df = pd.DataFrame(columns=["index", "bottle", "is_cracked"])
    entries = get_entries_for_topic(db, topic)
    for key in entries:
        df.loc[len(df)] = [key, entries[key]['bottle'], entries[key]['is_cracked']]
    return df

def create_vibration_df(db, topic):
    df = pd.DataFrame()
    entries = get_entries_for_topic(db, topic)
    for key in entries:
        df[entries[key]['bottle']] = entries[key]['drop_vibration']
    return df

fill_disp_red = create_disp_df(db, "iot1/teaching_factory_fast/dispenser_red")
fill_disp_blue = create_disp_df(db, "iot1/teaching_factory_fast/dispenser_blue")
fill_disp_green = create_disp_df(db, "iot1/teaching_factory_fast/dispenser_green")

temperatures = create_temp_df(db, "iot1/teaching_factory_fast/temperature")
ground_truth = create_ground_df(db, "iot1/teaching_factory_fast/ground_truth")

vibrations = create_vibration_df(db, "iot1/teaching_factory_fast/drop_vibration")

#print(vibrations)