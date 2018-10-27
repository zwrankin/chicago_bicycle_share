import requests
import os
import pandas as pd

ZIP_DIR = '../raw/divvy/compressed'
INPUT_DIR = '../raw/divvy'

# HAVING TROUBLE WITH ACCESS
# url = 'https://amazonaws.com/divvy-data/Divvy_Trips_2018_Q2.zip'
# target_path = '../raw/2018_Q2.zip'
#
# response = requests.get(url, stream=True)
# handle = open(target_path, "wb")
# for chunk in response.iter_content(chunk_size=512):
#     if chunk:  # filter out keep-alive new chunks
#         handle.write(chunk)
# handle.close()


def unzip_divvy(zip_dir=ZIP_DIR, input_dir=INPUT_DIR):
    for f in os.listdir(zip_dir):
        with zipfile.ZipFile(os.path.join(zip_dir, f),"r") as zip_ref:
            zip_ref.extractall(input_dir)


def aggregate_trip_data(input_dir=INPUT_DIR):
    files = [os.path.join(input_dir, f) for f in os.listdir(input_dir) if 'Trips' in f]
    df = pd.concat([pd.read_csv(f) for f in files])
    return df


if __name__ == "__main__":
    unzip_divvy()