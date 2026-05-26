import threading
from config import settings

class RoundRobinRotator:
    def __init__(self, items: list[str], name: str):
        self._items = items
        self._name = name
        self._index = 0
        self._lock = threading.Lock()

    def get_current(self) -> str:
        with self._lock:
            return self._items[self._index]

    def rotate(self) -> str:
        with self._lock:
            self._index = (self._index + 1) % len(self._items)
            return self._items[self._index]

    def get_all(self) -> list[str]:
        return self._items.copy()

    @property
    def count(self) -> int:
        return len(self._items)

    @property
    def index(self) -> int:
        with self._lock:
            return self._index

    def reset_index(self):
        with self._lock:
            self._index = 0


# GitHub token rotation only
# Cerebras rotation handled by CerebrasRotator in utils/cerebras.py
github_token_rotator = RoundRobinRotator(
    settings.github_tokens, "GitHub"
)
