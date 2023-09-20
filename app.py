import logging
import requests
import pandas as pd
import streamlit as st
from constants import (
    COIN_API_ENDPOINT, 
    BITCOIN_DATA_ANALYSIS_TITLE, 
    TOOL_INVITATION_DESCRIPTION
)
from calculate import (
    calculate_market_data, 
    calculate_volatility, 
    calculate_trade_velocity, 
    calculate_rsi, 
    calculate_macd
)
import prediction
import visualize

# Setting up logging
logging.basicConfig(filename='app.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def set_limit(period):
    """Sets the limit based on the period."""
    if period == "4HRS":
        return ((24 // 4) * 30) + (24 * 7)  # one month + one week more
    elif period == "12HRS":
        return ((24 // 12) * 90) + (24 * 7)   # three months + one week more
    else:
        return (24 * 7) * 2  # one week + one week more

def retrieve_data(url, headers):
    """Retrieves data from the API."""
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.HTTPError as http_err:
        logging.error(f"HTTP error occurred: {http_err}")
        st.write(f"HTTP error occurred: {http_err}")
        return None
    except requests.exceptions.ConnectionError as conn_err:
        logging.error(f"Connection error occurred: {conn_err}")
        st.write(f"Connection error occurred: {conn_err}")
        return None
    except requests.exceptions.RequestException as req_err:
        logging.error(f"Error fetching data: {req_err}")
        st.write(f"Error fetching data: {req_err}")
        return None

    data = response.json()
    if isinstance(data, list) and data:
        df = pd.DataFrame(data)
        df = process_data(df)
        df = prediction.append_forecasted_data(df)
        return df
    else:
        st.write(f"Unexpected response format: {data}")
        return None

def process_data(df):
    """Processes the data frame."""
    df = convert_to_datetime(df)
    df = calculate_market_metrics(df)
    return df

def convert_to_datetime(df):
    """Converts specific columns to datetime format."""
    df['time_period_start'] = pd.to_datetime(df['time_period_start'])
    df['time_open'] = pd.to_datetime(df['time_open'])
    df['time_close'] = pd.to_datetime(df['time_close'])
    return df

def calculate_market_metrics(df):
    """Calculates various market metrics."""
    df = calculate_market_data(df)
    df = calculate_volatility(df)
    df = calculate_trade_velocity(df)
    df = calculate_rsi(df)
    df = calculate_macd(df)
    return df

def visualize_data(df):
    """Visualizes the data using various visualization methods."""
    visualize.visualize_market_data(df)
    visualize.visualize_volatility(df)
    visualize.visualize_trade_velocity(df)
    visualize.visualize_rsi_and_macd(df)

def main():
    # Creating the Streamlit UI
    st.title(BITCOIN_DATA_ANALYSIS_TITLE)
    st.write(TOOL_INVITATION_DESCRIPTION)

    video_file = open('app.webm', 'rb')
    video_bytes = video_file.read()
    st.video(video_bytes, format='video/webm')

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
            limit = set_limit(period)  # Corrected here
            url = f"{COIN_API_ENDPOINT}?period_id={period}&limit={limit}"
            headers = {"X-CoinAPI-Key": api_key}
            df = retrieve_data(url, headers)
            if df is not None:
                visualize_data(df)
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            st.write(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
