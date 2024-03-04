# this is a controller
from Api.DatabaseLayer import MoistureSensorDB
import numpy as np
from scipy import stats

dblayer = MoistureSensorDB


def add_new_data(id, moisturelevel):
    return dblayer.add_new_moisture_data(id, moisturelevel)


def get_latest_moisture_data_for_all_microcontrollers():
    return dblayer.get_latest_moisture_data_for_all_microcontrollers()

