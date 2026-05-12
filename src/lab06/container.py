from typing import TypeVar, Generic, Callable, Optional, Protocol, List

class Displayable(Protocol):
    def display(self) -> str:
        ...

class Scorable(Protocol):
    def score(self) -> float:
        ...

D = TypeVar('D', bound=Displayable)
S = TypeVar('S', bound=Scorable)
T = TypeVar('T')
R = TypeVar('R')

class TypedCollection(Generic[T]):
    def __init__(self) -> None:
        self._items: List[T] = []
    
    def add(self, item: T) -> None:
        self._items.append(item)
        print(f"✓ Добавлен элемент в коллекцию")
    
    def remove(self, item: T) -> None:
        if item not in self._items:
            raise ValueError(f"Элемент не найден в коллекции")
        self._items.remove(item)
        print(f"✗ Элемент удален из коллекции")
    
    def get_all(self) -> List[T]:
        return self._items.copy()
    
    def size(self) -> int:
        return len(self._items)
    
    def clear(self) -> None:
        self._items.clear()
        print("Коллекция очищена")
    
    def contains(self, item: T) -> bool:
        return item in self._items
    
    def __len__(self) -> int:
        return len(self._items)
    
    def __iter__(self):
        return iter(self._items)
    
    def find(self, predicate: Callable[[T], bool]) -> Optional[T]:
        for item in self._items:
            if predicate(item):
                return item
        return None
    
    def filter(self, predicate: Callable[[T], bool]) -> List[T]:
        return [item for item in self._items if predicate(item)]
    
    def map(self, transform: Callable[[T], R]) -> List[R]:
        return [transform(item) for item in self._items]
    
    def first(self) -> Optional[T]:
        return self._items[0] if self._items else None
    
    def last(self) -> Optional[T]:
        return self._items[-1] if self._items else None
    
    def __str__(self) -> str:
        if not self._items:
            return "TypedCollection[]"
        return f"TypedCollection[{len(self._items)} элементов]"