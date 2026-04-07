from bank_account import BankAccount
import validate

def main():
    print("="*60)
    print("Демонстрация работы класса BankAccount")
    print("="*60)

    print("\n--- Сценарий 1: Создание объекта и вывод ---")
    try:
        acc1 = BankAccount("40817810099910000123", "Иван Петров", 15000.50, 50000.0, 12.5)
        print("Объект успешно создан!")

        print("\nВывод информации о счете:")
        print(acc1)

        print("\nВывод для разработчика (__repr__):")
        print(repr(acc1))

        print("\nДоступ к атрибуту класса:")
        print(f"Через экземпляр: {acc1.bank_name}")
        print(f"Через класс: {BankAccount.bank_name}")

    except Exception as e:
        print(f"Ошибка при создании acc1: {e}")

    print("\n--- Сценарий 2: Демонстрация валидации (try/except) ---")
    print("Пытаемся создать счет с отрицательным балансом:")
    try:
        acc_invalid = BankAccount("123", "Тест Тестов", -100, 1000, 10)
    except ValueError as e:
        print(f"  Успешно перехвачена ошибка: {e}")

    print("\nПытаемся создать счет с некорректным именем (цифры):")
    try:
        acc_invalid = BankAccount("123", "Тест123", 100, 1000, 10)
    except ValueError as e:
        print(f"  Успешно перехвачена ошибка: {e}")

    print("\n--- Сценарий 3: Изменение свойств и бизнес-методы ---")
    acc2 = BankAccount("40817810099910000124", "Анна Смирнова", 5000.0, 20000.0, 15.0)
    print("Создан счет acc2:")
    print(acc2)

    print("\nИзменяем кредитный лимит через setter:")
    acc2.credit_limit = 25000.0
    print(f"Новый лимит: {acc2.credit_limit}")

    print("\nПытаемся установить отрицательный лимит:")
    try:
        acc2.credit_limit = -5000
    except ValueError as e:
        print(f"  Ошибка: {e}")

    print("\nПополняем счет (deposit):")
    acc2.deposit(1000)

    print("\nСнимаем 10000 руб. (в пределах кредитного лимита):")
    acc2.withdraw(10000)

    print("\nПытаемся снять сумму больше доступной (превышение кредитного лимита):")
    try:
        acc2.withdraw(50000)
    except ValueError as e:
        print(f"  Ошибка: {e}")

    print("\n--- Сценарий 4: Сравнение объектов и управление состоянием ---")

    acc3 = BankAccount("40817810099910000125", "Сидор Сидоров", 100.0, 0.0, 10.0)
    acc4 = BankAccount("40817810099910000125", "Другой Человек", 999.0, 1.0, 1.0) # Тот же номер

    print(f"acc1 == acc2? {'Да' if acc1 == acc2 else 'Нет'}")
    print(f"acc3 == acc4? (одинаковый номер счета) {'Да' if acc3 == acc4 else 'Нет'}")

    print("\nПытаемся закрыть счет acc3 (баланс 100, кредитного лимита нет):")
    acc3.close_account()

    print("\nПытаемся внести депозит на закрытый счет acc3:")
    try:
        acc3.deposit(500)
    except PermissionError as e:
        print(f"  Ошибка: {e}")

    print("\nПытаемся закрыть счет acc2, на котором есть долг (баланс отрицательный):")
    acc_debt = BankAccount("debt123", "Должник", 1000, 5000, 20)
    acc_debt.withdraw(6000)
    print(f"Баланс должника: {acc_debt.balance}")
    try:
        acc_debt.close_account()
    except PermissionError as e:
        print(f"  Ошибка: {e}")

    print("\n--- Сценарий 5: Итоговое состояние объектов ---")
    print("Информация по acc2 после всех операций:")
    print(acc2)
    print("\nИнформация по acc3 (закрыт):")
    print(acc3)

if __name__ == "__main__":
    main()