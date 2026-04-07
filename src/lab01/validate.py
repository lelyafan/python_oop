import re

def validate_owner_name(name: str):
    if not isinstance(name, str):
        raise TypeError("Имя владельца должно быть строкой.")
    if not name or name.isspace():
        raise ValueError("Имя владельца не может быть пустым.")
    if not re.match(r"^[A-Za-zA-Яа-я\s]+$", name):
        raise ValueError("Имя владельца может содержать только буквы и пробелы.")
    return name.strip()

def validate_balance(balance: float):
    if not isinstance(balance, (int,float)):
        raise TypeError("Баланс должен быть числом.")
    if balance < 0:
        raise ValueError("Баланс не может быть отрицательным")
    return float(balance)

def validate_credit_limit(limit: float):
    if not isinstance(limit, (int, float)):
        raise TypeError("Кредитный лимит должен быть числом")
    if limit < 0:
        raise ValueError("Кредитный лимит не может быть отрицательным")
    return float(limit)

def validate_interest_rate(rate: float):
    if not isinstance(rate, (int, float)):
        raise TypeError("Процентная ставка должна быть числом")
    if rate < 0 or rate > 100:
        raise ValueError("Процентная ставка должна быть в диапазоне от 0 до 100.")
    return float(rate)

def validate_account_number(acc_num: str):
    if not isinstance(acc_num, str):
        raise TypeError("Номер счета должен быть строкой.")
    if not acc_num or acc_num.isspace():
        raise ValueError("Номер счета не может быть пустым")
    return acc_num.strip()