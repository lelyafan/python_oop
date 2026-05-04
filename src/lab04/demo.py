"""
Демонстрация работы интерфейсов и абстрактных классов
Лабораторная работа №4 - оценка 5
"""
from interfaces import Printable, Comparable, InterestCalculable, Withdrawable, DepositCalculable
from models import BankAccount, JoinAccount, CurrencyAccount
from typing import List, Any


def print_separator(title: str):
    """Печать разделителя с заголовком"""
    print("\n" + "=" * 70)
    print(f"📌 {title}")
    print("=" * 70)


def universal_print(items: List[Printable]):
    """
    Универсальная функция, работающая через интерфейс Printable
    Принимает любой список объектов, реализующих Printable
    """
    print("\n📄 Вывод через универсальную функцию print_all():")
    for i, item in enumerate(items, 1):
        print(f"\n--- Объект {i} (кратко) ---")
        print(item.to_string(verbose=False))


def sort_by_balance(items: List[Comparable]) -> List[Comparable]:
    """
    Универсальная сортировка через интерфейс Comparable
    """
    return sorted(items, key=lambda x: x)


class BankCollection:
    """
    Коллекция банковских счетов (интеграция с ЛР-2)
    Поддерживает фильтрацию по интерфейсам
    """
    
    def __init__(self):
        self._accounts: List[BankAccount] = []
    
    def add(self, account: BankAccount):
        """Добавление счета в коллекцию"""
        self._accounts.append(account)
    
    def get_all(self) -> List[BankAccount]:
        """Получение всех счетов"""
        return self._accounts.copy()
    
    def get_printable(self) -> List[Printable]:
        """Фильтрация по интерфейсу Printable"""
        return [acc for acc in self._accounts if isinstance(acc, Printable)]
    
    def get_comparable(self) -> List[Comparable]:
        """Фильтрация по интерфейсу Comparable"""
        return [acc for acc in self._accounts if isinstance(acc, Comparable)]
    
    def get_interest_calculable(self) -> List[InterestCalculable]:
        """Фильтрация по интерфейсу InterestCalculable"""
        return [acc for acc in self._accounts if isinstance(acc, InterestCalculable)]
    
    def get_withdrawable(self) -> List[Withdrawable]:
        """Фильтрация по интерфейсу Withdrawable"""
        return [acc for acc in self._accounts if isinstance(acc, Withdrawable)]
    
    def get_deposit_calculable(self) -> List[DepositCalculable]:
        """Фильтрация по интерфейсу DepositCalculable"""
        return [acc for acc in self._accounts if isinstance(acc, DepositCalculable)]
    
    def __len__(self):
        return len(self._accounts)


def scenario_1_interfaces_basics():
    """Сценарий 1: Базовое создание и реализация интерфейсов"""
    print_separator("СЦЕНАРИЙ 1: СОЗДАНИЕ ОБЪЕКТОВ И ПРОВЕРКА РЕАЛИЗАЦИИ ИНТЕРФЕЙСОВ")
    
    # Создание объектов
    basic_acc = BankAccount("40817810123456789012", "Иванов Иван", 100000, 50000, 5.0)
    join_acc = JoinAccount("40817810987654321098", "Петрова Мария", 250000, 100000, 6.0,
                           co_owners=["Сидоров Алексей", "Кузнецова Елена"])
    currency_acc = CurrencyAccount("40817810555555555555", "Смирнов Дмитрий", 5000, 2000, 3.5, currency="USD")
    
    # Проверка реализации интерфейсов через isinstance
    objects = [basic_acc, join_acc, currency_acc]
    
    print("\n🔍 Проверка реализации интерфейсов через isinstance():")
    for obj in objects:
        print(f"\n📊 {type(obj).__name__}:")
        print(f"   Printable: {isinstance(obj, Printable)}")
        print(f"   Comparable: {isinstance(obj, Comparable)}")
        print(f"   InterestCalculable: {isinstance(obj, InterestCalculable)}")
        print(f"   Withdrawable: {isinstance(obj, Withdrawable)}")
        print(f"   DepositCalculable: {isinstance(obj, DepositCalculable)}")
        if isinstance(obj, JoinAccount):
            print(f"   Специфический метод: add_co_owner()")
        if isinstance(obj, CurrencyAccount):
            print(f"   Специфический метод: convert_to()")
    
    # Демонстрация метода to_string() (интерфейс Printable)
    print("\n📄 Демонстрация метода to_string() (Printable):")
    for obj in objects:
        print(f"\n{type(obj).__name__} (подробно):")
        print(obj.to_string(verbose=True))
        print(f"{type(obj).__name__} (кратко):")
        print(obj.to_string(verbose=False))


