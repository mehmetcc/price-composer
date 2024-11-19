from typing import Annotated, Dict
from fastapi import Depends, FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from price_composer.dependencies import get_symbols
from price_composer.resolver.symbol_resolver import get_latest_stock_prices
import asyncio

from ..utils.symbols import Symbols

origins = [
    "http://localhost:3000"
]


app = FastAPI()
app.add_middleware(CORSMiddleware, 
                   allow_origins=origins, 
                   allow_credentials=True, 
                   allow_methods=["*"],
                   allow_headers=["*"],)


@app.get('/')
async def root() -> Dict[str, str]:
    return {'message': 'I am running, against all odds'}

@app.get('/api/v1/stock')
async def stock(symbols: Annotated[Symbols, Depends(get_symbols)]) -> list[str]:
    return symbols.stocks

@app.websocket('/api/v1/ws')
async def prices(websocket: WebSocket, symbols: Annotated[Symbols, Depends(get_symbols)]) -> None:
    await websocket.accept()

    while True:
        await asyncio.sleep(10)
        await websocket.send_json(get_latest_stock_prices(symbols.stocks))