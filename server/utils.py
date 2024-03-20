import json
import pickle
import numpy as np

global __model
global __location
global __data_columns



def load_artifacts():
    global __data_columns
    global __location
    with open("./artifacts/columns.json", "r") as f:
        __data_columns = json.load(f)['data_columns']

    __location = __data_columns[3:]

    global __model
    with open("./artifacts/home_prices_model.pickle","rb") as f:
        __model = pickle.load(f)

def get_locations():
    return __location

def get_data_columns():
    return __data_columns

def clear_model():
    __model = None

def get_estimated_price(location, total_sqft, bath, bhk):
    try:
        loc = __data_columns.index(location.lower())
    except:
        loc = -1
    x = np.zeros(len(__data_columns))
    x[0] = total_sqft
    x[1] = bath
    x[2] = bhk

    if loc>=0:
        x[loc] = 1

    return round(__model.predict([x])[0], 2)


if __name__ == "__main__":
    load_artifacts()
    print(get_estimated_price('1st Phase JP Nagar',1000, 2, 2))
    print(get_estimated_price('1st Phase JP Nagar',1000, 3, 3))