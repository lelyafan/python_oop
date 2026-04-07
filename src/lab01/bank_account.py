import validate

class BankAccount:
    bank_name = "Надежный банк"

    def __init__(self, account_number: str, owner_name: str, initial_balance: float, credit_limit: float, interest_rate: float):
        self._account_number = validate.validate_account_number(account_number)
        self._owner_name = validate.validate_owner_name(owner_name)
        self._balance = validate.validate_balance(initial_balance)
        self._credit_limit = validate.validate_credit_limit(credit_limit)
        self._interest_rate = validate.validate_interest_rate(interest_rate)
        self._is_active = True

    @property
    def account_number(self):
        return self._account_number
    
    @property
    def owner_name(self):
        return self._owner_name
    
    @property
    def balance(self):
        return self._balance
    
    @property
    def credit_limit(self):
        return self._credit_limit
    
    @property
    def interest_rate(self):
        return self._interest_rate

    @property
    def is_active(self):
        return self._is_active
    
    @credit_limit.setter
    def credit_limit(self, new_limit):
        if not self._is_active:
            raise PermissionError("Нельзя изменить лимит для закрытого счета.")
        self._credit_limit = validate.validate_credit_limit(new_limit)
        print(f"Кредитный лимит изменен на {self._credit_limit:.2f}")
    
    def deposit(self, amount: float):
        if not self._is_active:
            raise PermissionError("Нельзя вносить средства на закрытый счет.")
        if not isinstance(amount, (int, float)) or amount <= 0:
            raise ValueError("Сумма для пополнения должна быть положительным числом.")

        self._balance += amount
        print(f"Пополнение на {amount:.2f}. Текущий баланс: {self._balance:.2f}")

    def withdraw(self, amount: float):
        if not self._is_active:
            raise PermissionError("Нельзя снимать средства с закрытого счета.")
        if not isinstance(amount, (int, float)) or amount <= 0:
            raise ValueError("Сумма для снятия должна быть положительным числом.")

        available_funds = self._balance + self._credit_limit
        if amount > available_funds:
            raise ValueError(f"Недостаточно средств. Доступно для снятия (с учетом кредита): {available_funds:.2f}")

        self._balance -= amount
        print(f"Снятие {amount:.2f}. Текущий баланс: {self._balance:.2f}")

    def close_account(self):
        if not self._is_active:
            print("Счет уже закрыт.")
            return
    
        if self._balance < 0:
            raise PermissionError(f"Невозможно закрыть счет. Есть задолженность перед банком: {-self._balance:.2f}")

        self._is_active = False
        print(f"Счет {self._account_number} успешно закрыт.")

    def __str__(self):
        if self._is_active:
            status = "Активен"
        else:
            status = "Закрыт"
        return (f"👤 Владелец: {self._owner_name}\n"
                f"🏦 Счет: {self._account_number}\n"
                f"💰 Баланс: {self._balance:,.2f} руб.\n"
                f"💳 Кредитный лимит: {self._credit_limit:,.2f} руб.\n"
                f"📈 Ставка: {self._interest_rate:.1f}%\n"
                f"🔔 Статус: {status}")

    def __repr__(self):
        return (f"BankAccount(account_number='{self._account_number}', "
                f"owner_name='{self._owner_name}', "
                f"balance={self._balance}, "
                f"credit_limit={self._credit_limit}, "
                f"interest_rate={self._interest_rate})")

    def __eq__(self, other):
        if not isinstance(other, BankAccount):
            return False
        return self._account_number == other._account_number
