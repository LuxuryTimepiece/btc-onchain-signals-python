import requests
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

# Constants for API time range
START_DATE = int((datetime.now() - timedelta(days=30)).timestamp() * 1000)  # 30 days ago in milliseconds
END_DATE = int(datetime.now().timestamp() * 1000)  # Now in milliseconds

def get_price_data():
    """Fetch 30 days of OHLC price data from CoinGecko."""
    try:
        url = f"https://api.coingecko.com/api/v3/coins/bitcoin/ohlc?vs_currency=usd&from={START_DATE}&to={END_DATE}&days=30"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        df = pd.DataFrame(data, columns=["timestamp", "open", "high", "low", "close"])
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
        return df
    except Exception as e:
        logger.error(f"Error fetching price data: {e}")
        return None

def get_onchain_data():
    """Fetch on-chain data (transactions and unique addresses) from Blockchain.com."""
    metrics = {
        "n-transactions": "https://api.blockchain.info/charts/n-transactions?timespan=30days&format=json",
        "n-unique-addresses": "https://api.blockchain.info/charts/n-unique-addresses?timespan=30days&format=json",
    }
    onchain_data = {}
    try:
        for metric, url in metrics.items():
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()["values"]
            df = pd.DataFrame(data)
            df["x"] = pd.to_datetime(df["x"], unit="s")
            onchain_data[metric] = df.rename(columns={"x": "timestamp", "y": metric})
        return onchain_data
    except Exception as e:
        logger.error(f"Error fetching on-chain data: {e}")
        return None

def get_mempool_data():
    """Fetch block height and fee rates from mempool.space."""
    try:
        block_height = requests.get("https://mempool.space/api/blocks/tip/height").text
        fee_rates = requests.get("https://mempool.space/api/v1/fees/recommended").json()
        return {"block_height": int(block_height), "fee_rates": fee_rates}
    except Exception as e:
        logger.error(f"Error fetching mempool data: {e}")
        return None

def calculate_rsi(price_df, period=14):
    """Calculate 14-period RSI manually."""
    if price_df is None or price_df.empty:
        return None
    prices = price_df["close"].values
    if len(prices) < period + 1:
        return price_df

    # Calculate price changes (deltas)
    deltas = np.diff(prices)
    
    # Initialize gains and losses
    gains = np.zeros(len(prices))
    losses = np.zeros(len(prices))
    
    # First period: average gains and losses
    for i in range(period):
        if deltas[i] > 0:
            gains[i + 1] = deltas[i]
        elif deltas[i] < 0:
            losses[i + 1] = -deltas[i]
    
    avg_gain = np.mean(gains[1:period + 1])
    avg_loss = np.mean(losses[1:period + 1])
    
    # Calculate RSI for the first period
    rsi = np.zeros(len(prices))
    if avg_loss == 0:
        rsi[period] = 100
    else:
        rs = avg_gain / avg_loss
        rsi[period] = 100 - (100 / (1 + rs))
    
    # Calculate RSI for subsequent periods using smoothing
    for i in range(period, len(deltas)):
        delta = deltas[i]
        gain = max(delta, 0)
        loss = max(-delta, 0)
        
        avg_gain = ((avg_gain * (period - 1)) + gain) / period
        avg_loss = ((avg_loss * (period - 1)) + loss) / period
        
        if avg_loss == 0:
            rsi[i + 1] = 100
        else:
            rs = avg_gain / avg_loss
            rsi[i + 1] = 100 - (100 / (1 + rs))
    
    price_df["rsi"] = rsi
    return price_df

def generate_signals(df):
    """Generate trading signals based on RSI and on-chain metrics."""
    if df is None or df.empty:
        return None
    df["signal"] = "Hold"
    df["n-unique-addresses"] = df["n-unique-addresses"].ffill()
    df["n-transactions"] = df["n-transactions"].ffill()
    df["addr_change_7d"] = df["n-unique-addresses"].pct_change(periods=6)
    df["tx_change_7d"] = df["n-transactions"].pct_change(periods=6)
    df.loc[(df["rsi"] < 30) & (df["addr_change_7d"] > 0), "signal"] = "Buy"
    df.loc[(df["rsi"] > 70) & (df["tx_change_7d"] < 0), "signal"] = "Sell"
    return df

def fetch_bitcoin_data():
    """Main function to fetch and process data, returning the latest data point and historical data for the graph."""
    try:
        # Fetch data
        price_df = get_price_data()
        if price_df is None:
            return None
        onchain_data = get_onchain_data()
        if onchain_data is None:
            return None
        mempool_data = get_mempool_data()
        if mempool_data is None:
            return None

        # Calculate RSI
        price_df = calculate_rsi(price_df)
        if price_df is None:
            return None

        # Merge data
        tx_df = onchain_data["n-transactions"]
        addr_df = onchain_data["n-unique-addresses"]
        merged_df = price_df.merge(tx_df[["timestamp", "n-transactions"]], on="timestamp", how="left")
        merged_df = merged_df.merge(addr_df[["timestamp", "n-unique-addresses"]], on="timestamp", how="left")
        merged_df["block_height"] = mempool_data["block_height"]
        merged_df["fastest_fee"] = mempool_data["fee_rates"]["fastestFee"]

        # Generate signals
        merged_df = generate_signals(merged_df)
        if merged_df is None:
            return None

        # Convert timestamps to strings for JSON serialization
        merged_df["timestamp"] = merged_df["timestamp"].dt.strftime('%Y-%m-%dT%H:%M:%S')

        # Prepare data for the frontend
        latest = merged_df.iloc[-1]
        price_change_24h = ((latest["close"] - merged_df.iloc[-2]["close"]) / merged_df.iloc[-2]["close"] * 100) if len(merged_df) > 1 else 0

        # Prepare historical data for the graph (last 30 days)
        historical_data = merged_df.tail(30).to_dict(orient="records")

        return {
            "price": float(latest["close"]),
            "price_change_24h": float(price_change_24h),
            "active_addresses": int(latest["n-unique-addresses"]) if not pd.isna(latest["n-unique-addresses"]) else 0,
            "tx_volume": float(latest["n-transactions"]) if not pd.isna(latest["n-transactions"]) else 0,
            "rsi": float(latest["rsi"]) if not pd.isna(latest["rsi"]) else None,
            "signal": latest["signal"],
            "block_height": int(latest["block_height"]),
            "fastest_fee": int(latest["fastest_fee"]),
            "historical_data": historical_data,  # For the graph
        }
    except Exception as e:
        logger.error(f"Error in fetch_bitcoin_data: {e}")
        return None