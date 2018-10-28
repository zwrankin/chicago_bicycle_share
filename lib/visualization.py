import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import learning_curve
import folium

def plot_learning_curve(estimator, title, X, y, ylim=None, cv=None, scoring=None,
                        n_jobs=-1, train_sizes=np.linspace(.1, 1.0, 5)):
    """Generate a simple plot of the test and training learning curve"""
    plt.figure()
    plt.title(title)
    if ylim is not None:
        plt.ylim(*ylim)
    plt.xlabel("Training examples")
    plt.ylabel(f"Score ({scoring})")
    train_sizes, train_scores, test_scores = learning_curve(
        estimator, X, y, cv=cv, scoring=scoring, n_jobs=n_jobs, train_sizes=train_sizes)
    train_scores_mean = np.mean(train_scores, axis=1)
    train_scores_std = np.std(train_scores, axis=1)
    test_scores_mean = np.mean(test_scores, axis=1)
    test_scores_std = np.std(test_scores, axis=1)
    plt.grid()

    plt.fill_between(train_sizes, train_scores_mean - train_scores_std,
                     train_scores_mean + train_scores_std, alpha=0.1,
                     color="r")
    plt.fill_between(train_sizes, test_scores_mean - test_scores_std,
                     test_scores_mean + test_scores_std, alpha=0.1, color="g")
    plt.plot(train_sizes, train_scores_mean, 'o-', color="r",
             label="Training score")
    plt.plot(train_sizes, test_scores_mean, 'o-', color="g",
             label="Cross-validation score")

    plt.legend(loc="best")
    return plt


def map_stations(df, indicator: str):
    """
    Creates Folium map of chosen indicator with circle size corresponding to indicator value.
    :param df: pd.DataFrame with  Required columns: ['latitude', 'longitude', 'color', {indicator}]
    :param indicator: column name of value to plot
    :return:
    """

    REQUIRED_COLS = ['latitude', 'longitude', 'color', indicator]
    assert(all([col in df.columns for col in REQUIRED_COLS])), f'df is missing one or more of {REQUIRED_COLS}'

    m = folium.Map(location=[41.9, -87.6], zoom_start=11)
    for i in df.index:
        folium.Circle((df['latitude'][i], df['longitude'][i]), radius=str(df[indicator][i] * 20),
                      color=df['color'][i]).add_to(m)

    # Folium doesn't have good legend support, HMTL adapted from
    # https://medium.com/@bobhaffner/creating-a-legend-for-a-folium-map-c1e0ffc34373
    legend_html = '''
                    <div style="position: fixed; 
                                bottom: 500px; left: 500px; width: 100px; height: 90px; 
                                border:2px solid grey; z-index:9999; font-size:14px;
                                ">&nbsp; Year Built <br>
                                  &nbsp; 2015 &nbsp; <i class="fa fa-map-marker fa-2x" style="color:red"></i><br>
                                  &nbsp; <2015 &nbsp; <i class="fa fa-map-marker fa-2x" style="color:blue"></i>
                    </div>
                    '''
    m.get_root().html.add_child(folium.Element(legend_html))
    return m
