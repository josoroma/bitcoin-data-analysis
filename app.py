import logging
import requests
import pandas as pd
import streamlit as st

from constants import COIN_API_ENDPOINT, BITCOIN_DATA_ANALYSIS_TITLE, TOOL_INVITATION_DESCRIPTION
from market_data_calculator import MarketDataCalculator
from data_retriever import DataRetriever
import prediction
import visualize

# Logging setup
logging.basicConfig(
    filename='app.log', 
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


def apply_market_calculations(df, calculations):
    """Applies a series of market calculations on the DataFrame."""
    for calculation in calculations:
        df = calculation(df)
    return df


def visualize_data(df):
    """Visualizes the market data using various methods."""
    visualize.market_data(df)
    visualize.volatility(df)
    visualize.trade_velocity(df)
    visualize.rsi_and_macd(df)


def display_video():
    """Displays a WEBM video."""
    with open('app.webm', 'rb') as video_file:
        st.video(video_file.read(), format='video/webm')


def fetch_and_predict_data(api_key, period):
    limit = DataRetriever.set_limit(period)
    url = f"{COIN_API_ENDPOINT}?period_id={period}&limit={limit}"
    headers = {"X-CoinAPI-Key": api_key}

    data = DataRetriever.retrieve_data(url, headers)

    if isinstance(data, list) and data:
        df = pd.DataFrame(data)
        calculations = [
            MarketDataCalculator.convert_to_datetime,
            MarketDataCalculator.calculate_market_data,
            MarketDataCalculator.calculate_volatility,
            MarketDataCalculator.calculate_trade_velocity,
            MarketDataCalculator.calculate_rsi,
            MarketDataCalculator.calculate_macd
        ]
        df = apply_market_calculations(df, calculations)
        df = prediction.append_forecasted_data(df)
        return df
    else:
        st.write(f"Unexpected response format: {data}")
        return None


def main():
    st.title(BITCOIN_DATA_ANALYSIS_TITLE)
    st.write(TOOL_INVITATION_DESCRIPTION)
    display_video()

    col1, col2 = st.columns(2)

    api_key = col1.text_input('Enter your CoinAPI.io API Key:', type='password')
    period = col2.selectbox('Select the time period:', ['1HRS', '4HRS', '12HRS'])

    if api_key:
        try:
            df = fetch_and_predict_data(api_key, period)
            if df is not None:
                visualize_data(df)
        except requests.RequestException as e:
            logging.error(f"Request error: {e}")
            st.write(f"Request error: {e}")
        except Exception as e:
            logging.error(f"An unknown error occurred: {e}")
            st.write(f"An unknown error occurred: {e}")


if __name__ == "__main__":
    main()
