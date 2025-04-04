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
ticker = st.sidebar.text_input('Enter the Stock Ticker (ie AAPL)',value = 'AAPL')
start_date = st.sidebar.date_input('Start Date', value = pd.to_datetime('2024-02-01'))
end_date =  st.sidebar.date_input('End Date', value = pd.to_datetime('2025-04-03'))

# Fetch stock data
if st.sidebar.button('Fetch Data'):
    try:
        data = yf.download(ticker, start=start_date, end=end_date, progress=False)
        if data.empty:
            st.error("No data returned. Please check the ticker symbol or date range.")
        else:
            st.session_state['stock_data'] = data
            st.success('Stock Data Loaded')
    except Exception as e:
        st.error(f"Failed to fetch data: {e}")

if 'stock_data' in st.session_state:
    data = st.session_state['stock_data'] 
    fig = go.Figure(
        data=[
            go.Candlestick(
                x=data.index,
                open=data['Open'],
                high=data['High'],
                low=data['Low'],
                close=data['Close'],
                name='Candlestick'
            )
        ]
    )
    st.write(data.head())

    # Select technical indicators to show
    st.sidebar.subheader('Technical Indicators')
    indicators = st.sidebar.multiselect(
        'Select Indicators:',
        ['20-Day SMA', '20-Day EMA', '20 Day Bollinger Bands', 'VWAP'],
        default = ['20-Day SMA']
    )

    # Helper functions to add indicators
    def add_indicator(indicator):
        if indicator == '20-Day SMA':
            # 20 Day SMA Eqn
            sma = data['Close'].rolling(window=20).mean()
            fig.add_trace(go.Scatter(x=data.index,y=sma ,mode='lines',name='SMA (20)'))
            print(sma)
        elif indicator == '20-Day EMA':
            # 20 Day EMA Eqn
            ema = data['Close'].ewm(span=20).mean()
            fig.add_trace(go.Scatter(x=data.index, y= ema, mode='lines', name='EMA (20)'))
        elif indicator == '20-Day Bollinger Bands':
            # 20 Day Bollinger Bands Eqn
            sma = data['Close'].rolling(window=20).mean()
            std = data['Close'].rolling(window=20).std
            upper_bb = sma + 2 * std
            lower_bb = sma - 2 * std
            fig.add_trace(go.Scatter(x=data.index, y= upper_bb, mode='lines', name='Upper BB'))
            fig.add_trace(go.Scatter(x=data.index, y= lower_bb, mode='lines', name='Lower BB'))
        elif indicator == '20-Day VWAP':
            # 20 Day VWAP Eqn
            vwap = data['Close'] * data['Volume'].cumsum() / data['Volume'].cumsum()
            fig.add_trace(go.Scatter(x=data.index, y= vwap, mode='lines', name='VWAP'))


    # Add selected indicators to the charts
    for indicator in indicators:
        add_indicator(indicator)

    fig.update_layout(xaxis_rangeslider_visible=False)
    st.plotly_chart(fig)

# Analyze technical charts with LLaMA 3.2 Vision
st.subheader('AI Technical Analysis')
if st.button('Run AI Analysis'):
    # Save chart as temp image
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmpfile:
        fig.write_image(tmpfile.name)
        tmpfile_path = tmpfile.name
    with open(tmpfile_path, "rb") as image_file:
        image_data = base64.b64encode(image_file.read()).decode('utf-8')

    # AI Analysis Request
    messages = [{
        'role':'user',
        'content':""" You are a Stock Trader specializing in Technical Analysis at a top financial institution.
                      Analyze the stock chart's technical indicators and provide a buy/hold/sell recommendation.
                      Firt provide the recommendation and then provide the detailed reasoning.
        """,
        'images': image_data
    }]
    response = ollama.chat(model='llama3.2-vision', messages=messages)
    
    st.write('AI Technical Insights')
    st.write(response)

    # Clean up temp file
    # os.remove(tmpfile_path)










