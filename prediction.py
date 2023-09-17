from datetime import timedelta

import pandas as pd

from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

class Prediction:
    def __init__(self):
        pass

    @staticmethod
    def append_forecasted_data_using_sklearn_linear_regression_dataset_with_training_testing_set(df):
            # Convert columns to datetime format to prevent errors during subtraction
            df['time_period_start'] = pd.to_datetime(df['time_period_start'])
            df['time_period_end'] = pd.to_datetime(df['time_period_end'])
            df['time_open'] = pd.to_datetime(df['time_open'])
            df['time_close'] = pd.to_datetime(df['time_close'])

            # Prepare data for linear regression model
            df['hour'] = df['time_period_start'].dt.hour
            df['day'] = df['time_period_start'].dt.day
            df['month'] = df['time_period_start'].dt.month
            df['year'] = df['time_period_start'].dt.year
            
            # Get the greatest date from the data
            greatest_date = df['time_period_start'].max()

            # Calculate the next week date range starting from the greatest date
            future_dates = pd.date_range(start=greatest_date, periods=7*24, freq='H')

            # Create a future dataframe for forecasting next one week
            future_df = pd.DataFrame({'time_period_start': future_dates})
            future_df['time_period_end'] = future_df['time_period_start'] + timedelta(hours=1)
            future_df['hour'] = future_df['time_period_start'].dt.hour
            future_df['day'] = future_df['time_period_start'].dt.day
            future_df['month'] = future_df['time_period_start'].dt.month
            future_df['year'] = future_df['time_period_start'].dt.year

            # List of columns to be forecasted
            forecast_columns = [
                'price_open', 
                'price_high', 
                'price_low', 
                'price_close', 
                'volume_traded', 
                'trades_count', 
                'volatility', 
                'trade_velocity', 
                'rolling_mean', 
                'rolling_std', 
                'bollinger_upper', 
                'bollinger_lower', 
                'ma50', 
                'ma200', 
                'vwap', 
                'rsi', 
                'ema12', 
                'ema26', 
                'macd', 
                'macd_signal'
            ]

            # Forecast the future data for each column using separate models
            for col in forecast_columns:
                X = df[['hour', 'day', 'month', 'year']]
                y = df[col]

                # Remove or fill NaN values here
                y = y.fillna(y.mean())  # Filling NaN values with mean

                X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)
                
                model = LinearRegression()
                model.fit(X_train, y_train)
                
                future_X = future_df[['hour', 'day', 'month', 'year']]
                future_df[col] = model.predict(future_X)

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
