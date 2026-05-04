from abc import ABC, abstractmethod
from typing import Any, Dict


class Printable(ABC):

    @abstractmethod
    def to_string(self, verbose: bool = True) -> str:
        pass


class Comparable(ABC):
    @abstractmethod
    def compare_to(self, other: Any) -> int:
        pass


class InterestCalculable(ABC):
    
    @abstractmethod
    def calculate_interest(self) -> float:
        pass
    
    @abstractmethod
    def process_monthly(self) -> Dict[str, Any]:
        pass


class Withdrawable(ABC):
    @abstractmethod
    def withdraw(self, amount: float) -> bool:
        pass


class DepositCalculable(ABC):
    
    @abstractmethod
    def get_profit_forecast(self, months: int) -> float:
        pass