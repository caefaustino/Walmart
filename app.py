import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns
import plotly.express as px
import streamlit as st
import functions

from statsforecast import StatsForecast
from statsforecast.models import SeasonalNaive
from statsforecast.models import AutoARIMA

st.image('logo.jpeg')
st.title(':blue[Walmart Sales Forecast]')
st.write('This app will show stats about Walmart sales in US and forecast sales for the next 12 weeks.')
st.write('Please upload a CSV file:')
upload_file = st.file_uploader('Choose a file')
if upload_file is not None:
    df_input = pd.read_csv(upload_file)
    df_input = functions.prepare(df_input)
    st.dataframe(df_input.head(10), column_config={'Date': st.column_config.DatetimeColumn(format='YYYY MM DD')}, hide_index=True)
    st.header('General stats')
    fig = px.line(functions.TotalSales(df_input), x='Date', y='Weekly_Sales', title='Weekly Sales Over Time')
    st.plotly_chart(fig, use_container_width=True)
    st.subheader('Top-10 Stores based on total sales')
    st.dataframe(functions.top10(df_input), hide_index=True)
    st.subheader('Underperforming stores - sales below 1st quartile')
    st.dataframe(functions.bottom(df_input), hide_index=True)
    store_sales = df_input.groupby('Store')['Weekly_Sales'].sum().reset_index()
    store_sales = store_sales.sort_values(by='Weekly_Sales', ascending=False)
    store_sales = store_sales.rename(columns={'Weekly_Sales':'Total_Sales'})
    fig1 = px.bar(store_sales, x='Store', y='Total_Sales', title='Total Sales by Store')
    st.plotly_chart(fig1, use_container_width=True)
    st.subheader('See also weekly sales over time for each store')
    stores = int(df_input['Store'].max())
    store = st.number_input('Select store number', max_value=stores, step=1, format='%d')
    fig2 = px.line(df_input[(df_input['Store']==store)], x='Date', y='Weekly_Sales')
    st.plotly_chart(fig2, use_container_width=True)
    
    st.header('Forecasts sales for the next 12 weeks')
    
    st.subheader('All stores')
    df1_input = functions.prepare1(df_input)
    df1_input = df1_input.groupby('ds')['y'].sum().reset_index()
    df1_input.insert(0, 'unique_id', '99')
    fcst1 = functions.forecasts(df1_input)
    st.dataframe(fcst1, column_config={'Week': st.column_config.DatetimeColumn(format='YYYY MM DD'), 'Forecast': st.column_config.NumberColumn(format='%.2f', width='medium')}, hide_index=True)

    st.subheader('Store by store')
    option1 = st.slider('Select store number', min_value=1, max_value=stores, step=1, format='%d')
    df2_input = functions.prepare1(df_input)
    df2_input = df2_input[df2_input['unique_id'] == option1].reset_index(drop=True)
    fcst2 = functions.forecasts(df2_input)
    st.dataframe(fcst2, column_config={'Week': st.column_config.DatetimeColumn(format='YYYY MM DD'), 'Forecast': st.column_config.NumberColumn(format='%.2f')})