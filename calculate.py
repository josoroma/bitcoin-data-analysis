import logging
from pandas import DataFrame

# Initialize logging
logging.basicConfig(level=logging.INFO)


def calculate_market_data(df: DataFrame) -> DataFrame:
    """
    Calculates various market data features such as VWAP, rolling mean, and Bollinger Bands.

    :param df: Input data frame with market data
    :return: Data frame with calculated features
    """
    if not isinstance(df, DataFrame):
        logging.error("Input is not a data frame")
        raise ValueError("Input must be a data frame")

    try:
        df["vwap"] = (df["volume_traded"] * df["price_close"]).cumsum() / df["volume_traded"].cumsum()

        df["rolling_mean"] = df["price_close"].rolling(window=20).mean()
        df["rolling_std"] = df["price_close"].rolling(window=20).std()
        df["bollinger_upper"] = df["rolling_mean"] + (df["rolling_std"] * 2)
        df["bollinger_lower"] = df["rolling_mean"] - (df["rolling_std"] * 2)

        df["ma50"] = df["price_close"].rolling(window=50).mean()
        df["ma200"] = df["price_close"].rolling(window=200).mean()
    except KeyError as e:
        logging.error(f"Missing necessary columns in data frame: {e}")
        raise

    return df


def calculate_volatility(df: DataFrame) -> DataFrame:
    """
    Calculates volatility based on price high, low, and open.

    :param df: Input data frame with market data
    :return: Data frame with calculated volatility
    """
    try:
        df["volatility"] = ((df["price_high"] - df["price_low"]) / df["price_open"]) * 100
    except KeyError as e:
        logging.error(f"Missing necessary columns in data frame: {e}")
        raise

    return df


def calculate_trade_velocity(df: DataFrame) -> DataFrame:
    """
    Calculates trade velocity based on trade count and time difference.

    :param df: Input data frame with market data
    :return: Data frame with calculated trade velocity
    """
    try:
        df["trade_velocity"] = df["trades_count"] / ((df["time_close"] - df["time_open"]).dt.total_seconds() / 3600)
    except KeyError as e:
        logging.error(f"Missing necessary columns in data frame: {e}")
        raise

    return df


def calculate_rsi(df: DataFrame) -> DataFrame:
    """
    Calculates the Relative Strength Index (RSI).

    :param df: Input data frame with market data
    :return: Data frame with calculated RSI
    """
    try:
        delta = df["price_close"].diff()
        gain = (delta.where(delta > 0, 0)).fillna(0)
        loss = (-delta.where(delta < 0, 0)).fillna(0)
        avg_gain = gain.rolling(window=14).mean()
        avg_loss = loss.rolling(window=14).mean()
        rs = avg_gain / avg_loss
        df["rsi"] = 100 - (100 / (1 + rs))
    except KeyError as e:
        logging.error(f"Missing necessary columns in data frame: {e}")
        raise

    return df


def calculate_macd(df: DataFrame) -> DataFrame:
    """
    Calculates the Moving Average Convergence Divergence (MACD).

    :param df: Input data frame with market data
    :return: Data frame with calculated MACD
    """
    try:
        df["ema12"] = df["price_close"].ewm(span=12, adjust=False).mean()
        df["ema26"] = df["price_close"].ewm(span=26, adjust=False).mean()
        df["macd"] = df["ema12"] - df["ema26"]
        df["macd_signal"] = df["macd"].ewm(span=9, adjust=False).mean()
    except KeyError as e:
        logging.error(f"Missing necessary columns in data frame: {e}")
        raise

    return df
