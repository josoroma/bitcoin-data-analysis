import logging
import requests
import pandas as pd
import streamlit as st
from constants import (
    COIN_API_ENDPOINT, 
    BITCOIN_DATA_ANALYSIS_TITLE, 
    TOOL_INVITATION_DESCRIPTION
)

from market_data_calculator import MarketDataCalculator
from data_retriever import DataRetriever
import prediction
import visualize

# Setting up logging
logging.basicConfig(filename='app.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def process_data(df):
    """Processes the data frame."""
    df = MarketDataCalculator.convert_to_datetime(df)
    df = calculate_market_metrics(df)
    return df

def calculate_market_metrics(df):
    """Calculates various market metrics."""
    df = MarketDataCalculator.calculate_market_data(df)
    df = MarketDataCalculator.calculate_volatility(df)
    df = MarketDataCalculator.calculate_trade_velocity(df)
    df = MarketDataCalculator.calculate_rsi(df)
    df = MarketDataCalculator.calculate_macd(df)
    return df

def visualize_data(df):
    """Visualizes the data using various visualization methods."""
    visualize.market_data(df)
    visualize.volatility(df)
    visualize.trade_velocity(df)
    visualize.rsi_and_macd(df)

def display_video():
    """Display WEBM Video."""
    video_file = open('app.webm', 'rb')
    video_bytes = video_file.read()
    st.video(video_bytes, format='video/webm')

def predict_data(api_key, period):
    limit = DataRetriever.set_limit(period)

    url = f"{COIN_API_ENDPOINT}?period_id={period}&limit={limit}"
    headers = {"X-CoinAPI-Key": api_key}

    data = DataRetriever.retrieve_data(url, headers)

    if isinstance(data, list) and data:
        df = pd.DataFrame(data)
        df = process_data(df)
        df = prediction.append_forecasted_data(df)
        return df
    else:
        st.write(f"Unexpected response format: {data}")
        return None

def main():
    # Creating the Streamlit UI
    st.title(BITCOIN_DATA_ANALYSIS_TITLE)
    st.write(TOOL_INVITATION_DESCRIPTION)

    display_video()

    col1, col2 = st.columns(2)

    # Setting API key input in column 1
    col1.markdown("### API Key")
    api_key = col1.text_input('Enter your CoinAPI.io API Key:', type='password')

    # Setting selectbox for choosing time period in column 2
    col2.markdown("### Time Period")
    period_options = ['1HRS', '4HRS', '12HRS']
    period = col2.selectbox('Select the time period:', period_options)

    if api_key:
        try:
            df = predict_data(api_key, period)
            if df is not None:
                visualize_data(df)
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            st.write(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
