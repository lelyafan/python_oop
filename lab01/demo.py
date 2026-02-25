from model import BankAccount

print("=== Создание объекта ===")
acc1 = BankAccount("ACC1001", "Alice", 1000, 500)
print(acc1)

print("\n=== Сравнение объектов ===")
acc2 = BankAccount("ACC1001", "Alice", 2000, 300)
print("acc1 == acc2:", acc1 == acc2)

print("\n=== Работа setter ===")
acc1.credit_limit = 800
print("Новый лимит:", acc1.credit_limit)

print("\n=== Проверка ограничения ===")
try:
    acc1.credit_limit = -100
except ValueError as e:
    print("Ошибка:", e)

print("\n=== Бизнес-методы ===")
acc1.deposit(500)
acc1.withdraw(200)
print("Баланс после операций:", acc1.balance)

print("\n=== Демонстрация состояния ===")
acc1.close()

try:
    acc1.withdraw(100)
except RuntimeError as e:
    print("Ошибка при снятии:", e)

print("Статус активен:", acc1.is_active)

print("\n=== Атрибут класса ===")
print("Через класс:", BankAccount.bank_name)
print("Через экземпляр:", acc1.bank_name)

print("\n=== Некорректное создание ===")
try:
    bad = BankAccount("", "", -100, -50)
except Exception as e:
    print("Ошибка создания:", e)