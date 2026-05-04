from container import BankCollection
from models import BankAccount, JoinAccount, CurrencyAccount
from typing import List


def print_separator(title: str):
    print("\n" + "=" * 80)
    print(f"📌 {title}")
    print("=" * 80)


def scenario_1_basic_collection():
    print_separator("СЦЕНАРИЙ 1: БАЗОВЫЕ ОПЕРАЦИИ С КОЛЛЕКЦИЕЙ")
    
    collection = BankCollection(BankAccount, "account_number")
    
    acc1 = BankAccount("40817810123456789012", "Иванов Иван", 100000, 50000, 5.0)
    acc2 = BankAccount("40817810123456789013", "Петров Петр", 50000, 30000, 4.5)
    acc3 = BankAccount("40817810123456789014", "Сидоров Алексей", 200000, 100000, 6.0)
    
    collection.add(acc1)
    collection.add(acc2)
    collection.add(acc3)
    
    print("📊 Коллекция после добавления:")
    print(f"   Размер: {len(collection)}")
    print(f"   Репрезентация: {collection}")

    print("\n📋 Все счета:")
    for acc in collection.get_all():
        print(f"   - {acc.account_number} | {acc.owner_name} | {acc.balance:.2f} руб.")

    print("\n🔍 Поиск счета по owner_name='Петров Петр':")
    found = collection.find_by(owner_name="Петров Петр")
    if found:
        print(f"   Найден: {found.account_number}")
    
    print("\n🗑️ Удаление счета Петрова Петра...")
    collection.remove(acc2)
    print(f"   Размер после удаления: {len(collection)}")
    
    print("\n🔄 Попытка добавить дубликат:")
    try:
        collection.add(acc1)
    except ValueError as e:
        print(f"   ❌ Ошибка: {e}")


def scenario_2_sorting():
    print_separator("СЦЕНАРИЙ 2: СОРТИРОВКА КОЛЛЕКЦИИ")
    
    collection = BankCollection(BankAccount, "account_number")
    
    accounts = [
        BankAccount("C001", "Воробьев", 50000, 30000, 4.0),
        BankAccount("A002", "Алексеев", 200000, 100000, 6.0),
        BankAccount("B003", "Борисов", 75000, 40000, 5.0),
    ]
    
    for acc in accounts:
        collection.add(acc)
    
    print("📊 Исходный порядок:")
    for acc in collection:
        print(f"   {acc.account_number} | {acc.owner_name} | {acc.balance:.2f} руб.")
    
    print("\n📊 Сортировка по ID (account_number):")
    collection.sort_by_id()
    for acc in collection:
        print(f"   {acc.account_number} | {acc.owner_name} | {acc.balance:.2f} руб.")
    
    print("\n📊 Сортировка по балансу (по убыванию):")
    collection.sort_by_balance()
    for acc in collection:
        print(f"   {acc.account_number} | {acc.owner_name} | {acc.balance:.2f} руб.")
    
    print("\n📊 Сортировка по процентной ставке (по убыванию):")
    collection.sort_by_interest_rate()
    for acc in collection:
        print(f"   {acc.account_number} | {acc.owner_name} | {acc.interest_rate:.1f}%")


def scenario_3_filtering():
    print_separator("СЦЕНАРИЙ 3: ФИЛЬТРАЦИЯ КОЛЛЕКЦИИ")
    
    collection = BankCollection(BankAccount, "account_number")
    
    accounts = [
        BankAccount("001", "Бедный", 1000, 10000, 5.0),
        BankAccount("002", "Средний", 50000, 30000, 5.0),
        BankAccount("003", "Богатый", 150000, 100000, 5.0),
        BankAccount("004", "Очень богатый", 500000, 200000, 5.0),
        BankAccount("005", "С нулевым", 0, 5000, 5.0),
    ]
    
    for acc in accounts:
        collection.add(acc)
    
    print("📊 Все счета:")
    for acc in collection:
        print(f"   {acc.owner_name}: {acc.balance:.2f} руб.")
    
    print("\n📊 Активные счета (is_active=True):")
    active = collection.get_active_accounts()
    for acc in active:
        print(f"   {acc.owner_name}: {acc.balance:.2f} руб.")
    
    print("\n📊 Счета с положительным балансом:")
    positive = collection.get_positive_balance()
    for acc in positive:
        print(f"   {acc.owner_name}: {acc.balance:.2f} руб.")
    
    print("\n📊 Крупные счета (баланс > 100000 руб.):")
    large = collection.get_large_balance(100000)
    for acc in large:
        print(f"   {acc.owner_name}: {acc.balance:.2f} руб.")
    
    print("\n📊 Кастомная фильтрация (баланс между 10000 и 100000):")
    custom = collection.filter(lambda acc: 10000 < acc.balance < 100000)
    for acc in custom:
        print(f"   {acc.owner_name}: {acc.balance:.2f} руб.")


