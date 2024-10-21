from functools import lru_cache
from price_composer.utils.symbols import Symbols


@lru_cache
def get_symbols() -> Symbols:
    return Symbols()
