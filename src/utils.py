import numpy as np
from sklearn.model_selection import KFold

kfold = KFold(n_splits=3, random_state=10)


def report_cv_scores(results, n_top=3):
    for i in range(1, n_top + 1):
        candidates = np.flatnonzero(results['rank_test_score'] == i)
        for candidate in candidates:
            print("Model with rank: {0}".format(i))
            print("Mean validation score: {0:.3f} (std: {1:.3f})".format(
                  results['mean_test_score'][candidate],
                  results['std_test_score'][candidate]))
            print("Parameters: {0}".format(results['params'][candidate]))
            print("")


def df_to_geojson(df, identifier, properties, lat='latitude', lon='longitude'):
    """Adapted from https://geoffboeing.com/2015/10/exporting-python-data-geojson/"""
    geojson = {'type':'FeatureCollection', 'features':[]}
    for _, row in df.iterrows():
        feature = {'type':'Feature',
                   'id': row[identifier],
                   'properties':{},
                   'geometry':{'type':'Point',
                               'coordinates':[]}}
        feature['geometry']['coordinates'] = [row[lon],row[lat]]  # recall that geojson is cartesian (ie, NOT lat-long)
        for prop in properties:
            feature['properties'][prop] = row[prop]
        geojson['features'].append(feature)
    return geojson
