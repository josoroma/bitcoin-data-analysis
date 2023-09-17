import streamlit as st
import requests
import pandas as pd

from calculate import Calculate
from visualize import Visualize
from prediction import Prediction

from constants import (COIN_API_ENDPOINT, BITCOIN_DATA_ANALYSIS_TITLE, TOOL_INVITATION_DESCRIPTION)

class BitcoinDataAnalysis:
    def __init__(self, api_key, period='1HRS'):
        self.period = period
        self.limit = self.set_limit(period)
        self.url = f"{COIN_API_ENDPOINT}?period_id={self.period}&limit={self.limit}"
        self.headers = {
            "X-CoinAPI-Key": api_key
        }
        
        self.data = None
        self.df = None
        self.visualize = Visualize()

    def set_limit(self, period):
        if period == '4HRS':
            return ((24 // 4) * 30) + (24 * 7)  # one month + one week more
        elif period == '12HRS':
            return ((24 // 12) * 90) + (24 * 7)   # three months + one week more
        else:
            return (24 * 7) * 2  # one week + one week more

    def retrieve_data(self):
        try:
            response = requests.get(self.url, headers=self.headers)
            response.raise_for_status()
            self.data = response.json()

            if isinstance(self.data, list) and self.data:
                self.df = pd.DataFrame(self.data)
                # st.subheader("Historical Data")
                # st.dataframe(self.df)
                self.process_data()
                # st.subheader("Processed Data")
                # st.dataframe(self.df)
                self.df = Prediction.append_forecasted_data_using_sklearn_linear_regression_dataset_with_training_testing_set(self.df)
                # st.subheader("Predicted Data")
                # st.dataframe(self.df)
            else:
                st.write(f"Unexpected response format: {self.data}")
        except requests.exceptions.RequestException as e:
            st.write(f"Error fetching data: {e}")
            self.df = None

    def process_data(self):
        self.df['time_period_start'] = pd.to_datetime(self.df['time_period_start'])
        self.df['time_open'] = pd.to_datetime(self.df['time_open'])
        self.df['time_close'] = pd.to_datetime(self.df['time_close'])
        self.df = Calculate.calculate_market_data(self.df)
        self.df = Calculate.calculate_volatility(self.df)
        self.df = Calculate.calculate_trade_velocity(self.df)
        self.df = Calculate.calculate_rsi_and_macd(self.df)

if __name__ == "__main__":
    # Creating the Streamlit UI
    # st.set_page_config(layout="wide")
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

    # Store the current API key and period in the session state
    if 'current_api_key' not in st.session_state:
        st.session_state['current_api_key'] = None
    if 'current_period' not in st.session_state:
        st.session_state['current_period'] = None

    # Create an instance of the BitcoinDataAnalysis class if the API key or period has changed
    if api_key and (api_key != st.session_state['current_api_key'] or period != st.session_state['current_period']):
        try:
            st.session_state['btc_data_analysis'] = BitcoinDataAnalysis(api_key, period)
            st.session_state['btc_data_analysis'].retrieve_data()
        except Exception as e:
            st.write(f"An error occurred: {e}")

        # Update the current API key and period in the session state
        st.session_state['current_api_key'] = api_key
        st.session_state['current_period'] = period

    # Checking if the instance exists and data is retrieved, and then calling the visualization methods
    if st.session_state.get('btc_data_analysis') and st.session_state['btc_data_analysis'].df is not None:
        st.session_state['btc_data_analysis'].visualize.visualize_market_data(st.session_state['btc_data_analysis'].df)
        st.session_state['btc_data_analysis'].visualize.visualize_volatility(st.session_state['btc_data_analysis'].df)
        st.session_state['btc_data_analysis'].visualize.visualize_trade_velocity(st.session_state['btc_data_analysis'].df)
        st.session_state['btc_data_analysis'].visualize.visualize_rsi_and_macd(st.session_state['btc_data_analysis'].df)