def scenario_4_mixed_types():
    print_separator("СЦЕНАРИЙ 4: ХРАНЕНИЕ ОБЪЕКТОВ РАЗНЫХ ТИПОВ")
    
    collection = BankCollection(BankAccount, "account_number")
    
    basic = BankAccount("B001", "Иванов Иван", 100000, 50000, 5.0)
    join = JoinAccount("J001", "Петрова Мария", 250000, 100000, 6.0,
                        co_owners=["Сидоров А.", "Кузнецова Е."])
    currency = CurrencyAccount("C001", "Смирнов Дмитрий", 5000, 2000, 3.5, currency="USD")
    
    collection.add(basic)
    collection.add(join)
    collection.add(currency)
    
    print("📊 Счета в коллекции (разные типы):")
    for acc in collection:
        print(f"\n   Тип: {type(acc).__name__}")
        print(f"   {acc.to_string(verbose=False)}")
    
    print("\n🔄 Демонстрация полиморфизма через интерфейс InterestCalculable:")
    results = collection.process_all_monthly()
    for i, result in enumerate(results):
        print(f"   Счет {i+1}: {result['type']} | Проценты: {result['interest']:.2f}")
    
    print(f"\n💰 Общая сумма балансов: {collection.get_total_balance():,.2f} руб.")


def scenario_5_interface_filtering():
    print_separator("СЦЕНАРИЙ 5: ФИЛЬТРАЦИЯ ПО ИНТЕРФЕЙСАМ")
    
    collection = BankCollection(BankAccount, "account_number")
    
    accounts = [
        BankAccount("B001", "Иванов Иван", 100000, 50000, 5.0),
        JoinAccount("J001", "Петрова Мария", 250000, 100000, 6.0,
                   co_owners=["Сидоров А."]),
        CurrencyAccount("C001", "Смирнов Дмитрий", 5000, 2000, 3.5, currency="USD"),
        JoinAccount("J002", "Козлов Андрей", 150000, 80000, 5.5,
                   co_owners=["Новикова И."]),
        CurrencyAccount("C002", "Воробьева Анна", 7500, 3000, 4.0, currency="EUR")
    ]
    
    for acc in accounts:
        collection.add(acc)
    
    print(f"📊 Всего счетов: {len(collection)}")
    
    printable = collection.get_printable_items()
    print(f"\n📄 Printable объекты ({len(printable)}):")
    for item in printable:
        print(f"   {item.to_string(verbose=False)}")
    
    interest_items = collection.get_interest_calculable_items()
    print(f"\n📈 InterestCalculable объекты ({len(interest_items)}):")
    for item in interest_items:
        print(f"   {item.owner_name}: ставка {item.interest_rate}%")
    
    deposit_items = collection.get_deposit_calculable_items()
    print(f"\n💰 DepositCalculable объекты ({len(deposit_items)}):")
    for item in deposit_items:
        forecast = item.get_profit_forecast(6)
        currency_str = " руб." if not hasattr(item, 'currency') else f" {item.currency}"
        print(f"   {item.owner_name}: прогноз на 6 мес: {forecast:.2f}{currency_str}")
    
    total_profit = collection.get_total_profit_forecast(6)
    print(f"\n📊 Суммарный прогноз прибыли за 6 месяцев: {total_profit:.2f}")


