import requests
import logging

logger = logging.getLogger(__name__)

def fetch_bitcoin_data():
    try:
        # For testing, return mock data
        return {
            'price': 60000.00,
            'price_change_24h': 2.5,
            'active_addresses': 800000,
            'tx_count': 300000,
            'hash_rate': 180.5
        }
    except Exception as e:
        logger.error(f"Error fetching data: {e}")
        return None