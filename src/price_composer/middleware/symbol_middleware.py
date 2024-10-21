from price_composer.dependencies import get_symbols
from price_composer.utils.symbols import Symbols
import yfinance as yf
from fastapi import Depends
from typing import Annotated


class StockNotFoundException(Exception):
    pass

async def get_latest_price(symbol: str) -> float:
    ticker = yf.Ticker(symbol)
    return ticker.fast_info.last_price

async def get_latest_stock_price(symbol: str, symbols: Annotated[Symbols, Depends(get_symbols)]) -> float:
    if symbol not in symbols.stocks:
        raise StockNotFoundException('Stock can\'t be found')
    
    return get_latest_price(symbol)
