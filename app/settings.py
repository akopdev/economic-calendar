from dataclasses import dataclass
from typing import Any
import os

@dataclass
class Settings:
    DATABASE_DSL: str = "mongodb://demo:demo@localhost:27017/"
    DATABASE_NAME: str = "economic_calendar"

    def __getattribute__(self, name: str) -> Any:
        """
        Use environment variable values if possible
        """
        try:
            value = os.getenv(name, None)
            if value is None:
                value = object.__getattribute__(self, name)
        except AttributeError:
            value = None
        return value

settings = Settings()
