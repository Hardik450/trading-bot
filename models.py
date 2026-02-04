"""
Data models for trading bot
"""
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field, field_validator


class OrderSide(str, Enum):
    """Order side enumeration"""
    BUY = "BUY"
    SELL = "SELL"


class OrderType(str, Enum):
    """Order type enumeration"""
    MARKET = "MARKET"
    LIMIT = "LIMIT"


class OrderRequest(BaseModel):
    """Order request model with validation"""
    symbol: str = Field(..., min_length=1, description="Trading pair symbol (e.g., BTCUSDT)")
    side: OrderSide = Field(..., description="Order side (BUY or SELL)")
    order_type: OrderType = Field(..., description="Order type (MARKET or LIMIT)")
    quantity: float = Field(..., gt=0, description="Order quantity (must be positive)")
    price: Optional[float] = Field(None, gt=0, description="Limit price (required for LIMIT orders)")
    
    @field_validator("symbol")
    @classmethod
    def validate_symbol(cls, v: str) -> str:
        """Ensure symbol is uppercase and has no spaces"""
        return v.upper().strip()
    
    @field_validator("price")
    @classmethod
    def validate_price_for_limit(cls, v: Optional[float], info) -> Optional[float]:
        """Ensure price is provided for LIMIT orders"""
        if info.data.get("order_type") == OrderType.LIMIT and v is None:
            raise ValueError("Price is required for LIMIT orders")
        if info.data.get("order_type") == OrderType.MARKET and v is not None:
            raise ValueError("Price should not be provided for MARKET orders")
        return v
    
    class Config:
        use_enum_values = True


class OrderResponse(BaseModel):
    """Order response model"""
    order_id: int = Field(..., alias="orderId")
    symbol: str
    status: str
    side: str
    order_type: str = Field(..., alias="type")
    quantity: str = Field(..., alias="origQty")
    price: str
    executed_qty: str = Field(..., alias="executedQty")
    cumulative_quote_qty: str = Field(..., alias="cumQuote")
    avg_price: Optional[str] = Field(None, alias="avgPrice")
    time_in_force: Optional[str] = Field(None, alias="timeInForce")
    
    class Config:
        populate_by_name = True
        
    def __str__(self) -> str:
        """String representation of order response"""
        lines = [
            f"Order ID: {self.order_id}",
            f"Symbol: {self.symbol}",
            f"Status: {self.status}",
            f"Side: {self.side}",
            f"Type: {self.order_type}",
            f"Quantity: {self.quantity}",
            f"Executed Quantity: {self.executed_qty}",
        ]
        
        if self.price and float(self.price) > 0:
            lines.append(f"Price: {self.price}")
        
        if self.avg_price and float(self.avg_price) > 0:
            lines.append(f"Average Price: {self.avg_price}")
        
        if self.cumulative_quote_qty:
            lines.append(f"Cumulative Quote: {self.cumulative_quote_qty}")
            
        return "\n".join(lines)
