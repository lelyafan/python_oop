from container import TypedCollection, Displayable, Scorable, D, S
from typing import Optional, List
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lib.models import JoinAccount, CurrencyAccount

def join_account_display(self) -> str:
    return (f"🔗 Совместный счет: {self._account_number}\n"
            f"   Владелец: {self._owner_name}\n"
            f"   Совладельцы: {', '.join(self._co_owners) if self._co_owners else 'нет'}\n"
            f"   Баланс: {self._balance:,.2f} руб.\n"
            f"   Статус: {'Активен' if self._is_active else 'Закрыт'}")

def join_account_score(self) -> float:
    score = 5.0
    if self._balance > 100000:
        score += 2.0
    elif self._balance > 50000:
        score += 1.0
    if len(self._co_owners) > 0:
        score += min(len(self._co_owners) * 0.5, 2.0)
    return min(score, 10.0)

def currency_account_display(self) -> str:
    return (f"💱 Валютный счет: {self._account_number}\n"
            f"   Владелец: {self._owner_name}\n"
            f"   Валюта: {self._currency}\n"
            f"   Баланс: {self._balance:.2f} {self._currency}\n"
            f"   Курс к RUB: {self._exchange_rate:.2f}\n"
            f"   Эквивалент в RUB: {self.get_balance_in_rub():,.2f} руб.\n"
            f"   Статус: {'Активен' if self._is_active else 'Закрыт'}")

def currency_account_score(self) -> float:
    score = 5.0
    if self._currency == 'USD':
        score += 1.0
    elif self._currency == 'EUR':
        score += 1.5
    rub_balance = self.get_balance_in_rub()
    if rub_balance > 200000:
        score += 2.0
    elif rub_balance > 100000:
        score += 1.0
    return min(score, 10.0)

JoinAccount.display = join_account_display
JoinAccount.score = join_account_score
CurrencyAccount.display = currency_account_display
CurrencyAccount.score = currency_account_score

class Student:
    def __init__(self, name: str, gpa: float, year: int, student_id: str):
        self._name = name
        self._gpa = gpa
        self._year = year
        self._student_id = student_id
    
    def get_name(self) -> str:
        return self._name
    
    def get_gpa(self) -> float:
        return self._gpa
    
    def get_year(self) -> int:
        return self._year
    
    def display(self) -> str:
        return f"👨‍🎓 Студент: {self._name}, ID: {self._student_id}, Курс: {self._year}, GPA: {self._gpa}"
    
    def score(self) -> float:
        return self._gpa
    
    def __str__(self):
        return self.display()

def demonstrate_basic_generics():
    print("\n" + "="*60)
    print("ЗАДАНИЯ 3 И 4: Базовая Generic-коллекция")
    print("="*60)
    
    students = TypedCollection[Student]()
    
    print("\n--- Добавление студентов ---")
    students.add(Student("Иван Петров", 4.8, 3, "S001"))
    students.add(Student("Мария Сидорова", 4.9, 3, "S002"))
    students.add(Student("Алексей Иванов", 4.2, 2, "S003"))
    students.add(Student("Елена Смирнова", 5.0, 4, "S004"))
    
    print(f"\nВсего студентов: {students.size()}")
    print(f"Коллекция: {students}")
    
    print("\n--- Демонстрация find() ---")
    
    found = students.find(lambda s: s.get_gpa() > 4.8)
    if found:
        print(f"Найден студент с GPA > 4.8: {found.display()}")
    else:
        print("Студент с GPA > 4.8 не найден")
    
    not_found = students.find(lambda s: s.get_gpa() > 5.5)
    if not_found is None:
        print("Студент с GPA > 5.5 не найден (вернулся None)")
    
    print("\n--- Демонстрация filter() ---")
    high_performers = students.filter(lambda s: s.get_gpa() >= 4.7)
    print(f"Студенты с высоким GPA (>= 4.7): {len(high_performers)} чел.")
    for s in high_performers:
        print(f"  • {s.get_name()} - GPA: {s.get_gpa()}")
    
    print("\n--- Демонстрация map() и изменения типа результата ---")
    
    names = students.map(lambda s: s.get_name())
    print(f"Имена студентов: {names}")
    print(f"  Тип результата: {type(names).__name__}[{type(names[0]).__name__}]")
    
    gpas = students.map(lambda s: s.get_gpa())
    print(f"GPA студентов: {gpas}")
    print(f"  Тип результата: {type(gpas).__name__}[{type(gpas[0]).__name__}]")
    
    student_info = students.map(lambda s: (s.get_name(), s.get_gpa(), s.get_year()))
    print(f"Информация о студентах: {student_info}")
    print(f"  Тип результата: {type(student_info).__name__}[{type(student_info[0]).__name__}]")

