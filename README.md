# chicago_bicycle_share
Using Chicago Divvy Bike Share Data for data visualization and Machine Learning practice

## D3 Visualization 
http://bl.ocks.org/zwrankin/26944952b0b6bcae78107abedec5498f
Interactive visualization of rides between stations using D3 and Leaflet. Check it out!
![Alt text](readme_images/d3_snip.JPG?raw=true "Sankey snip")

## Research Questions
#### 1) How can you predict usage of newly built stations?
Since Divvy creates new stations every year, it would be great to model usage before construction.
In the `2018_10_27_divvy_predict_station_usage.ipynb` notebook, I do so using a k-nearest neighbors model.
However, since station expansion is in new neighborhoods, existing geographic patterns are insufficient.
Next steps would include using other data sources such as the census and Yelp API to improve generalizability.  
![Alt text](readme_images/pdp_snip.JPG?raw=true "Partial Dependence Plot from k-nearest-neighbors model")

#### 2) How can you predict the imbalance of bikes among the Divvy stations?
One of the limitations of Divvy's station-based bikeshare model is that you must manually redistribute bikes
when the number of trips to and from a station are not balanced. 
As I show in the `2018_12_18_station_usage_imbalance.ipynb` notebook, only **2%** of stations have a daily imbalance 
of >5 bikes, and only 2 have imbalance of >20 bikes per day. That's less than I imaged (in Seattle, I watched bikes 
pile up at the bottom of hills). In Chicago, I think the bigger issue is the intra-day imbalance due to the daily 
commute. I showed in an old notebook (`2018_09_24_weather_and_ridership.ipynb`) that weather can predict ridership. 
Oddly, the imbalance is *smaller* in the summer, with no stations having daily imbalance of >20. 
At this time, the level of station imbalance does not merit a sophisticated model predicting daily imbalance. 
![Alt text](readme_images/imbalance_snip.JPG?raw=true "Stations with imbalance of >5 bikes per day to (blue) or from (red)")
![Alt text](readme_images/weather_snip.JPG?raw=true "SHAP values of random forest using weather to predict ridership")

 
 Predicting daily usage 
(using e.g. weather features) would be fun, but not the compelling logistical issue I intended to pursue. 
