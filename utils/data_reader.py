from typing import Any, Dict
import logging

logger = logging.getLogger(__name__)

class DataReader:
    def __init__(self, test_data: Dict = None):
        self._data = test_data or {}

    def get_value(self, key: str, default: Any = None) -> Any:
        keys = key.split('.')
        value = self._data
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                logger.warning(f"Key {key} not found, returning default: {default}")
                return default
        return value

# For compatibility with your code
APIDataReader = DataReader