def scenario_2_universal_function():
    """Сценарий 2: Универсальная функция через интерфейс"""
    print_separator("СЦЕНАРИЙ 2: УНИВЕРСАЛЬНАЯ ФУНКЦИЯ ЧЕРЕЗ ИНТЕРФЕЙС PRINTABLE")
    
    accounts = [
        BankAccount("ACC001", "Иванов Иван", 100000, 50000, 5.0),
        JoinAccount("ACC002", "Петрова Мария", 250000, 100000, 6.0,
                   co_owners=["Сидоров А."]),
        CurrencyAccount("ACC003", "Смирнов Дмитрий", 5000, 2000, 3.5, currency="USD")
    ]
    
    # Универсальная функция работает с любыми Printable объектами
    universal_print(accounts)
    
    print("\n🔍 Демонстрация isinstance() для проверки типов:")
    for acc in accounts:
        if isinstance(acc, JoinAccount):
            print(f"   {acc.owner_name}: является JoinAccount")
        elif isinstance(acc, CurrencyAccount):
            print(f"   {acc.owner_name}: является CurrencyAccount")
        else:
            print(f"   {acc.owner_name}: является BankAccount")


def scenario_3_polymorphism_via_interfaces():
    """Сценарий 3: Полиморфизм через интерфейсы (без условий)"""
    print_separator("СЦЕНАРИЙ 3: ПОЛИМОРФИЗМ ЧЕРЕЗ ИНТЕРФЕЙСЫ (GOOD-ПАТТЕРН)")
    
    accounts = [
        BankAccount("B001", "Иванов Иван", 100000, 50000, 5.0),
        JoinAccount("J001", "Петрова Мария", 250000, 100000, 6.0,
                   co_owners=["Сидоров А."]),
        CurrencyAccount("C001", "Смирнов Дмитрий", 5000, 2000, 3.5, currency="USD")
    ]
    
    # ХОРОШО: работа через интерфейс InterestCalculable
    print("\n✅ GOOD-ПАТТЕРН: вызов через интерфейс InterestCalculable")
    for acc in accounts:
        if isinstance(acc, InterestCalculable):
            print(f"\n📊 {type(acc).__name__}:")
            result = acc.process_monthly()
            print(f"   Результат: {result['type']}")
            print(f"   Проценты: {result['interest']:.2f}")
    
    # ХОРОШО: работа через интерфейс Withdrawable
    print("\n✅ GOOD-ПАТТЕРН: вызов через интерфейс Withdrawable")
    for acc in accounts:
        if isinstance(acc, Withdrawable):
            print(f"\n💳 {type(acc).__name__}:")
            acc.withdraw(10000)
    
    # ПЛОХО (для демонстрации) - анти-паттерн
    print("\n❌ АНТИ-ПАТТЕРН (так делать НЕ нужно):")
    print("   if type(account) == JoinAccount:")
    print("       account.process_with_bonus()")
    print("   elif type(account) == CurrencyAccount:")
    print("       account.process_with_currency()")
    
    print("\n✅ GOOD-ПАТТЕРН (правильный подход):")
    print("   if isinstance(account, InterestCalculable):")
    print("       result = account.process_monthly()")


def scenario_4_collection_integration():
    """Сценарий 4: Интеграция с коллекцией и фильтрация по интерфейсам"""
    print_separator("СЦЕНАРИЙ 4: КОЛЛЕКЦИЯ И ФИЛЬТРАЦИЯ ПО ИНТЕРФЕЙСАМ")
    
    # Создание коллекции
    collection = BankCollection()
    
    # Добавление счетов разных типов
    collection.add(BankAccount("B001", "Иванов Иван", 100000, 50000, 5.0))
    collection.add(JoinAccount("J001", "Петрова Мария", 250000, 100000, 6.0,
                               co_owners=["Сидоров А.", "Кузнецова Е."]))
    collection.add(CurrencyAccount("C001", "Смирнов Дмитрий", 5000, 2000, 3.5, currency="USD"))
    collection.add(JoinAccount("J002", "Козлов Андрей", 150000, 80000, 5.5,
                               co_owners=["Новикова И."]))
    collection.add(CurrencyAccount("C002", "Воробьева Анна", 7500, 3000, 4.0, currency="EUR"))
    
    print(f"📊 Всего счетов в коллекции: {len(collection)}")
    
    # Фильтрация по интерфейсу Printable
    printable_items = collection.get_printable()
    print(f"\n📄 Printable объекты ({len(printable_items)}):")
    for item in printable_items:
        print(f"   - {item.to_string(verbose=False)}")
    
    # Фильтрация по интерфейсу Comparable
    comparable_items = collection.get_comparable()
    print(f"\n🔍 Comparable объекты ({len(comparable_items)}):")
    for item in comparable_items:
        print(f"   - {item.owner_name}: баланс {item.balance:.2f}")
    
    # Фильтрация по интерфейсу InterestCalculable
    interest_items = collection.get_interest_calculable()
    print(f"\n📈 InterestCalculable объекты ({len(interest_items)}):")
    for item in interest_items:
        print(f"   - {item.owner_name}: ставка {item.interest_rate}%")
    
    # Фильтрация по интерфейсу DepositCalculable
    deposit_items = collection.get_deposit_calculable()
    print(f"\n💰 DepositCalculable объекты ({len(deposit_items)}):")
    for item in deposit_items:
        forecast = item.get_profit_forecast(6)
        print(f"   - {item.owner_name}: прогноз прибыли за 6 мес: {forecast:.2f}")


