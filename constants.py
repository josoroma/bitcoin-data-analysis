COIN_API_ENDPOINT = "https://rest.coinapi.io/v1/ohlcv/BITSTAMP_SPOT_BTC_USD/latest"

BITCOIN_DATA_ANALYSIS_TITLE = "Bitcoin Data Analysis"

TOOL_INVITATION_DESCRIPTION = """
This is a tool designed to provide you with expert predictions on critical market trends and trading volumes.

Through an interactive and user-friendly interface, you can seamlessly navigate between historical and forecasted data, enabling you to formulate strategies with precision and confidence.

Step into a realm where informed decisions pave the way to successful investments, and where your foresight is your greatest asset.
"""

MARKET_DATA_TITLE = "Market Data Analysis"

UPPER_BOLLINGER_BAND_DESCRIPTION = """
The Upper Bollinger Band is a volatility indicator which is calculated as two standard deviations above the 20-period moving average of the closing prices. It helps in identifying overbought conditions in the market.
"""

UPPER_BOLLINGER_BAND_USAGE = {
    "Buy": "A common strategy is to buy when the price touches or crosses below the upper band and then starts moving back towards it, indicating potential upward momentum.",
    "Sell": "Traders often sell when the price touches or crosses above the upper band and starts to reverse, indicating potential downward momentum.",
    "Risk/Opportunity Detection": "The Upper Bollinger Band can be used to detect increased volatility and potential reversal points in the market. It can signal opportunities for profit-taking or reducing exposure."
}

LOWER_BOLLINGER_BAND_DESCRIPTION = """
The Lower Bollinger Band is calculated as two standard deviations below the 20-period moving average of the closing prices, serving as an indicator for oversold conditions in the market.
"""

LOWER_BOLLINGER_BAND_USAGE = {
    "Buy": "Traders might consider buying when the price touches or crosses above the lower band and starts to move back up, indicating potential recovery.",
    "Sell": "Selling is often considered when the price crosses below the lower band and fails to recover, indicating a potential further decline.",
    "Risk/Opportunity Detection": "The Lower Bollinger Band helps in identifying periods of low volatility where the market might be consolidating before the next big move."
}

MA50_DESCRIPTION = """
The 50-period moving average is a trend-following indicator that smoothens price data over the last 50 periods to identify medium-term trends.
"""

MA50_USAGE = {
    "Buy": "A common strategy is to buy when the price crosses above the 50-period moving average, indicating a potential uptrend.",
    "Sell": "Consider selling when the price crosses below the 50-period moving average, suggesting a potential downtrend.",
    "Risk/Opportunity Detection": "The 50-period moving average can be used to identify areas of support or resistance, helping traders to identify potential entry or exit points."
}

MA200_DESCRIPTION = """
The 200-period moving average serves as a long-term trend indicator, smoothing price data over the last 200 periods to help identify the prevailing market trend.
"""

MA200_USAGE = {
    "Buy": "Traders often buy when the price crosses above the 200-period moving average, signaling the beginning of a long-term uptrend.",
    "Sell": "Selling is considered when the price crosses below the 200-period moving average, indicating a potential long-term downtrend.",
    "Risk/Opportunity Detection": "The 200-period moving average is often used as a dynamic support or resistance level. It can help in identifying major trend reversals and market sentiment shifts."
}

VOLUME_TRADED_TITLE = "Volume Traded"

VOLUME_DESCRIPTION = """
The graph visualizes the volume of Bitcoin traded over time, offering insights into market activity and potential trends. Analyzing trading volume can help traders understand the strength or weakness of a market move, as high volumes often indicate strong moves and vice versa.
"""

VOLUME_USAGE = {
    "Buy": "High trading volumes during a market uptrend may suggest a good buying opportunity, as it indicates strong positive momentum.",
    "Sell": "Conversely, high trading volumes during a market downtrend may signal a selling opportunity, reflecting strong negative momentum.",
    "Risk/Opportunity Detection": "Analyzing trading volumes can help in identifying potential reversals or breakouts. For instance, a sudden spike in volume might indicate the start of a new trend, presenting an opportunity for traders to position themselves accordingly."
}

VWAP_ANALYSIS_TITLE = "VWAP Analysis"

VWAP_DESCRIPTION = """
The Volume Weighted Average Price (VWAP) is a vital trading benchmark that illustrates the average price at which Bitcoin trades have been executed, weighted by volume. It is computed over a specific time period, presenting traders with an insight into the true average price of Bitcoin, considering both price and volume.
"""

VWAP_USAGE = {
    "Buy": "Traders could consider buying opportunities when the price is below the VWAP line, indicating that Bitcoin is potentially undervalued at that point in time, thus might be a good buying point.",
    "Sell": "Conversely, when the price is above the VWAP line, it signifies that Bitcoin is potentially overvalued, suggesting a selling opportunity to capitalize on the higher prices.",
    "Risk/Opportunity Detection": "Utilizing VWAP can assist in identifying potential market reversals and opportunities. A significant deviation from the VWAP line might indicate a potential reversal, offering an opportunity to strategize trades accordingly. Moreover, it can help in detecting periods of high liquidity and trading volume, helping to mitigate risk and identify potential entry and exit points."
}

VOLATILITY_TITLE = "Volatility Analysis"

VOLATILITY_DESCRIPTION = """
The graph representation that highlights the volatility in Bitcoin prices. Volatility, in this context, is measured as the daily percentage change between the highest and lowest prices. It serves as a critical tool for traders to understand the market's behavior and fluctuations over a given time period.
"""

VOLATILITY_USAGE = {
    "Buy": "Traders might consider buying opportunities during periods of low volatility, anticipating a potential surge in the near future. Additionally, identifying patterns of increasing volatility can suggest the onset of a bullish market phase.",
    "Sell": "Periods of high volatility, particularly when accompanied by a downward trend in prices, might suggest a good time to sell, as it can indicate a bearish market phase or the onset of a potential downturn.",
    "Risk/Opportunity Detection": "Tracking volatility assists in recognizing potential market risks and opportunities. Spikes in volatility often signal significant market events, and monitoring these can help in making informed decisions to capitalize on market movements or to implement strategies to mitigate risk."
}

MACD_ANALYSIS_TITLE = "MACD Analysis"

MACD_LINE_DESCRIPTION = """
The MACD Line is a trend-following momentum indicator that reveals the relationship between two moving averages of a security’s price. It is calculated by subtracting the 26-period Exponential Moving Average (EMA) from the 12-period EMA.
"""

MACD_LINE_USAGE = {
    "Buy": "A buy signal is generated when the MACD Line crosses above the Signal Line, indicating potential upward momentum.",
    "Sell": "A sell signal is triggered when the MACD Line crosses below the Signal Line, suggesting potential downward momentum.",
    "Risk/Opportunity Detection": "The MACD Line can help in detecting potential market reversals. A divergence between the MACD Line and the price action is a strong indicator of potential reversals."
}

SIGNAL_LINE_DESCRIPTION = """
The Signal Line is a 9-period EMA of the MACD Line, used to identify potential buy or sell signals.
"""

SIGNAL_LINE_USAGE = {
    "Buy": "Buy signals are generally considered when the MACD Line crosses above the Signal Line.",
    "Sell": "Conversely, sell signals are considered when the MACD Line crosses below the Signal Line.",
    "Risk/Opportunity Detection": "Observing the interactions between the MACD Line and the Signal Line can provide insights into potential trend reversals and opportunities in the market."
}
