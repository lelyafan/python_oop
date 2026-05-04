from typing import TypeVar, Generic, List, Optional, Callable, Any
from abc import ABC, abstractmethod
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from lab04.interfaces import Printable, Comparable, InterestCalculable, Withdrawable, DepositCalculable

T = TypeVar('T')


class BankCollection(Generic[T]): 
    def __init__(self, item_type: type, id_attr: str = "account_number"):
        self._items: List[T] = []
        self._item_type = item_type
        self._id_attr = id_attr

    def _get_item_id(self, item: T):
        return getattr(item, self._id_attr)

    def add(self, item: T) -> None:
        if not isinstance(item, self._item_type):
            raise TypeError(f"Можно добавлять только объекты типа {self._item_type.__name__}")

        item_id = self._get_item_id(item)
        if any(self._get_item_id(existing) == item_id for existing in self._items):
            raise ValueError(f"Объект с {self._id_attr}={item_id} уже существует в коллекции")

        self._items.append(item)

    def remove(self, item: T) -> None:
        if item not in self._items:
            raise ValueError("Объект не найден в коллекции")
        self._items.remove(item)

    def remove_at(self, index: int) -> None:
        if index < 0 or index >= len(self._items):
            raise IndexError("Индекс вне диапазона")
        del self._items[index]

    def get_all(self) -> List[T]:
        return self._items.copy()

    def get_by_index(self, index: int) -> T:
        if index < 0 or index >= len(self._items):
            raise IndexError("Индекс вне диапазона")
        return self._items[index]

    def find_by(self, **kwargs) -> Optional[T]:
        for item in self._items:
            match = True
            for attr, value in kwargs.items():
                if getattr(item, attr, None) != value:
                    match = False
                    break
            if match:
                return item
        return None

    def find_all_by(self, **kwargs) -> List[T]:
        result = []
        for item in self._items:
            match = True
            for attr, value in kwargs.items():
                if getattr(item, attr, None) != value:
                    match = False
                    break
            if match:
                result.append(item)
        return result
    
    def filter_by_interface(self, interface_type: type) -> List[Any]:
        return [item for item in self._items if isinstance(item, interface_type)]
    
    def get_printable_items(self) -> List[Printable]:
        return self.filter_by_interface(Printable)
    
    def get_comparable_items(self) -> List[Comparable]:
        return self.filter_by_interface(Comparable)
    
    def get_interest_calculable_items(self) -> List[InterestCalculable]:
        return self.filter_by_interface(InterestCalculable)
    
    def get_withdrawable_items(self) -> List[Withdrawable]:
        return self.filter_by_interface(Withdrawable)
    
    def get_deposit_calculable_items(self) -> List[DepositCalculable]:
        return self.filter_by_interface(DepositCalculable)

    def process_all_monthly(self) -> List[dict]:
        results = []
        for item in self.get_interest_calculable_items():
            results.append(item.process_monthly())
        return results
    
    def print_all_short(self) -> None:
        for item in self.get_printable_items():
            print(item.to_string(verbose=False))
    
    def print_all_detailed(self) -> None:
        for item in self.get_printable_items():
            print(item.to_string(verbose=True))
            print()
    
    def get_total_balance(self) -> float:
        return sum(getattr(item, "balance", 0) for item in self._items)
    
    def get_total_profit_forecast(self, months: int = 6) -> float:
        total = 0
        for item in self.get_deposit_calculable_items():
            total += item.get_profit_forecast(months)
        return total

    def __len__(self) -> int:
        return len(self._items)

    def __iter__(self):
        return iter(self._items)

    def __getitem__(self, index):
        if isinstance(index, slice):
            result = BankCollection(self._item_type, self._id_attr)
            result._items = self._items[index]
            return result
        if index < 0 or index >= len(self._items):
            raise IndexError("Индекс вне диапазона")
        return self._items[index]

    def sort(self, key: Callable[[T], any], reverse: bool = False) -> None:
        self._items.sort(key=key, reverse=reverse)

    def sort_by_id(self) -> None:
        self.sort(key=lambda x: self._get_item_id(x))

    def sort_by_balance(self) -> None:
        self.sort(key=lambda x: getattr(x, "balance", 0), reverse=True)
    
    def sort_by_interest_rate(self) -> None:
        self.sort(key=lambda x: getattr(x, "interest_rate", 0), reverse=True)

    def filter(self, predicate: Callable[[T], bool]) -> 'BankCollection[T]':
        new_collection = BankCollection(self._item_type, self._id_attr)
        for item in self._items:
            if predicate(item):
                new_collection.add(item)
        return new_collection

    def get_active_accounts(self) -> 'BankCollection[T]':
        return self.filter(lambda acc: getattr(acc, "is_active", False))

    def get_positive_balance(self) -> 'BankCollection[T]':
        return self.filter(lambda acc: getattr(acc, "balance", 0) > 0)

    def get_large_balance(self, min_balance: float = 100000) -> 'BankCollection[T]':
        return self.filter(lambda acc: getattr(acc, "balance", 0) >= min_balance)

    def __repr__(self):
        return f"BankCollection({self._item_type.__name__}, items={len(self._items)})"