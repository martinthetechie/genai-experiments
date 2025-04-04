import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
import ollama
import tempfile
import base64
import os

# Set up streamlit
st.set_page_config(layout='wide')
st.title('AI Technical Analystis Dashboard')
st.sidebar.header('Configs')

# Input for stock tracker and date range
ticker = st.sidebar.text_input('Enter the Stock Ticker (ie AAPL)')
start_date = st.sidebar.date_input('Start Date', value = pd.to_datetime('2023-02-01'))
end_date =  st.sidebar.date_input('End Date', value = pd.to_datetime('2024-04-03'))

# Fetch stock data
if st.sidebar.button('Fetch Data'):
    st.session_state['stock_data'] = yf.download(ticker,start=start_date, end=end_date)
    st.success('Stock Data Loaded')

if 'stock_data' in st.session_state:
    data = st.session_state['stock_data']
    fig = go.Figure(
        x=data.index,
        open=data['Open'],
        high=data['High'],
        low=data['Low'],
        close=data['Close'],
        name='Candlestick'
    )

# Select technical indicators to show
st.sidebar.subheader('Technical Indicators')
indicators = st.sidebar.multiselect(
    'Select Indicators:',
    ['20-Day SMA', '20-Day EMA', '20 Day Bollinger Bands', 'VWAP'],
    defualt = ['20-Day SMA']
)

# Helper functions to add indicators
def add_indicator(indicator):
    
# Add selected indicators to the charts
for indicator in indicators:
    add_indicator(indicator)