def scenario_5_sorting_and_advanced():
    """Сценарий 5: Сортировка через Comparable и множественная реализация"""
    print_separator("СЦЕНАРИЙ 5: СОРТИРОВКА ЧЕРЕЗ COMPARABLE И МНОЖЕСТВЕННАЯ РЕАЛИЗАЦИЯ")
    
    # Создание списка для сортировки
    accounts = [
        BankAccount("B003", "Зайцев Петр", 50000, 30000, 4.0),
        BankAccount("B001", "Иванов Иван", 100000, 50000, 5.0),
        BankAccount("B002", "Петрова Мария", 75000, 40000, 4.5),
    ]
    
    print("\n📊 Исходный список (по порядку создания):")
    for acc in accounts:
        print(f"   {acc.owner_name}: {acc.balance:.2f} руб.")
    
    # Сортировка через интерфейс Comparable
    # NOTE: Python sorted использует __lt__, поэтому для демонстрации используем key
    print("\n📊 Отсортированный список (по балансу, через интерфейс Comparable):")
    sorted_accounts = sorted(accounts, key=lambda x: x.balance)
    for acc in sorted_accounts:
        print(f"   {acc.owner_name}: {acc.balance:.2f} руб.")
    
    # Демонстрация множественной реализации интерфейсов
    print("\n🔍 Множественная реализация интерфейсов (Multiple Inheritance):")
    currency_acc = CurrencyAccount("C999", "Трейдеров Валерий", 10000, 5000, 5.0, currency="USD")
    
    print(f"\n   Класс CurrencyAccount реализует:")
    print(f"   - Printable ({isinstance(currency_acc, Printable)})")
    print(f"   - Comparable ({isinstance(currency_acc, Comparable)})")
    print(f"   - InterestCalculable ({isinstance(currency_acc, InterestCalculable)})")
    print(f"   - Withdrawable ({isinstance(currency_acc, Withdrawable)})")
    print(f"   - DepositCalculable ({isinstance(currency_acc, DepositCalculable)})")
    
    # Демонстрация прогноза прибыли (интерфейс DepositCalculable)
    print("\n💰 Демонстрация прогноза прибыли (интерфейс DepositCalculable):")
    for acc in [BankAccount("D001", "Консервативный", 100000, 0, 5.0),
                JoinAccount("D002", "Совместный", 100000, 50000, 6.0, ["Совладелец"]),
                CurrencyAccount("D003", "Валютный", 1000, 0, 4.0, currency="USD")]:
        
        print(f"\n   {type(acc).__name__}: {acc.owner_name}")
        if isinstance(acc, DepositCalculable):
            for months in [3, 6, 12]:
                profit = acc.get_profit_forecast(months)
                print(f"      Прибыль за {months} мес: {profit:.2f} {'руб.' if not isinstance(acc, CurrencyAccount) else 'USD'}")


def main():
    """Главная функция демонстрации"""
    print("\n" + "=" * 80)
    print("🏦 ЛАБОРАТОРНАЯ РАБОТА №4 - ИНТЕРФЕЙСЫ И АБСТРАКТНЫЕ КЛАССЫ (ABC)")
    print("Реализованные интерфейсы: Printable, Comparable, InterestCalculable, Withdrawable, DepositCalculable")
    print("=" * 80)
    
    scenarios = [
        ("Базовое создание и реализация интерфейсов", scenario_1_interfaces_basics),
        ("Универсальная функция через интерфейс Printable", scenario_2_universal_function),
        ("Полиморфизм через интерфейсы (Good-паттерн)", scenario_3_polymorphism_via_interfaces),
        ("Интеграция с коллекцией и фильтрация", scenario_4_collection_integration),
        ("Сортировка через Comparable и множественная реализация", scenario_5_sorting_and_advanced)
    ]
    
    for name, func in scenarios:
        try:
            func()
        except Exception as e:
            print(f"\n❌ Ошибка в {name}: {e}")

if __name__ == "__main__":
    main()