from base import BankAccount
from models import JoinAccount, CurrencyAccount


def print_separator(title: str):
    """Печать разделителя с заголовком"""
    print("\n" + "=" * 60)
    print(f"📌 {title}")
    print("=" * 60)


def demonstrate_inheritance():
    """Сценарий 1: Демонстрация базовых возможностей наследования"""
    print_separator("СЦЕНАРИЙ 1: СОЗДАНИЕ ОБЪЕКТОВ РАЗНЫХ ТИПОВ")
    
    # Создание базового счета
    basic_acc = BankAccount("40817810123456789012", "Иванов Иван", 100000, 50000, 5.0)
    print("🏦 Базовый счет:")
    print(basic_acc)
    
    # Создание совместного счета
    join_acc = JoinAccount(
        "40817810987654321098", 
        "Петрова Мария", 
        250000, 
        100000, 
        6.0,
        co_owners=["Сидоров Алексей", "Кузнецова Елена"],
        withdrawal_limit=75000
    )
    print("\n👥 Совместный счет:")
    print(join_acc)
    
    # Создание валютного счета
    currency_acc = CurrencyAccount(
        "40817810555555555555",
        "Смирнов Дмитрий",
        5000,
        2000,
        3.5,
        currency="USD"
    )
    print("\n💵 Валютный счет:")
    print(currency_acc)


def demonstrate_polymorphism():
    """Сценарий 2: Демонстрация полиморфного поведения"""
    print_separator("СЦЕНАРИЙ 2: ПОЛИМОРФИЗМ")
    
    accounts = [
        BankAccount("ACC001", "Иванов Иван", 100000, 50000, 5.0),
        JoinAccount("ACC002", "Петрова Мария", 250000, 100000, 6.0, 
                   co_owners=["Сидоров А."], withdrawal_limit=75000),
        CurrencyAccount("ACC003", "Смирнов Дмитрий", 5000, 2000, 3.5, currency="USD")
    ]
    
    for i, account in enumerate(accounts, 1):
        print(f"\n📊 Счет {i} ({type(account).__name__}):")
        print(f"   Баланс до: {account.balance:,.2f}")
        
        # Вызов одного и того же метода - разное поведение!
        result = account.process_monthly()
        
        print(f"   Тип операции: {result['type']}")
        print(f"   Проценты: {result['interest']:.2f}")
        if 'bonus' in result:
            print(f"   Бонус: {result['bonus']:.2f}")
        if 'old_rate' in result:
            print(f"   Изменение курса: {result['old_rate']:.2f} -> {result['new_rate']:.2f}")
        print(f"   Баланс после: {account.balance:,.2f}")


def demonstrate_type_checking():
    """Сценарий 3: Демонстрация проверки типов через isinstance"""
    print_separator("СЦЕНАРИЙ 3: ПРОВЕРКА ТИПОВ И ФИЛЬТРАЦИЯ")
    
    accounts = [
        BankAccount("B001", "Иванов Иван", 100000, 50000, 5.0),
        JoinAccount("J001", "Петрова Мария", 250000, 100000, 6.0, 
                   co_owners=["Сидоров А."]),
        CurrencyAccount("C001", "Смирнов Дмитрий", 5000, 2000, 3.5, currency="USD"),
        JoinAccount("J002", "Кузнецова Елена", 300000, 150000, 6.5,
                   co_owners=["Морозов П.", "Волкова А."]),
        CurrencyAccount("C002", "Соколов Антон", 10000, 5000, 4.0, currency="EUR")
    ]
    
    print(f"📊 Всего счетов: {len(accounts)}")
    
    # Фильтрация по типу
    join_accounts = [acc for acc in accounts if isinstance(acc, JoinAccount)]
    currency_accounts = [acc for acc in accounts if isinstance(acc, CurrencyAccount)]
    basic_accounts = [acc for acc in accounts if type(acc) == BankAccount and not isinstance(acc, (JoinAccount, CurrencyAccount))]
    
    print(f"\n👥 Совместные счета ({len(join_accounts)}):")
    for acc in join_accounts:
        print(f"   - {acc.owner_name} (совладельцы: {len(acc.co_owners)})")
    
    print(f"\n💵 Валютные счета ({len(currency_accounts)}):")
    for acc in currency_accounts:
        print(f"   - {acc.owner_name} ({acc.currency})")
    
    print(f"\n🏦 Обычные счета ({len(basic_accounts)}):")
    for acc in basic_accounts:
        print(f"   - {acc.owner_name}")
    
    # Проверка конкретных типов
    print("\n🔍 Проверка типов:")
    for acc in accounts[:3]:
        if isinstance(acc, JoinAccount):
            print(f"   {acc.owner_name}: является совместным счетом")
        elif isinstance(acc, CurrencyAccount):
            print(f"   {acc.owner_name}: является валютным счетом")
        else:
            print(f"   {acc.owner_name}: является базовым счетом")


