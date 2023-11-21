import pandas as pd
import numpy as np
import plotly.express as px

from statsforecast import StatsForecast
from statsforecast.models import AutoARIMA

# Convert Date to datetime
def prepare(df_in):
    df_in['Date'] = pd.to_datetime(df_in['Date'], format='%d-%m-%Y')
    return(df_in)

# Identify Top-10 stores based on total sales
def top10(df_in):
    store_sales = df_in.groupby('Store')['Weekly_Sales'].sum().reset_index()
    store_sales = store_sales.sort_values(by='Weekly_Sales', ascending=False)
    store_sales = store_sales.rename(columns={'Weekly_Sales':'Total_Sales'})
    store_sales = store_sales.head(10)
    return(store_sales)

# Total Weekly Sales Over Time
def TotalSales(df_in):
    total_weekly_sales = df_in.groupby('Date')['Weekly_Sales'].sum().reset_index()
    return(total_weekly_sales)

# Identify underperforming stores - Stores with sales below Q1
def bottom(df_in):
    store_sales = df_in.groupby('Store')['Weekly_Sales'].sum().reset_index()
    store_sales = store_sales.sort_values(by='Weekly_Sales', ascending=False)
    store_sales = store_sales.rename(columns={'Weekly_Sales':'Total_Sales'})
    q1 = np.quantile(store_sales['Total_Sales'], 0.25)
    store_sales = store_sales[(store_sales['Total_Sales'] < q1)].sort_values(by='Total_Sales')
    return(store_sales)

# Prepare dataset to StatsForecast
def prepare1(df_in):
    df_prep = df_in.drop(['Holiday_Flag', 'Temperature', 'Fuel_Price', 'CPI', 'Unemployment'], axis=1)
    df_prep = df_prep.rename(columns={'Store':'unique_id', 'Date':'ds' ,'Weekly_Sales':'y'})
    return(df_prep)

# Forecasts
def forecasts(df_in):
    models = [AutoARIMA()]
    sf = StatsForecast(models=models, freq='W', n_jobs=-1)
    fcst = sf.forecast(df=df_in, h=12)
    fcst.index.name='Store'
    fcst = fcst.rename(columns={'ds':'Week', 'AutoARIMA':'Forecast'})
    return(fcst)