
import logging
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import streamlit as st

# Setting up logging
logging.basicConfig(level=logging.INFO)

# Importing constants
from constants import (
    MARKET_DATA_TITLE,
    UPPER_BOLLINGER_BAND_DESCRIPTION,
    UPPER_BOLLINGER_BAND_USAGE,
    LOWER_BOLLINGER_BAND_DESCRIPTION,
    LOWER_BOLLINGER_BAND_USAGE,
    MA50_DESCRIPTION,
    MA50_USAGE,
    MA200_DESCRIPTION,
    MA200_USAGE,
    VOLUME_TRADED_TITLE,
    VOLUME_DESCRIPTION,
    VOLUME_USAGE,
    VWAP_DESCRIPTION,
    VWAP_USAGE,
    VOLATILITY_TITLE,
    VOLATILITY_DESCRIPTION,
    VOLATILITY_USAGE,
    MACD_ANALYSIS_TITLE,
    MACD_LINE_DESCRIPTION,
    MACD_LINE_USAGE,
    SIGNAL_LINE_DESCRIPTION,
    SIGNAL_LINE_USAGE,
)


def display_description_and_usage(description, usage):
    """Displays the description and usage information."""
    st.write(f"""
        Description: {description}
        Usage:
        - Buy: {usage['Buy']}
        - Sell: {usage['Sell']}
        - Risk/Opportunity Detection: {usage['Risk/Opportunity Detection']}
    """)


def market_data(df):
    """Visualizes market data using various indicators."""
    try:
        st.title(MARKET_DATA_TITLE)

        market_data_description = st.checkbox("Market Data Help")

        if market_data_description:
            display_description_and_usage(VWAP_DESCRIPTION, VWAP_USAGE)
            display_description_and_usage(UPPER_BOLLINGER_BAND_DESCRIPTION, UPPER_BOLLINGER_BAND_USAGE)
            display_description_and_usage(LOWER_BOLLINGER_BAND_DESCRIPTION, LOWER_BOLLINGER_BAND_USAGE)
            display_description_and_usage(MA50_DESCRIPTION, MA50_USAGE)
            display_description_and_usage(MA200_DESCRIPTION, MA200_USAGE)

        fig = make_subplots(rows=1, cols=1, shared_xaxes=True, subplot_titles=("Market Data",))

        fig.add_trace(go.Candlestick(
            x=df["time_period_start"], 
            open=df["price_open"], 
            high=df["price_high"], 
            low=df["price_low"], 
            close=df["price_close"], 
            name="Market data"))

        fig.add_trace(go.Scatter(x=df["time_period_start"], y=df["vwap"], mode="lines", name="Volume Weighted Average Price (VWAP)", line=dict(width=2, color="purple")))

        fig.add_trace(go.Scatter(x=df["time_period_start"], y=df["bollinger_upper"], marker=dict(color="blue"), line=dict(width=0.5), name="Upper Bollinger Band"))
        fig.add_trace(go.Scatter(x=df["time_period_start"], y=df["bollinger_lower"], marker=dict(color="red"), line=dict(width=0.5), name="Lower Bollinger Band"))

        fig.add_trace(go.Scatter(x=df["time_period_start"], y=df["ma50"], marker=dict(color="orange"), line=dict(width=0.5), name="50-period Moving Average"))
        fig.add_trace(go.Scatter(x=df["time_period_start"], y=df["ma200"], marker=dict(color="green"), line=dict(width=0.5), name="200-period Moving Average"))

        fig.update_layout(title="Bitcoin Candlestick Chart with Market Data", yaxis_title="Price (USD)")

        st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        logging.error(f"An error occurred while visualizing market data: {e}")
        st.write("An error occurred while visualizing market data. Please check the logs for more details.")


def volatility(df):
    """Visualizes the volatility of the market data."""
    try:
        st.title(VOLATILITY_TITLE)

        volatility_description = st.checkbox('Volatility Help')

        if volatility_description:
            display_description_and_usage(VOLATILITY_DESCRIPTION, VOLATILITY_USAGE)

        fig = make_subplots(rows=1, cols=1, shared_xaxes=True, subplot_titles=('Volatility Analysis',))

        fig.add_trace(go.Scatter(x=df['time_period_start'], y=df['volatility'], mode='lines', name='Volatility', line=dict(width=2, color='red')))

        fig.update_layout(title='Bitcoin Price Volatility Analysis', yaxis_title='Volatility (%)')

        st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        logging.error(f"An error occurred while visualizing volatility data: {e}")
        st.write("An error occurred while visualizing volatility data. Please check the logs for more details.")


def trade_velocity(df):
    """Visualizes the trade velocity based on volume traded."""
    try:
        st.title(VOLUME_TRADED_TITLE)

        volume_traded_description = st.checkbox('Volume Traded Help')

        if volume_traded_description:
            display_description_and_usage(VOLUME_DESCRIPTION, VOLUME_USAGE)

        fig = make_subplots(rows=1, cols=1, shared_xaxes=True, subplot_titles=('Volume Traded',))

        fig.add_trace(go.Bar(x=df['time_period_start'], y=df['volume_traded'], name='Volume Traded'))

        fig.update_layout(title='Bitcoin Volume Traded Analysis', yaxis_title='Volume')

        st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        logging.error(f"An error occurred while visualizing trade velocity data: {e}")
        st.write("An error occurred while visualizing trade velocity data. Please check the logs for more details.")


def rsi_and_macd(df):
    """Visualizes the RSI and MACD indicators."""
    try:
        st.title(MACD_ANALYSIS_TITLE)

        macd_description = st.checkbox('MACD Help')

        if macd_description:
            display_description_and_usage(MACD_LINE_DESCRIPTION, MACD_LINE_USAGE)
            display_description_and_usage(SIGNAL_LINE_DESCRIPTION, SIGNAL_LINE_USAGE)

        fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=('MACD Line and Signal Line', 'MACD Histogram'))

        fig.add_trace(go.Scatter(x=df['time_period_start'], y=df['macd'], mode='lines', name='MACD Line', line=dict(width=2, color='blue')), row=1, col=1)
        fig.add_trace(go.Scatter(x=df['time_period_start'], y=df['macd_signal'], mode='lines', name='Signal Line', line=dict(width=2, color='red')), row=1, col=1)
        fig.add_trace(go.Bar(x=df['time_period_start'], y=df['macd'] - df['macd_signal'], name='MACD Histogram'), row=2, col=1)

        fig.update_layout(title='Bitcoin Moving Average Convergence Divergence (MACD) Analysis', yaxis_title='MACD Value')

        st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        logging.error(f"An error occurred while visualizing RSI and MACD data: {e}")
        st.write("An error occurred while visualizing RSI and MACD data. Please check the logs for more details.")
