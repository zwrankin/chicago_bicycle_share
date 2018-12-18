import requests
import os
import shutil
import numpy as np
import pandas as pd
import zipfile
from sodapy import Socrata

ZIP_DIR = '../data/raw/divvy/compressed'
INPUT_DIR = '../data/raw/divvy'

# https://www.divvybikes.com/system-data
def download_divvy():
    pass
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


def standardize_unzipped_files(input_dir=INPUT_DIR):
    """Some get unzipped into folders, move all into input_dir"""
    dirs = next(os.walk(input_dir))[1]
    trip_dirs = [d for d in dirs if 'Trips' in d]
    for trip_dir in trip_dirs:
        files = os.listdir(os.path.join(input_dir, trip_dir))
        for file in files:
            source = os.path.join(input_dir, trip_dir, file)
            destination = os.path.join(input_dir, file)
            shutil.copy(source, destination)
        shutil.rmtree(os.path.join(input_dir, trip_dir))


def unzip_divvy(zip_dir=ZIP_DIR, input_dir=INPUT_DIR):
    """Unzip all data and move to input_dir"""
    for f in os.listdir(zip_dir):
        with zipfile.ZipFile(os.path.join(zip_dir, f),"r") as zip_ref:
            zip_ref.extractall(input_dir)


def query_cta_stations(input_dir=INPUT_DIR, save=True):
    """
    Loads some data from Chicago L (metro) stations using Socrata Open API (SODA)
    Data and API documentation available at
    https://data.cityofchicago.org/Transportation/CTA-System-Information-List-of-L-Stops/8pix-ypme
    """
    # Unauthenticated client only works with public data sets. Note 'None'
    # in place of application token, and no username or password:
    client = Socrata("data.cityofchicago.org", None)

    # Example authenticated client (needed for non-public datasets):
    # client = Socrata(data.cityofchicago.org,
    #                  MyAppToken,
    #                  userame="user@example.com",
    #                  password="AFakePassword")

    # First 2000 results, returned as JSON from API / converted to Python list of
    # dictionaries by sodapy.
    results = client.get("8mj8-j3c4", limit=2000)

    # Convert to pandas DataFrame
    df = pd.DataFrame.from_records(results)
    df['latitude'] = df.location.map(lambda x: x['coordinates'][1])
    df['longitude'] = df.location.map(lambda x: x['coordinates'][0])
    if save:
        df.to_hdf(os.path.join(input_dir, 'cta_stations.hdf'), key='cta_stations')
    else:
        return df


if __name__ == "__main__":
    download_divvy()
    unzip_divvy()
    standardize_unzipped_files()
    query_cta_stations()
