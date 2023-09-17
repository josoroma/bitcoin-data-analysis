import streamlit as st

from plotly.subplots import make_subplots
import plotly.graph_objects as go

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
    SIGNAL_LINE_USAGE
)

class Visualize:
    def __init__(self):
        pass

    @staticmethod
    def visualize_market_data(df):
        st.title(MARKET_DATA_TITLE)

        market_data_description = st.checkbox('Market Data Help')
        
        if market_data_description:
            st.write(f"""
                Description: {VWAP_DESCRIPTION}
                Usage:
                - Buy: {VWAP_USAGE['Buy']}
                - Sell: {VWAP_USAGE['Sell']}
                - Risk/Opportunity Detection: {VWAP_USAGE['Risk/Opportunity Detection']}
                """)
            
            st.write(f"""
                Description: {UPPER_BOLLINGER_BAND_DESCRIPTION}
                Usage:
                - Buy: {UPPER_BOLLINGER_BAND_USAGE['Buy']}
                - Sell: {UPPER_BOLLINGER_BAND_USAGE['Sell']}
                - Risk/Opportunity Detection: {UPPER_BOLLINGER_BAND_USAGE['Risk/Opportunity Detection']}
                """)

            st.write(f"""
                Description: {LOWER_BOLLINGER_BAND_DESCRIPTION}
                Usage:
                - Buy: {LOWER_BOLLINGER_BAND_USAGE['Buy']}
                - Sell: {LOWER_BOLLINGER_BAND_USAGE['Sell']}
                - Risk/Opportunity Detection: {LOWER_BOLLINGER_BAND_USAGE['Risk/Opportunity Detection']}
                """)

            st.write(f"""
                Description: {MA50_DESCRIPTION}
                Usage:
                - Buy: {MA50_USAGE['Buy']}
                - Sell: {MA50_USAGE['Sell']}
                - Risk/Opportunity Detection: {MA50_USAGE['Risk/Opportunity Detection']}
                """)

            st.write(f"""
                Description: {MA200_DESCRIPTION}
                Usage:
                - Buy: {MA200_USAGE['Buy']}
                - Sell: {MA200_USAGE['Sell']}
                - Risk/Opportunity Detection: {MA200_USAGE['Risk/Opportunity Detection']}
                """)

        fig = make_subplots(rows=1, cols=1, shared_xaxes=True, subplot_titles=('Market Data',))
        
        fig.add_trace(go.Candlestick(
            x=df['time_period_start'], 
            open=df['price_open'], 
            high=df['price_high'], 
            low=df['price_low'], 
            close=df['price_close'], 
            name='Market data'))
        
        fig.add_trace(go.Scatter(x=df['time_period_start'], y=df['vwap'], mode='lines', name='Volume Weighted Average Price (VWAP)', line=dict(width=2, color='purple')))
        
        fig.add_trace(go.Scatter(x=df['time_period_start'], y=df['bollinger_upper'], marker=dict(color='blue'), line=dict(width=0.5), name='Upper Bollinger Band'))
        fig.add_trace(go.Scatter(x=df['time_period_start'], y=df['bollinger_lower'], marker=dict(color='red'), line=dict(width=0.5), name='Lower Bollinger Band'))

        fig.add_trace(go.Scatter(x=df['time_period_start'], y=df['ma50'], marker=dict(color='orange'), line=dict(width=0.5), name='50-period Moving Average'))
        fig.add_trace(go.Scatter(x=df['time_period_start'], y=df['ma200'], marker=dict(color='green'), line=dict(width=0.5), name='200-period Moving Average'))

        fig.update_layout(title='Bitcoin Candlestick Chart with Market Data', yaxis_title='Price (USD)')
            
        st.plotly_chart(fig, use_container_width=True)

    @staticmethod
    def visualize_volatility(df):
        st.title(VOLATILITY_TITLE)
        
        volatility_description = st.checkbox('Volatility Help')
        
        if volatility_description:
            st.write(f"""
            Description: {VOLATILITY_DESCRIPTION}
            Usage:
            - Buy: {VOLATILITY_USAGE['Buy']}
            - Sell: {VOLATILITY_USAGE['Sell']}
            - Risk/Opportunity Detection: {VOLATILITY_USAGE['Risk/Opportunity Detection']}
            """)
        
        fig = make_subplots(rows=1, cols=1, shared_xaxes=True, subplot_titles=('Volatility Analysis',))
        
        fig.add_trace(go.Scatter(x=df['time_period_start'], y=df['volatility'], mode='lines', name='Volatility', line=dict(width=2, color='red')))
        
        fig.update_layout(title='Bitcoin Price Volatility Analysis', yaxis_title='Volatility (%)')
        
        st.plotly_chart(fig, use_container_width=True)

    @staticmethod
    def visualize_trade_velocity(df):
        st.title(VOLUME_TRADED_TITLE)

        volume_traded_description = st.checkbox('Volume Traded Help')
        
        if volume_traded_description:
            st.title(VOLUME_TRADED_TITLE)
            st.write(f"""
            Description: {VOLUME_DESCRIPTION}
            Usage:
            - Buy: {VOLUME_USAGE['Buy']}
            - Sell: {VOLUME_USAGE['Sell']}
            - Risk/Opportunity Detection: {VOLUME_USAGE['Risk/Opportunity Detection']}
            """)
        
        fig = make_subplots(rows=1, cols=1, shared_xaxes=True, subplot_titles=('Volume Traded',))
        
        fig.add_trace(go.Bar(x=df['time_period_start'], y=df['volume_traded'], name='Volume Traded'))
        
        fig.update_layout(title='Bitcoin Volume Traded Analysis', yaxis_title='Volume')
        
        st.plotly_chart(fig, use_container_width=True)

    @staticmethod
    def visualize_rsi_and_macd(df):
        st.title(MACD_ANALYSIS_TITLE)
        
        macd_description = st.checkbox('MACD Help')
        
        if macd_description:
            st.write(f"""
                Description: {MACD_LINE_DESCRIPTION}
                Usage:
                - Buy: {MACD_LINE_USAGE['Buy']}
                - Sell: {MACD_LINE_USAGE['Sell']}
                - Risk/Opportunity Detection: {MACD_LINE_USAGE['Risk/Opportunity Detection']}
                """)

            st.write(f"""
                Description: {SIGNAL_LINE_DESCRIPTION}
                Usage:
                - Buy: {SIGNAL_LINE_USAGE['Buy']}
                - Sell: {SIGNAL_LINE_USAGE['Sell']}
                - Risk/Opportunity Detection: {SIGNAL_LINE_USAGE['Risk/Opportunity Detection']}
                """)
        
        fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=('MACD Line and Signal Line', 'MACD Histogram'))
        
        fig.add_trace(go.Scatter(x=df['time_period_start'], y=df['macd'], mode='lines', name='MACD Line', line=dict(width=2, color='blue')), row=1, col=1)
        fig.add_trace(go.Scatter(x=df['time_period_start'], y=df['macd_signal'], mode='lines', name='Signal Line', line=dict(width=2, color='red')), row=1, col=1)
        fig.add_trace(go.Bar(x=df['time_period_start'], y=df['macd'] - df['macd_signal'], name='MACD Histogram'), row=2, col=1)
        
        fig.update_layout(title='Bitcoin Moving Average Convergence Divergence (MACD) Analysis', yaxis_title='MACD Value')
        
        st.plotly_chart(fig, use_container_width=True)
