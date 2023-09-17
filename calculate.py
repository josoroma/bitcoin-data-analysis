
class Calculate:
    def __init__(self):
        pass

    @staticmethod
    def calculate_market_data(df):
        df['vwap'] = (df['volume_traded'] * df['price_close']).cumsum() / df['volume_traded'].cumsum()
        
        df['rolling_mean'] = df['price_close'].rolling(window=20).mean()
        df['rolling_std'] = df['price_close'].rolling(window=20).std()
        df['bollinger_upper'] = df['rolling_mean'] + (df['rolling_std'] * 2)
        df['bollinger_lower'] = df['rolling_mean'] - (df['rolling_std'] * 2)

        df['ma50'] = df['price_close'].rolling(window=50).mean()
        df['ma200'] = df['price_close'].rolling(window=200).mean()
        
        return df

    @staticmethod
    def calculate_volatility(df):
        df['volatility'] = ((df['price_high'] - df['price_low']) / df['price_open']) * 100
        return df
    
    @staticmethod
    def calculate_trade_velocity(df):
        df['trade_velocity'] = df['trades_count'] / ((df['time_close'] - df['time_open']).dt.total_seconds()/3600)        
        return df

    @staticmethod
    def calculate_rsi_and_macd(df):
        delta = df['price_close'].diff()
        gain = (delta.where(delta > 0, 0)).fillna(0)
        loss = (-delta.where(delta < 0, 0)).fillna(0)
        avg_gain = gain.rolling(window=14).mean()
        avg_loss = loss.rolling(window=14).mean()
        rs = avg_gain / avg_loss
        # RSI
        df['rsi'] = 100 - (100 / (1 + rs))
        # MACD
        df['ema12'] = df['price_close'].ewm(span=12, adjust=False).mean()
        df['ema26'] = df['price_close'].ewm(span=26, adjust=False).mean()
        df['macd'] = df['ema12'] - df['ema26']
        df['macd_signal'] = df['macd'].ewm(span=9, adjust=False).mean()

        return df
