"""
Binance Futures API Client
Handles authentication, request signing, and API communication
"""
import time
import hmac
import hashlib
from typing import Dict, Any, Optional
from urllib.parse import urlencode
import requests

from config import config
from logger import setup_logger
from exceptions import BinanceAPIError, NetworkError

logger = setup_logger(__name__)


class BinanceClient:
    """
    Client for interacting with Binance Futures Testnet API
    """
    
    def __init__(self, api_key: str, api_secret: str, base_url: str = None):
        """
        Initialize Binance client
        
        Args:
            api_key: Binance API key
            api_secret: Binance API secret
            base_url: Base URL for API (defaults to testnet)
        """
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = base_url or config.TESTNET_BASE_URL
        self.session = requests.Session()
        self.session.headers.update({
            "X-MBX-APIKEY": self.api_key,
            "Content-Type": "application/x-www-form-urlencoded"
        })
        logger.info(f"Initialized Binance client with base URL: {self.base_url}")
    
    def _generate_signature(self, params: Dict[str, Any]) -> str:
        """
        Generate HMAC SHA256 signature for request
        
        Args:
            params: Request parameters
            
        Returns:
            Hexadecimal signature string
        """
        query_string = urlencode(params)
        signature = hmac.new(
            self.api_secret.encode("utf-8"),
            query_string.encode("utf-8"),
            hashlib.sha256
        ).hexdigest()
        return signature
    
    def _send_signed_request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Send a signed request to Binance API
        
        Args:
            method: HTTP method (GET, POST, DELETE, etc.)
            endpoint: API endpoint path
            params: Request parameters
            
        Returns:
            JSON response from API
            
        Raises:
            NetworkError: If request fails
            BinanceAPIError: If API returns an error
        """
        params = params or {}
        params["timestamp"] = int(time.time() * 1000)
        params["signature"] = self._generate_signature(params)
        
        url = f"{self.base_url}{endpoint}"
        
        logger.debug(f"Sending {method} request to {endpoint}")
        logger.debug(f"Parameters: {params}")
        
        try:
            if method.upper() == "GET":
                response = self.session.get(url, params=params, timeout=10)
            elif method.upper() == "POST":
                response = self.session.post(url, params=params, timeout=10)
            elif method.upper() == "DELETE":
                response = self.session.delete(url, params=params, timeout=10)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            logger.debug(f"Response status: {response.status_code}")
            logger.debug(f"Response body: {response.text}")
            
            response.raise_for_status()
            
            return response.json()
            
        except requests.exceptions.Timeout as e:
            logger.error(f"Request timeout: {e}")
            raise NetworkError(f"Request timeout: {e}")
        except requests.exceptions.ConnectionError as e:
            logger.error(f"Connection error: {e}")
            raise NetworkError(f"Connection error: {e}")
        except requests.exceptions.HTTPError as e:
            error_data = {}
            try:
                error_data = response.json()
            except Exception:
                pass
            
            error_msg = error_data.get("msg", str(e))
            error_code = error_data.get("code", response.status_code)
            
            logger.error(f"API error [{error_code}]: {error_msg}")
            raise BinanceAPIError(
                message=error_msg,
                code=error_code,
                response=error_data
            )
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            raise NetworkError(f"Unexpected error: {e}")
    
    def get_server_time(self) -> int:
        """
        Get Binance server time
        
        Returns:
            Server timestamp in milliseconds
        """
        endpoint = "/fapi/v1/time"
        url = f"{self.base_url}{endpoint}"
        
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            return data.get("serverTime")
        except Exception as e:
            logger.error(f"Failed to get server time: {e}")
            raise NetworkError(f"Failed to get server time: {e}")
    
    def get_exchange_info(self, symbol: Optional[str] = None) -> Dict[str, Any]:
        """
        Get exchange information
        
        Args:
            symbol: Optional symbol to filter by
            
        Returns:
            Exchange information
        """
        endpoint = "/fapi/v1/exchangeInfo"
        url = f"{self.base_url}{endpoint}"
        params = {"symbol": symbol} if symbol else {}
        
        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Failed to get exchange info: {e}")
            raise NetworkError(f"Failed to get exchange info: {e}")
    
    def place_order(
        self,
        symbol: str,
        side: str,
        order_type: str,
        quantity: float,
        price: Optional[float] = None,
        time_in_force: str = "GTC"
    ) -> Dict[str, Any]:
        """
        Place an order on Binance Futures
        
        Args:
            symbol: Trading pair symbol (e.g., BTCUSDT)
            side: Order side (BUY or SELL)
            order_type: Order type (MARKET or LIMIT)
            quantity: Order quantity
            price: Limit price (required for LIMIT orders)
            time_in_force: Time in force (default: GTC - Good Till Cancel)
            
        Returns:
            Order response from API
        """
        endpoint = "/fapi/v1/order"
        
        params = {
            "symbol": symbol,
            "side": side,
            "type": order_type,
            "quantity": quantity,
        }
        
        if order_type == "LIMIT":
            if price is None:
                raise ValueError("Price is required for LIMIT orders")
            params["price"] = price
            params["timeInForce"] = time_in_force
        
        logger.info(f"Placing {order_type} {side} order for {quantity} {symbol}")
        if price:
            logger.info(f"Limit price: {price}")
        
        return self._send_signed_request("POST", endpoint, params)
    
    def get_account_info(self) -> Dict[str, Any]:
        """
        Get account information
        
        Returns:
            Account information including balances
        """
        endpoint = "/fapi/v2/account"
        return self._send_signed_request("GET", endpoint)
    
    def get_position_info(self, symbol: Optional[str] = None) -> Dict[str, Any]:
        """
        Get position information
        
        Args:
            symbol: Optional symbol to filter by
            
        Returns:
            Position information
        """
        endpoint = "/fapi/v2/positionRisk"
        params = {"symbol": symbol} if symbol else {}
        return self._send_signed_request("GET", endpoint, params)
