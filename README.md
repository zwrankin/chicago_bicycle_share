# chicago_bicycle_share
Using Chicago Divvy Bike Share Data for data visualization and Machine Learning practice, and build a predictive model 

## D3 Visualization 
http://bl.ocks.org/zwrankin/26944952b0b6bcae78107abedec5498f
Interactive visualization of rides between stations using D3 and Leaflet. Check it out!

## Feature importance practice
First, using pre-downloaded kaggle data, played around with some feature importance tools, 
including permutation importance, partial dependence plots, and SHAP values

See `/notebooks/2018_09_24_initial_data_exploration_and_models.ipynb`
- To download data, `kaggle datasets download -d yingwurenjian/chicago-divvy-bicycle-sharing-data`

## Prediction of station usage
Second, I downloaded records from 15 million Divvy rides from the website (https://www.divvybikes.com/system-data) 
built a k-nearest-neighbors algorithm to predict usage of new stations. See
`notebooks/2018_10_27_divvy_predict_station_usage.ipynb` for model and plots. 
- Future directions: use census data as non-spatial model components, and use Google Maps api to get distance and 
travel time matrix to get real-world spatial information on the stations (beyond just lat/long)

