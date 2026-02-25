class BankAccount:
    
    # Атрибут класса
    bank_name = "Python Bank"

    def __init__(self, account_number: str, owner: str, balance: float, credit_limit: float):
        self._validate_account_number(account_number)
        self._validate_owner(owner)
        self._validate_balance(balance)
        self._validate_credit_limit(credit_limit)

        self._account_number = account_number
        self._owner = owner
        self._balance = balance
        self._credit_limit = credit_limit
        self._is_active = True  # логическое состояние

    # -----------------------
    # Валидация (вынесена отдельно)
    # -----------------------

    def _validate_account_number(self, value):
        if not isinstance(value, str):
            raise TypeError("Номер счета должен быть строкой")
        if not value.strip():
            raise ValueError("Номер счета не может быть пустым")

    def _validate_owner(self, value):
        if not isinstance(value, str):
            raise TypeError("Имя владельца должно быть строкой")
        if not value.strip():
            raise ValueError("Имя владельца не может быть пустым")

    def _validate_balance(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError("Баланс должен быть числом")
        if value < 0:
            raise ValueError("Баланс не может быть отрицательным")

    def _validate_credit_limit(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError("Кредитный лимит должен быть числом")
        if value < 0:
            raise ValueError("Кредитный лимит не может быть отрицательным")

    # -----------------------
    # Properties
    # -----------------------

    @property
    def account_number(self):
        return self._account_number

    @property
    def owner(self):
        return self._owner

    @property
    def balance(self):
        return self._balance

    @property
    def credit_limit(self):
        return self._credit_limit

    @credit_limit.setter
    def credit_limit(self, value):
        self._validate_credit_limit(value)
        self._credit_limit = value

    @property
    def is_active(self):
        return self._is_active

    # -----------------------
    # Магические методы
    # -----------------------

    def __str__(self):
        status = "Активен" if self._is_active else "Закрыт"
        return (
            f"Банк: {self.bank_name}\n"
            f"Счет: {self._account_number}\n"
            f"Владелец: {self._owner}\n"
            f"Баланс: {self._balance:,.2f}\n"
            f"Лимит: {self._credit_limit:,.2f}\n"
            f"Статус: {status}"
        )

    def __repr__(self):
        return (f"BankAccount('{self._account_number}', "
                f"'{self._owner}', {self._balance}, {self._credit_limit})")

    def __eq__(self, other):
        if not isinstance(other, BankAccount):
            return False
        return self._account_number == other._account_number

    # -----------------------
    # Бизнес-методы
    # -----------------------

    def deposit(self, amount: float):
        if not self._is_active:
            raise RuntimeError("Счет закрыт")

        if not isinstance(amount, (int, float)):
            raise TypeError("Сумма должна быть числом")
        if amount <= 0:
            raise ValueError("Сумма должна быть положительной")

        self._balance += amount

    def withdraw(self, amount: float):
        if not self._is_active:
            raise RuntimeError("Счет закрыт")

        if not isinstance(amount, (int, float)):
            raise TypeError("Сумма должна быть числом")
        if amount <= 0:
            raise ValueError("Сумма должна быть положительной")

        if self._balance + self._credit_limit < amount:
            raise ValueError("Превышен доступный лимит средств")

        self._balance -= amount

    # -----------------------
    # Управление состоянием
    # -----------------------

    def close(self):
        self._is_active = False

    def activate(self):
        self._is_active = True