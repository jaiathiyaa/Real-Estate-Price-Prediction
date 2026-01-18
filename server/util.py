import json
import pickle
import os
import numpy as np

__locations = None
__data_columns = None
__model = None


def get_estimated_price(location, sqft, bhk, bath):
    if __model is None:
        raise Exception("Model not loaded. Call load_saved_artifacts() first.")

    if sqft < 300:
        raise ValueError("Total area too small for prediction")

    if bhk < 1 or bath < 1:
        raise ValueError("BHK and Bathroom must be at least 1")

    location = location.lower().strip()

    try:
        loc_index = __data_columns.index(location)
    except ValueError:
        loc_index = -1

    x = np.zeros(len(__data_columns))
    x[0] = sqft
    x[1] = bath
    x[2] = bhk

    if loc_index >= 0:
        x[loc_index] = 1

    price = __model.predict([x])[0]
    
    price = max(price,0)
    
    return round(price, 2)


def get_location_names():
    return __locations


def load_saved_artifacts():
    print("Loading saved artifacts...")

    global __data_columns
    global __locations
    global __model

    base_dir = os.path.dirname(os.path.abspath(__file__))

    columns_path = os.path.join(base_dir, "./artifacts/columns.json")
    model_path = os.path.join(base_dir, "./artifacts/banglore_home_prices_model.pickle")

    with open(columns_path, "r") as f:
        __data_columns = json.load(f)["data_columns"]
        __locations = __data_columns[3:]

    with open(model_path, "rb") as f:
        __model = pickle.load(f)

    print("Artifacts loaded successfully")


if __name__ == "__main__":
    print(get_location_names())
    print(get_estimated_price("whitefield", 1200, 2, 2))
