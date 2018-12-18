import os
import numpy as np
import pandas as pd
import geojson
from .download_data import INPUT_DIR
from .utils import euclidian_distance, df_to_geojson


DATA_DIR = '../data/processed'


def process_trip_data(input_dir=INPUT_DIR):
    """Combine all trip csv files into one hdf"""
    files = [os.path.join(input_dir, f) for f in os.listdir(input_dir) if 'Trips' in f]
    df = pd.concat([load_and_standardize_divvy_dataset(f) for f in files])
    df['start_datetime'] = pd.to_datetime(df.start_time)
    df['end_datetime'] = pd.to_datetime(df.end_time)
    df.to_hdf(os.path.join(input_dir, 'trips.hdf'), key='trips')


def process_station_metadata(input_dir=INPUT_DIR, data_dir=DATA_DIR):

    # Hard-code latest station metadata
    df = pd.read_csv(os.path.join(input_dir, 'Divvy_Stations_2017_Q3Q4.csv'))
    df['online_datetime'] = pd.to_datetime(df.online_date)
    df['online_date'] = df.online_datetime.map(lambda x: x.strftime('%Y-%m-%d'))
    df['online_month'] = df.online_datetime.map(lambda x: x.strftime('%Y-%m'))
    df['online_year'] = df.online_datetime.map(lambda x: int(x.strftime('%Y')))
    # Duration online
    LAST_TRIP = pd.Timestamp('2018-06-30 23:59:56')
    df['online_duration'] = LAST_TRIP - df['online_datetime']
    df['online_duration_days'] = df.online_duration.astype(('timedelta64[D]'))


    # Calculate distance to nearest L station (for now, not line-specific)
    df_cta = load_cta_stations()
    df['distance_to_closest_L_station'] = df.apply(
        lambda x: min(euclidian_distance(x.latitude, df_cta.latitude, x.longitude, df_cta.longitude)), axis=1)

    # Add trip totals to station metadata
    df_trips = load_trip_data()
    trips_from = df_trips.groupby(['from_station_id']).trip_id.count().reset_index()
    trips_from = trips_from.rename(columns={'from_station_id': 'id', 'trip_id': 'trips_from_total'})
    df = pd.merge(df, trips_from)
    trips_to = df_trips.groupby(['to_station_id']).trip_id.count().reset_index()
    trips_to = trips_to.rename(columns={'to_station_id': 'id', 'trip_id': 'trips_to_total'})
    df = pd.merge(df, trips_to)
    df['trips_net_total'] = df.trips_to_total - df.trips_from_total
    # Daily trips
    df['trips_to_per_day'] = df.trips_to_total / df.online_duration_days
    df['trips_from_per_day'] = df.trips_from_total / df.online_duration_days
    df['trips_net_per_day'] = df.trips_net_total / df.online_duration_days

    df.to_hdf(os.path.join(data_dir, 'stations.hdf'), key='stations')


def save_daily_trip_data(input_dir=INPUT_DIR):
    pass
    # # Collapse trips by day
    # df_trips = load_trip_data()
    # # Merge station metadata
    # df_stations = load_station_metadata()
    # df = pd.merge(df_trips, df_stations, on=FILLMEIN)
    # # Save
    # df.to_hdf(os.path.join(input_dir, 'daily_trip_data.hdf'), key='daily_trip_data')


def load_daily_trip_data(data_dir=DATA_DIR):
    return pd.read_hdf(os.path.join(data_dir, 'daily_trip_data.hdf'))


def load_station_metadata(data_dir=DATA_DIR):
    return pd.read_hdf(os.path.join(data_dir, 'stations.hdf'))


def load_trip_data(data_dir=DATA_DIR):
    return pd.read_hdf(os.path.join(data_dir, 'trips.hdf'))


def load_cta_stations(input_dir=INPUT_DIR):
    return pd.read_hdf(os.path.join(input_dir, 'cta_stations.hdf'))


def process_sankey_data(data_dir=DATA_DIR):
    # Flows in csv format
    df = load_trip_data()
    df['trips'] = 1
    flows = df.groupby(['from_station_id', 'to_station_id'])['trips'].sum().reset_index()
    flows['target'] = flows.to_station_id.map(lambda s: 's' + str(s))
    flows['source'] = flows.from_station_id.map(lambda s: 's' + str(s))
    flows['flow'] = flows.trips
    flows[['target', 'source', 'flow']].to_csv(os.path.join(data_dir, 'sankey_rides_subset.csv'), index=False)

    # Station Totals in geojson format
    df_stations = load_station_metadata()
    df_stations['str_id'] = df_stations.id.map(lambda s: 's' + str(s))
    df_stations['trips'] = df_stations.trips_from_total
    df_stations['trips_per_day'] = df_stations.trips_from_per_day
    stations_geojson = df_to_geojson(df_stations, 'str_id', properties=['trips', 'trips_per_day'])
    with open(os.path.join(data_dir, 'stations.geojson'), 'w') as outfile:
        geojson.dump(stations_geojson, outfile)
    outfile.close()


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


if __name__ == "__main__":
    process_trip_data()
    process_station_metadata()
    save_daily_trip_data()
    process_sankey_data()
