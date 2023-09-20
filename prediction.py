from datetime import timedelta
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import logging

logging.basicConfig(level=logging.INFO)

def convert_to_datetime(df):
    """Convert columns to datetime format to prevent errors during subtraction."""
    datetime_columns = ["time_period_start", "time_period_end", "time_open", "time_close"]
    for col in datetime_columns:
        try:
            df[col] = pd.to_datetime(df[col])
        except Exception as e:
            logging.error(f"Error converting column {col} to datetime: {e}")
    return df

def prepare_data_for_regression(df):
    """Prepare data for the linear regression model by extracting date components."""
    df["hour"] = df["time_period_start"].dt.hour
    df["day"] = df["time_period_start"].dt.day
    df["month"] = df["time_period_start"].dt.month
    df["year"] = df["time_period_start"].dt.year
    return df

def create_future_dataframe(greatest_date):
    """Create a future dataframe for forecasting the next one week."""
    future_dates = pd.date_range(start=greatest_date, periods=7*24, freq='H')
    future_df = pd.DataFrame({"time_period_start": future_dates})
    future_df["time_period_end"] = future_df["time_period_start"] + timedelta(hours=1)
    future_df = prepare_data_for_regression(future_df)
    return future_df

def forecast_column(df, future_df, col):
    """Forecast a single column using a linear regression model."""
    try:
        X = df[["hour", "day", "month", "year"]]
        y = df[col].fillna(df[col].mean())  # Filling NaN values with mean

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)
        
        model = LinearRegression()
        model.fit(X_train, y_train)
        
        future_X = future_df[["hour", "day", "month", "year"]]
        future_df[col] = model.predict(future_X)
    except Exception as e:
        logging.error(f"Error forecasting column {col}: {e}")

def append_forecasted_data(df):
    """Append forecasted data to the original dataframe."""
    df = convert_to_datetime(df)
    df = prepare_data_for_regression(df)
    greatest_date = df["time_period_start"].max()
    future_df = create_future_dataframe(greatest_date)

    forecast_columns = [
        "price_open", "price_high", "price_low", "price_close", 
        "volume_traded", "trades_count", "volatility", "trade_velocity", 
        "rolling_mean", "rolling_std", "bollinger_upper", "bollinger_lower", 
        "ma50", "ma200", "vwap", "rsi", "ema12", "ema26", "macd", "macd_signal"
    ]

    for col in forecast_columns:
        forecast_column(df, future_df, col)

    # Calculate forecasted time_open and time_close based on average time differences
    avg_time_to_open = (df['time_open'] - df['time_period_start']).mean()
    avg_time_to_close = (df['time_period_end'] - df['time_close']).mean()
    future_df['time_open'] = future_df['time_period_start'] + avg_time_to_open
    future_df['time_close'] = future_df['time_period_end'] - avg_time_to_close

    # Create a reversed version of future_df
    reversed_future_df = future_df.iloc[::-1].reset_index(drop=True)
    reversed_future_df = reversed_future_df.iloc[1:-1].reset_index(drop=True)

    # Prepend the reversed data to the existing data
    df = pd.concat([reversed_future_df, df], ignore_index=True)

    return df