def scenario_6_slicing_and_indexing():
    print_separator("СЦЕНАРИЙ 6: ИНДЕКСАЦИЯ И СРЕЗЫ")
    
    collection = BankCollection(BankAccount, "account_number")
    
    for i in range(1, 6):
        acc = BankAccount(f"ACC00{i}", f"Владелец {i}", i * 10000, 5000, 5.0)
        collection.add(acc)
    
    print("📊 Все счета:")
    for i, acc in enumerate(collection):
        print(f"   [{i}] {acc.account_number} | {acc.owner_name} | {acc.balance:.2f}")
    
    print(f"\n🔍 Доступ по индексу [0]: {collection[0].owner_name}")
    print(f"🔍 Доступ по индексу [3]: {collection[3].owner_name}")
    
    print("\n🔪 Срез [1:4]:")
    slice_collection = collection[1:4]
    for acc in slice_collection:
        print(f"   {acc.account_number} | {acc.owner_name} | {acc.balance:.2f}")
    
    print(f"\n✅ get_by_index(2): {collection.get_by_index(2).owner_name}")
    
    try:
        print("   Попытка доступа к несуществующему индексу...")
        collection.get_by_index(100)
    except IndexError as e:
        print(f"   ❌ Ошибка: {e}")


def scenario_7_edge_cases():
    print_separator("СЦЕНАРИЙ 7: КРАЕВЫЕ СЛУЧАИ И ИСКЛЮЧЕНИЯ")
    
    collection = BankCollection(BankAccount, "account_number")
    
    print("🔒 Проверка типов:")
    try:
        collection.add("not_a_bank_account")
    except TypeError as e:
        print(f"   ❌ Неправильный тип: {e}")
    
    acc = BankAccount("TEST001", "Тестовый", 1000, 500, 5.0)
    collection.add(acc)
    print(f"   ✅ Добавлен: {acc.account_number}")
    
    print("\n🔒 Проверка уникальности:")
    try:
        collection.add(acc)
    except ValueError as e:
        print(f"   ❌ Дубликат: {e}")
    
    print("\n🔒 Удаление несуществующего объекта:")
    fake_acc = BankAccount("FAKE001", "Фейковый", 0, 0, 0)
    try:
        collection.remove(fake_acc)
    except ValueError as e:
        print(f"   ❌ Ошибка: {e}")
    
    print("\n🔒 Удаление по неверному индексу:")
    try:
        collection.remove_at(100)
    except IndexError as e:
        print(f"   ❌ Ошибка: {e}")
    
    print("\n🔒 Операции с пустой коллекцией:")
    empty = BankCollection(BankAccount, "account_number")
    print(f"   Размер: {len(empty)}")
    print(f"   get_all(): {empty.get_all()}")
    print(f"   get_total_balance(): {empty.get_total_balance():.2f}")
    
    print("\n✅ Успешное удаление:")
    collection.remove(acc)
    print(f"   Размер после удаления: {len(collection)}")


def main():
    print("\n" + "=" * 80)
    print("🏦 ЛАБОРАТОРНАЯ РАБОТА №5 - GENERIC-КОЛЛЕКЦИЯ И ПАТТЕРНЫ")
    print("BankCollection: обобщенная коллекция банковских счетов")
    print("=" * 80)
    
    scenarios = [
        ("Базовые операции с коллекцией", scenario_1_basic_collection),
        ("Сортировка коллекции", scenario_2_sorting),
        ("Фильтрация коллекции", scenario_3_filtering),
        ("Хранение объектов разных типов", scenario_4_mixed_types),
        ("Фильтрация по интерфейсам", scenario_5_interface_filtering),
        ("Индексация и срезы", scenario_6_slicing_and_indexing),
        ("Краевые случаи и исключения", scenario_7_edge_cases)
    ]
    
    for name, func in scenarios:
        try:
            func()
        except Exception as e:
            print(f"\n❌ Ошибка в {name}: {e}")

if __name__ == "__main__":
    main()