def demonstrate_collection_integration():
    """Сценарий 4: Интеграция с коллекцией и единый интерфейс"""
    print_separator("СЦЕНАРИЙ 4: РАБОТА С КОЛЛЕКЦИЕЙ И ЕДИНЫЙ ИНТЕРФЕЙС")
    
    # Создание коллекции разных типов счетов
    accounts = [
        BankAccount("40817810123456789012", "Иванов Иван", 100000, 50000, 5.0),
        JoinAccount("40817810987654321098", "Петрова Мария", 250000, 100000, 6.0,
                   co_owners=["Сидоров А.", "Кузнецова Е."], withdrawal_limit=75000),
        CurrencyAccount("40817810555555555555", "Смирнов Дмитрий", 5000, 2000, 3.5, currency="USD"),
        JoinAccount("40817810333333333333", "Козлов Андрей", 150000, 80000, 5.5,
                   co_owners=["Новикова И."], withdrawal_limit=50000),
        CurrencyAccount("40817810777777777777", "Воробьева Анна", 7500, 3000, 4.0, currency="EUR")
    ]
    
    print("📊 Все счета в коллекции:")
    for i, acc in enumerate(accounts, 1):
        print(f"\n   {i}. {type(acc).__name__}")
        print(f"      Владелец: {acc.owner_name}")
        print(f"      Баланс: {acc.balance:,.2f} руб.")
        if hasattr(acc, 'currency'):
            print(f"      Валюта: {acc.currency}")
        if hasattr(acc, 'co_owners'):
            print(f"      Совладельцев: {len(acc.co_owners)}")
    
    # Демонстрация единого интерфейса (полиморфизм без условий)
    print("\n" + "=" * 60)
    print("🔄 Единый интерфейс: выполнение операций со всеми счетами")
    print("=" * 60)
    
    for acc in accounts:
        print(f"\n💼 Счет {acc.account_number} ({type(acc).__name__}):")
        try:
            # Все счета поддерживают единый интерфейс
            print(f"   Пополнение на 10000...")
            acc.deposit(10000)
            print(f"   Пробуем снять 25000...")
            acc.withdraw(25000)
            print(f"   Итоговый баланс: {acc.balance:,.2f}")
        except Exception as e:
            print(f"   ❌ Ошибка: {e}")


def demonstrate_specific_methods():
    """Сценарий 5: Демонстрация специфических методов дочерних классов"""
    print_separator("СЦЕНАРИЙ 5: СПЕЦИФИЧЕСКИЕ МЕТОДЫ ДОЧЕРНИХ КЛАССОВ")
    
    # Демонстрация методов JoinAccount
    print("\n👥 JoinAccount - работа с совладельцами:")
    join_acc = JoinAccount("J999", "Главный Владелец", 500000, 200000, 7.0,
                           co_owners=["Владелец 1"], withdrawal_limit=100000)
    print(join_acc)
    
    print("\n   ➕ Добавляем нового совладельца...")
    join_acc.add_co_owner("Владелец 2")
    
    print("   ➕ Добавляем еще одного...")
    join_acc.add_co_owner("Владелец 3")
    
    print("\n   ❌ Удаляем совладельца...")
    join_acc.remove_co_owner("Владелец 1")
    
    print("\n   Итоговый список совладельцев:")
    print(f"   {join_acc.co_owners}")
    
    # Демонстрация методов CurrencyAccount
    print("\n" + "-" * 40)
    print("\n💱 CurrencyAccount - работа с валютами:")
    curr_acc = CurrencyAccount("C999", "Валютный Трейдер", 10000, 5000, 3.0, currency="USD")
    print(curr_acc)
    
    print("\n   💰 Баланс в рублях:")
    print(f"   {curr_acc.get_balance_in_rub():,.2f} RUB")
    
    print("\n   🔄 Конвертация в EUR:")
    converted = curr_acc.convert_to("EUR")
    print(f"   {curr_acc.balance} USD = {converted:.2f} EUR")
    
    print("\n   🔄 Конвертация в CNY:")
    converted = curr_acc.convert_to("CNY")
    print(f"   {curr_acc.balance} USD = {converted:.2f} CNY")


def main():
    """Главная функция демонстрации"""
    print("\n" + "=" * 80)
    print("🏦 ЛАБОРАТОРНАЯ РАБОТА №3 - НАСЛЕДОВАНИЕ И ПОЛИМОРФИЗМ")
    print("Базовый класс: BankAccount | Дочерние: JoinAccount, CurrencyAccount")
    print("=" * 80)
    
    demonstrations = [
        ("Демонстрация наследования", demonstrate_inheritance),
        ("Полиморфное поведение", demonstrate_polymorphism),
        ("Проверка типов и фильтрация", demonstrate_type_checking),
        ("Работа с коллекцией", demonstrate_collection_integration),
        ("Специфические методы дочерних классов", demonstrate_specific_methods)
    ]
    
    for name, func in demonstrations:
        try:
            func()
        except Exception as e:
            print(f"\n❌ Ошибка в {name}: {e}")

if __name__ == "__main__":
    main()