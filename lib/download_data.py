import requests
import os
import shutil
import pandas as pd
import zipfile

ZIP_DIR = '../raw/divvy/compressed'
INPUT_DIR = '../raw/divvy'

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


def load_and_standardize_divvy_dataset(filepath):
    """Ensure standard columns across different data"""
    colnames = ['trip_id', 'start_time', 'end_time', 'bikeid', 'tripduration',
                'from_station_id', 'from_station_name', 'to_station_id',
                'to_station_name', 'usertype', 'gender', 'birthyear']
    df = pd.read_csv(filepath)
    # Divvy_Trips_2018_Q1 has different column names (but the same data)
    if 'Divvy_Trips_2018_Q1' in filepath:
        df.columns = colnames
    df.rename(index=str, columns={"starttime": "start_time", "stoptime": "end_time", "birthday": "birthyear",},
              inplace=True)
    assert all([col in colnames for col in df.columns]), 'Check column name consistency'
    return df[colnames]  # standardize column order for safety


def aggregate_trip_data(input_dir=INPUT_DIR, save=True):
    """Combine all trip csv files into one hdf"""
    files = [os.path.join(input_dir, f) for f in os.listdir(input_dir) if 'Trips' in f]
    df = pd.concat([load_and_standardize_divvy_dataset(f) for f in files])
    df['start_datetime'] = pd.to_datetime(df.start_time)
    if save:
        df.to_hdf(os.path.join(input_dir, 'trips.hdf'), key='trips')
    else:
        return df


def load_trip_data(input_dir=INPUT_DIR):
    return pd.read_hdf(os.path.join(input_dir, 'trips.hdf'))


def load_station_data(input_dir=INPUT_DIR):
    """Loads the most recent station metadata"""
    df = pd.read_csv(os.path.join(input_dir, 'Divvy_Stations_2017_Q3Q4.csv'))
    df['online_datetime'] = pd.to_datetime(df.online_date)
    df['online_date'] = df.online_datetime.map(lambda x: x.strftime('%Y-%m-%d'))
    df['online_month'] = df.online_datetime.map(lambda x: x.strftime('%Y-%m'))
    df['online_year'] = df.online_datetime.map(lambda x: int(x.strftime('%Y')))
    return df


if __name__ == "__main__":
    download_divvy()
    unzip_divvy()
    standardize_unzipped_files()
    aggregate_trip_data()  # I think the datetime is actually the slowest part
