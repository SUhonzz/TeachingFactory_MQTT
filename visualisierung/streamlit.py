import streamlit as st
import pandas as pd
from tinydb import TinyDB, Query

Data_Queue = Queue()


def get_data_from_topic(topic):
