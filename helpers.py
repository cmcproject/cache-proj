from abc import ABC, abstractmethod
from datetime import timedelta


class Cache(ABC):
    @abstractmethod
    def set(self, key: str, value: str, ttl: timedelta):
        """Store a key-value pair with a TTL duration specified by timedelta."""
        pass

    @abstractmethod
    def get(self, key: str) -> str:
        """Retrieve a value by key. Returns None if key is not found or expired."""
        pass
