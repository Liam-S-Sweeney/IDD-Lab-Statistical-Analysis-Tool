import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats
from pandas.api.types import is_numeric_dtype

def explore_variable(variable):
    file_path = r'VT Teen Study Waves 1,2,3,4 merged all youth variables.csv'

    raw_df = pd.read_csv(file_path) 
    
    descriptive_dict = {
        # Variable Info
        'position': [],
        'variable_name': [],

        # Measures of Central Tendency
        'mean': [],
        'median': [],
        'mode': [],

        # Measures of Variability
        'var': [],
        'std': [],
        'range': [],
        'q1': [],
        'q3': [],
        'iqr': [],

        # Measures of Shape
        'skew': [],
        'kurtosis': [],

        # Measures of Frequency
        'count': [],
        'frequency': [],

        # Misc
        'min': [],
        'max': [],
        'se_mean': [],
    }
    
    numeric_df = raw_df.apply(pd.to_numeric, errors='coerce').replace(-99, np.nan)

    var_col = numeric_df[variable]
    non_na = var_col.dropna()
    values = non_na.to_numpy(dtype=float)
    non_na_array = np.array(non_na)


    descriptive_dict['position'].append(numeric_df.columns.get_loc(variable))
    descriptive_dict['variable_name'].append(variable)

    if non_na.empty:
        descriptive_dict['mean'].append(np.nan)
        descriptive_dict['median'].append(np.nan)
        descriptive_dict['mode'].append(np.nan)

        descriptive_dict['var'].append(np.nan)
        descriptive_dict['std'].append(np.nan)
        descriptive_dict['range'].append(np.nan)
        descriptive_dict['q1'].append(np.nan)
        descriptive_dict['q3'].append(np.nan)
        descriptive_dict['iqr'].append(np.nan)

        descriptive_dict['skew'].append(np.nan)
        descriptive_dict['kurtosis'].append(np.nan)

        descriptive_dict['count'].append(np.nan)
        descriptive_dict['frequency'].append(np.nan)

        descriptive_dict['min'].append(np.nan)
        descriptive_dict['max'].append(np.nan)
        descriptive_dict['se_mean'].append(np.nan)
    
    # Descriptive Computations
    else:
        # Measures of Central Tendency
        descriptive_dict['mean'].append(non_na.mean())
        descriptive_dict['median'].append(non_na.median())
        descriptive_dict['mode'].append(stats.mode(non_na_array))

        # Measures of Variability
        descriptive_dict['var'].append(non_na.var())
        descriptive_dict['std'].append(non_na.std())
        descriptive_dict['range'].append(non_na.max()-non_na.min())
        descriptive_dict['q1'].append(np.percentile(non_na, 25))
        descriptive_dict['q3'].append(np.percentile(non_na, 75))
        descriptive_dict['iqr'].append(np.percentile(non_na, 75)-np.percentile(non_na, 25))

        # Measures of Shape
        if values.size < 3 or np.isclose(values.std(ddof=0), 0.0, atol=1e-8):
            descriptive_dict['skew'].append(np.nan)
            descriptive_dict['kurtosis'].append(np.nan)    
        else:
            descriptive_dict['skew'].append(stats.skew(np.array(list(non_na))))
            descriptive_dict['kurtosis'].append(stats.kurtosis(np.array(list(non_na))))
        
        # Measures of Frequency
        n = len(non_na_array)
        unique_values, counts = np.unique(non_na_array, return_counts = True)
        frequencies_calc = counts/n * 100
        frequency_data = list(zip(unique_values, counts, frequencies_calc.astype(int)))
        frequency = f"Unique Value ; Counts : Frequeoncies | {frequency_data}"

        # Measures of Frequency | n; unique_val, count, percent
        descriptive_dict['count'].append(n)
        descriptive_dict['frequency'].append(frequency)

        # Misc
        descriptive_dict['min'].append(non_na.min())
        descriptive_dict['max'].append(non_na.max())
        descriptive_dict['se_mean'].append(non_na.std() / np.sqrt(n))

    descriptive_df = pd.DataFrame(descriptive_dict)

    try:
        descriptive_df.to_csv(f'{variable}_descriptive.csv', index=False)
    except:
        print("Error")   

def continuous_descriptive_visualizations(variable):
    # Histogram, Boxplot, Violin Plot, Dot Plot, Density Plot
    file_path = r'VT Teen Study Waves 1,2,3,4 merged all youth variables.csv'

    raw_df = pd.read_csv(file_path) 
    numeric_df = raw_df.apply(pd.to_numeric, errors='coerce')
    var_col = numeric_df[variable].replace(-99, np.nan)
    non_na = var_col.dropna()
    var = non_na.to_numpy(dtype=float)

    f, (ax_box, ax_hist, ax_violin, ax_dot, ax_density) = plt.subplots(5, sharex=True)

    sns.boxplot(x=var, ax=ax_box)
    sns.histplot(x=var, bins=12, kde=True, ax=ax_hist)
    sns.violinplot(x=var, ax=ax_violin)
    sns.swarmplot(x=var, ax=ax_dot)
    sns.kdeplot(x=var, ax=ax_density)

    ax_box.set(yticks=[])
    sns.despine(ax=ax_hist)
    sns.despine(ax=ax_box, left=True)
    sns.despine(ax=ax_violin)
    sns.despine(ax=ax_dot)
    sns.despine(ax=ax_density)

    f.suptitle(f"Continuous Data Visualization - {variable}", fontsize=16)
    plt.show()

def discrete_descriptive_visualizations(variable):
    # Bar Plot, Pie Chart
    file_path = r'VT Teen Study Waves 1,2,3,4 merged all youth variables.csv'

    raw_df = pd.read_csv(file_path) 
    numeric_df = raw_df.apply(pd.to_numeric, errors='coerce')
    var_col = numeric_df[variable].replace(-99, np.nan)
    non_na = var_col.dropna()
    var = non_na.to_numpy(dtype=float)

    f, (ax_bar, ax_pie) = plt.subplots(2, sharex=True)

    sns.boxplot(x=var, ax=ax_bar)
    sns.histplot(x=var, ax=ax_pie)

    ax_bar.set(yticks=[])
    sns.despine(ax=ax_bar)
    sns.despine(ax=ax_pie)

    f.suptitle(f'Discrete Descriptive Visualization - {variable}', fontsize=16)
    plt.show()