from datetime import datetime
from models import Client, BankAccount, Credit, Deposit
from collection import BankCollection


def main():
    print("=" * 60)
    print("ДЕМОНСТРАЦИЯ БАНКОВСКОЙ СИСТЕМЫ")
    print("=" * 60)

    # ========== Создание клиентов ==========
    client1 = Client(1, "Иван Петров", "1234 567890")
    client2 = Client(2, "Мария Сидорова", "2345 678901")
    client3 = Client(3, "Алексей Смирнов", "3456 789012")

    # ========== Сценарий 1: Работа со счетами ==========
    print("\n--- СЦЕНАРИЙ 1: Банковские счета ---")

    # Создание коллекции счетов
    accounts = BankCollection(BankAccount, id_attr="account_id")

    # Создание счетов
    acc1 = BankAccount(101, client1, 5000)
    acc2 = BankAccount(102, client2, 12000)
    acc3 = BankAccount(103, client3, 3000)

    # Добавление в коллекцию
    accounts.add(acc1)
    accounts.add(acc2)
    accounts.add(acc3)

    print(f"Добавлено 3 счета. Всего в коллекции: {len(accounts)}")

    # Проверка на дубликаты
    try:
        acc_duplicate = BankAccount(101, client1, 1000)
        accounts.add(acc_duplicate)
    except ValueError as e:
        print(f"❌ Ошибка (дубликат): {e}")

    # Проверка типа
    try:
        accounts.add("не банковский счёт")
    except TypeError as e:
        print(f"❌ Ошибка (тип): {e}")

    # Вывод всех счетов
    print("\nВсе счета:")
    for acc in accounts:
        print(f"  {acc}")

    # Поиск счёта по ID
    found = accounts.find_by(account_id=102)
    print(f"\n🔍 Поиск счёта 102: {found}")

    # Сортировка по балансу
    print("\nСортировка по балансу (по убыванию):")
    accounts.sort_by_balance()
    for acc in accounts:
        print(f"  {acc}")

    # Фильтрация: активные счета (баланс > 0)
    active = accounts.get_active_accounts()
    print(f"\n✅ Активные счета (баланс > 0): {len(active)}")
    for acc in active:
        print(f"  {acc}")

    # Индексация
    print(f"\n📌 Первый счёт: {accounts[0]}")
    print(f"📌 Третий счёт: {accounts[2]}")

    # Удаление по индексу
    accounts.remove_at(1)
    print(f"\n🗑️ Удалён счёт с индексом 1. Осталось счетов: {len(accounts)}")
    for acc in accounts:
        print(f"  {acc}")

    # ========== Сценарий 2: Кредиты ==========
    print("\n--- СЦЕНАРИЙ 2: Кредиты ---")

    credits = BankCollection(Credit, id_attr="credit_id")

    credit1 = Credit(201, client1, limit=100000, interest_rate=0.15)
    credit2 = Credit(202, client2, limit=50000, interest_rate=0.18)
    credit3 = Credit(203, client3, limit=200000, interest_rate=0.12)

    credits.add(credit1)
    credits.add(credit2)
    credits.add(credit3)

    # Выдача кредита
    credit1.take_credit(30000)
    credit2.take_credit(50000)  # использован полностью

    print("Кредиты после выдачи:")
    for cr in credits:
        print(f"  {cr}, использовано: {cr.used_amount}")

    # Фильтрация доступных кредитов
    available_credits = credits.get_available_credits()
    print(f"\n💰 Доступные кредиты (есть свободный лимит): {len(available_credits)}")
    for cr in available_credits:
        remaining = cr.limit - cr.used_amount
        print(f"  {cr.client.name}: осталось {remaining}")

    # Сортировка по процентной ставке
    print("\nСортировка кредитов по ставке (возрастание):")
    credits.sort(key=lambda c: c.interest_rate)
    for cr in credits:
        print(f"  {cr.client.name}: ставка {cr.interest_rate * 100}%")

    # ========== Сценарий 3: Депозиты ==========
    print("\n--- СЦЕНАРИЙ 3: Депозиты ---")

    deposits = BankCollection(Deposit, id_attr="deposit_id")

    dep1 = Deposit(301, client1, amount=100000, interest_rate=0.08, term_months=12)
    dep2 = Deposit(302, client2, amount=50000, interest_rate=0.07, term_months=6)
    dep3 = Deposit(303, client3, amount=250000, interest_rate=0.09, term_months=24)

    deposits.add(dep1)
    deposits.add(dep2)
    deposits.add(dep3)

    print("Все депозиты:")
    for dep in deposits:
        final = dep.calculate_final_amount()
        print(f"  {dep.client.name}: {dep.amount} -> через {dep.term_months} мес: {final:.2f}")

    # Крупные депозиты
    large = deposits.get_large_deposits(min_amount=80000)
    print(f"\n🏦 Крупные депозиты (>80 000): {len(large)}")
    for dep in large:
        print(f"  {dep.client.name}: {dep.amount}")

    # Использование len()
    print(f"\n📊 Статистика:")
    print(f"  Всего счетов: {len(accounts)}")
    print(f"  Всего кредитов: {len(credits)}")
    print(f"  Всего депозитов: {len(deposits)}")

    # Итерация в цикле for (уже показана выше)
    print("\n--- ИТОГОВАЯ ПРОВЕРКА ВСЕХ ВОЗМОЖНОСТЕЙ ---")
    print("✅ add() — добавление с проверкой типа и дубликатов")
    print("✅ remove() / remove_at() — удаление")
    print("✅ get_all() — получение всех объектов")
    print("✅ find_by() — поиск по атрибутам")
    print("✅ __len__() — длина коллекции")
    print("✅ __iter__() — итерация в for")
    print("✅ __getitem__() — индексация")
    print("✅ sort() / sort_by_*() — сортировка")
    print("✅ filter() / get_active_accounts() и др. — логические операции")
    print("✅ ограничение на дубликаты по id")
    print("✅ ограничение на тип объектов")


if __name__ == "__main__":
    main()