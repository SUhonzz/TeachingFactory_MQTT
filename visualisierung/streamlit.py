import streamlit as st
import pandas as pd
from tinydb import TinyDB, Query
import json

db = TinyDB('../database/db.json')


def get_entries_for_topic(db, topic):
    """
    This function retrieves all entries for a specified topic from the TinyDB database.

    Args:
    db (TinyDB): The TinyDB database instance.
    topic (str): The topic to retrieve entries for.

    Returns:
    dict: A dictionary of all entries for the specified topic.
    """
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


# Specify the topic
topic = "iot1/teaching_factory_fast/temperature"

# Get the entries for the specified topic
entries = get_entries_for_topic(db, topic)
print(entries)
