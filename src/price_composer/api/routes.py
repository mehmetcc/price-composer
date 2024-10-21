from functools import lru_cache
from typing import Annotated, Dict
from fastapi import Depends, FastAPI
from price_composer.dependencies import get_symbols

from ..utils.symbols import Symbols

app = FastAPI()

@app.get('/')
async def root() -> Dict[str, str]:
    return {'message': 'I am running, against all odds'}

@app.get('/api/v1/stock')
async def stock(symbols: Annotated[Symbols, Depends(get_symbols)]) -> list[str]:
    return symbols.stocks
