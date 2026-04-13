from typing import TypeVar, Generic, List, Optional, Callable

T = TypeVar('T')


class BankCollection(Generic[T]):

    def __init__(self, item_type: type, id_attr: str = "account_id"):
        """
        :param item_type: допустимый тип объектов (например, BankAccount)
        :param id_attr: имя атрибута для проверки уникальности (например, "account_id")
        """
        self._items: List[T] = []
        self._item_type = item_type
        self._id_attr = id_attr

    def _get_item_id(self, item: T):
        "Получить идентификатор объекта для проверки дубликатов"
        return getattr(item, self._id_attr)

    def add(self, item: T) -> None:
        "Добавить объект с проверкой типа и уникальности"
        if not isinstance(item, self._item_type):
            raise TypeError(f"Можно добавлять только объекты типа {self._item_type.__name__}")

        item_id = self._get_item_id(item)
        if any(self._get_item_id(existing) == item_id for existing in self._items):
            raise ValueError(f"Объект с {self._id_attr}={item_id} уже существует в коллекции")

        self._items.append(item)

    def remove(self, item: T) -> None:
        """Удалить объект"""
        if item not in self._items:
            raise ValueError("Объект не найден в коллекции")
        self._items.remove(item)

    def remove_at(self, index: int) -> None:
        """Удаление по индексу"""
        if index < 0 or index >= len(self._items):
            raise IndexError("Индекс вне диапазона")
        del self._items[index]

    def get_all(self) -> List[T]:
        """Вернуть список всех объектов"""
        return self._items.copy()

    def find_by(self, **kwargs) -> Optional[T]:
        """
        Поиск по одному или нескольким атрибутам.
        Пример: collection.find_by(account_id=101)
        """
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
        """Найти все объекты, соответствующие критериям"""
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

    # Магические методы
    def __len__(self) -> int:
        return len(self._items)

    def __iter__(self):
        return iter(self._items)

    def __getitem__(self, index):
        """Поддержка индексации collection[0], collection[1:3]"""
        if isinstance(index, slice):
            result = BankCollection(self._item_type, self._id_attr)
            result._items = self._items[index]
            return result
        if index < 0 or index >= len(self._items):
            raise IndexError("Индекс вне диапазона")
        return self._items[index]

    # Сортировка
    def sort(self, key: Callable[[T], any], reverse: bool = False) -> None:
        """Универсальная сортировка по ключу"""
        self._items.sort(key=key, reverse=reverse)

    def sort_by_id(self) -> None:
        """Сортировка по идентификатору"""
        self.sort(key=lambda x: self._get_item_id(x))

    def sort_by_balance(self) -> None:  # Для BankAccount
        self.sort(key=lambda x: getattr(x, "balance", 0), reverse=True)

    # Фильтрация — возвращают новую коллекцию
    def filter(self, predicate: Callable[[T], bool]) -> 'BankCollection[T]':
        """Вернуть новую коллекцию с элементами, удовлетворяющими условию"""
        new_collection = BankCollection(self._item_type, self._id_attr)
        for item in self._items:
            if predicate(item):
                new_collection.add(item)
        return new_collection

    def get_active_accounts(self) -> 'BankCollection[T]':
        """Получить счета с положительным балансом"""
        return self.filter(lambda acc: getattr(acc, "balance", 0) > 0)

    def get_available_credits(self) -> 'BankCollection[T]':
        """Получить кредиты с доступным лимитом"""
        def has_available_limit(credit):
            return hasattr(credit, "used_amount") and credit.used_amount < credit.limit
        return self.filter(has_available_limit)

    def get_large_deposits(self, min_amount: float = 100000) -> 'BankCollection[T]':
        """Получить крупные депозиты"""
        return self.filter(lambda dep: getattr(dep, "amount", 0) >= min_amount)

    def __repr__(self):
        return f"BankCollection({self._item_type.__name__}, items={len(self._items)})"