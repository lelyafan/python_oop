from datetime import datetime
from typing import Optional


class Client:
    """Клиент банка"""
    def __init__(self, client_id: int, name: str, passport: str):
        self.client_id = client_id
        self.name = name
        self.passport = passport

    def __repr__(self):
        return f"Client(id={self.client_id}, name='{self.name}')"


class Transaction:
    """Банковская транзакция"""
    def __init__(self, transaction_id: int, amount: float, date: datetime, description: str = ""):
        self.transaction_id = transaction_id
        self.amount = amount
        self.date = date
        self.description = description

    def __repr__(self):
        return f"Transaction(id={self.transaction_id}, amount={self.amount}, date={self.date.date()})"


class BankAccount:
    """Банковский счёт с ограничением: баланс ≥ 0"""
    def __init__(self, account_id: int, client: Client, initial_balance: float = 0.0):
        if initial_balance < 0:
            raise ValueError("Начальный баланс не может быть отрицательным")
        self.account_id = account_id
        self.client = client
        self.balance = initial_balance
        self.transactions: list[Transaction] = []

    def deposit(self, amount: float) -> Transaction:
        if amount <= 0:
            raise ValueError("Сумма пополнения должна быть положительной")
        self.balance += amount
        tx = Transaction(
            transaction_id=len(self.transactions) + 1,
            amount=amount,
            date=datetime.now(),
            description="Пополнение"
        )
        self.transactions.append(tx)
        return tx

    def withdraw(self, amount: float) -> Transaction:
        if amount <= 0:
            raise ValueError("Сумма снятия должна быть положительной")
        if self.balance - amount < 0:
            raise ValueError("Недостаточно средств. Баланс не может стать отрицательным")
        self.balance -= amount
        tx = Transaction(
            transaction_id=len(self.transactions) + 1,
            amount=-amount,
            date=datetime.now(),
            description="Снятие"
        )
        self.transactions.append(tx)
        return tx

    def __repr__(self):
        return f"BankAccount(id={self.account_id}, client={self.client.name}, balance={self.balance})"


class Credit:
    """Кредитный продукт с лимитом"""
    def __init__(self, credit_id: int, client: Client, limit: float, interest_rate: float):
        if limit < 0:
            raise ValueError("Лимит кредита не может быть отрицательным")
        self.credit_id = credit_id
        self.client = client
        self.limit = limit
        self.interest_rate = interest_rate 
        self.used_amount = 0.0

    def take_credit(self, amount: float):
        if amount <= 0:
            raise ValueError("Сумма кредита должна быть положительной")
        if self.used_amount + amount > self.limit:
            raise ValueError("Превышен лимит кредита")
        self.used_amount += amount

    def __repr__(self):
        return f"Credit(id={self.credit_id}, client={self.client.name}, limit={self.limit}, rate={self.interest_rate})"


class Deposit:
    """Депозит с процентной ставкой"""
    def __init__(self, deposit_id: int, client: Client, amount: float, interest_rate: float, term_months: int):
        if amount <= 0:
            raise ValueError("Сумма депозита должна быть положительной")
        self.deposit_id = deposit_id
        self.client = client
        self.amount = amount
        self.interest_rate = interest_rate
        self.term_months = term_months
        self.created_at = datetime.now()

    def calculate_final_amount(self) -> float:
        return self.amount * (1 + self.interest_rate * (self.term_months / 12))

    def __repr__(self):
        return f"Deposit(id={self.deposit_id}, client={self.client.name}, amount={self.amount}, rate={self.interest_rate})"