def demonstrate_protocol_displayable():
    print("\n" + "="*60)
    print("ЗАДАНИЕ 5: Протокол Displayable")
    print("="*60)
    
    displayable_collection = TypedCollection[D]()
    
    print("\n--- Создание объектов разных типов ---")
    
    join_acc = JoinAccount(
        account_number="JOINT001",
        owner_name="Иван Петров",
        initial_balance=150000.0,
        credit_limit=50000.0,
        interest_rate=5.0,
        co_owners=["Мария Сидорова", "Алексей Иванов"],
        withdrawal_limit=30000.0
    )
    
    currency_acc = CurrencyAccount(
        account_number="CURR001",
        owner_name="Елена Смирнова",
        initial_balance=1500.0,
        credit_limit=2000.0,
        interest_rate=3.5,
        currency="USD"
    )
    
    student = Student("Петр Иванов", 4.5, 2, "S005")
    
    print("\n--- Добавление объектов в TypedCollection[D] ---")
    displayable_collection.add(join_acc)
    displayable_collection.add(currency_acc)
    displayable_collection.add(student)
    
    print(f"\nВсего объектов в коллекции: {displayable_collection.size()}")
    print("Объекты добавлены без наследования от Displayable!\n")
    
    print("--- Вызов display() для каждого объекта ---")
    for i, obj in enumerate(displayable_collection.get_all(), 1):
        print(f"{i}. {obj.display()}")
        print()
    
    print("--- Преобразование с помощью map() ---")
    displays = displayable_collection.map(lambda obj: obj.display())
    for i, display_str in enumerate(displays, 1):
        print(f"{i}. {display_str[:100]}..." if len(display_str) > 100 else f"{i}. {display_str}")
        print()
    
    print("--- Фильтрация объектов ---")
    key_objects = displayable_collection.filter(
        lambda obj: "совместный" in obj.display().lower() or 
                   "валютный" in obj.display().lower()
    )
    print(f"Найдено банковских счетов: {len(key_objects)}")
    for obj in key_objects:
        print(f"  • {obj.display().split(chr(10))[0]}")

def demonstrate_protocol_scorable():
    print("\n" + "="*60)
    print("ЗАДАНИЕ 5: Протокол Scorable")
    print("="*60)
    
    scorable_collection = TypedCollection[S]()
    
    print("\n--- Создание объектов с методом score() ---")
    
    join_acc1 = JoinAccount(
        account_number="JOINT002",
        owner_name="Алексей Иванов",
        initial_balance=250000.0,
        credit_limit=100000.0,
        interest_rate=5.0,
        co_owners=["Петр Сидоров", "Ирина Козлова", "Михаил Ветров"],
        withdrawal_limit=50000.0
    )
    
    currency_acc1 = CurrencyAccount(
        account_number="CURR002",
        owner_name="Ольга Новикова",
        initial_balance=2500.0,
        credit_limit=3000.0,
        interest_rate=4.0,
        currency="EUR"
    )
    
    currency_acc2 = CurrencyAccount(
        account_number="CURR003",
        owner_name="Дмитрий Морозов",
        initial_balance=800.0,
        credit_limit=1000.0,
        interest_rate=3.0,
        currency="USD"
    )
    
    print("--- Добавление объектов в TypedCollection[S] ---")
    scorable_collection.add(join_acc1)
    scorable_collection.add(currency_acc1)
    scorable_collection.add(currency_acc2)
    
    print(f"\nВсего объектов в коллекции: {scorable_collection.size()}\n")
    
    print("--- Оценки объектов ---")
    for obj in scorable_collection.get_all():
        if hasattr(obj, 'display'):
            print(f"Объект: {obj.display().split(chr(10))[0]}")
        print(f"  Score: {obj.score():.2f}/10.0")
        print()
    
    print("--- Получение всех оценок через map() ---")
    scores = scorable_collection.map(lambda obj: obj.score())
    print(f"Оценки всех объектов: {scores}")
    print(f"Средняя оценка: {sum(scores)/len(scores):.2f}/10.0")
    
    print("\n--- Поиск объекта с максимальной оценкой ---")
    max_score_obj = scorable_collection.find(
        lambda obj: obj.score() == max([obj.score() for obj in scorable_collection.get_all()])
    )
    if max_score_obj:
        print(f"Объект с максимальной оценкой ({max_score_obj.score():.2f}/10.0):")
        print(f"  {max_score_obj.display().split(chr(10))[0]}")
    
    print("\n--- Фильтрация объектов с оценкой >= 7.0 ---")
    high_score_objects = scorable_collection.filter(lambda obj: obj.score() >= 7.0)
    print(f"Найдено {len(high_score_objects)} объектов:")
    for obj in high_score_objects:
        if hasattr(obj, 'display'):
            print(f"  • {obj.display().split(chr(10))[0]} -> {obj.score():.2f}")
    
    print("\n--- Один класс TypedCollection с разными ограничениями ---")
    print("TypedCollection[D] - для Displayable объектов")
    print("TypedCollection[S] - для Scorable объектов")

def demonstrate_type_safety():
    print("\n" + "="*60)
    print("ДОПОЛНИТЕЛЬНО: Type Safety")
    print("="*60)
    
    print("\n--- Примеры типизированных коллекций ---")
    
    string_collection = TypedCollection[str]()
    string_collection.add("Hello")
    string_collection.add("World")
    print(f"String collection: {string_collection.get_all()}")
    
    number_collection = TypedCollection[int]()
    number_collection.add(42)
    number_collection.add(100)
    print(f"Number collection: {number_collection.get_all()}")
    
    float_collection = TypedCollection[float]()
    float_collection.add(3.14)
    float_collection.add(2.718)
    print(f"Float collection: {float_collection.get_all()}")
    
    print("\n--- Преимущества типизации ---")
    print("1. IDE подсказывает доступные методы")
    print("2. Статический анализатор находит ошибки до выполнения")
    print("3. Код становится самодокументируемым")
    print("4. Упрощается рефакторинг и поддержка кода")

def main():
    print("\n" + "█"*70)
    print("ЛАБОРАТОРНАЯ РАБОТА №6 - Generics и typing")
    print("█"*70)
    
    demonstrate_basic_generics()
    demonstrate_protocol_displayable()
    demonstrate_protocol_scorable()
    demonstrate_type_safety()
    
    print("\n" + "█"*70)
    print("ДЕМОНСТРАЦИЯ ЗАВЕРШЕНА")
    print("█"*70)

if __name__ == "__main__":
    main()