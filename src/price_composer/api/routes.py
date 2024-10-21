from concurrent.futures import thread
from functools import lru_cache
from typing import Annotated, Dict
from fastapi import Depends, FastAPI, WebSocket
from price_composer.dependencies import get_symbols
from price_composer.resolver.symbol_resolver import get_latest_stock_prices
import asyncio

from ..utils.symbols import Symbols

app = FastAPI()

@app.get('/')
async def root() -> Dict[str, str]:
    return {'message': 'I am running, against all odds'}

@app.get('/api/v1/stock')
async def stock(symbols: Annotated[Symbols, Depends(get_symbols)]) -> list[str]:
    return symbols.stocks

@app.websocket('/ws')
async def prices(websocket: WebSocket, symbols: Annotated[Symbols, Depends(get_symbols)]) -> None:
    await websocket.accept()

    while True:
        await asyncio.sleep(60)
        await websocket.send_json(get_latest_stock_prices(symbols.stocks))