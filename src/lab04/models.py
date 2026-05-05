import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lib import validate
from interfaces import (Printable, Comparable, InterestCalculable, Withdrawable, DepositCalculable)
from typing import List, Dict, Any


class BankAccount(Printable, Comparable, InterestCalculable, Withdrawable, DepositCalculable):
    bank_name = "Надежный банк"

    def __init__(self, account_number: str, owner_name: str, initial_balance: float, 
                 credit_limit: float, interest_rate: float):
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
    
    def to_string(self, verbose: bool = True) -> str:
        if not verbose:
            return f"{self._account_number} | {self._owner_name} | {self._balance:.2f}"
        
        status = "Активен" if self._is_active else "Закрыт"
        return (f"👤 Владелец: {self._owner_name}\n"
                f"🏦 Счет: {self._account_number}\n"
                f"💰 Баланс: {self._balance:,.2f} руб.\n"
                f"💳 Кредитный лимит: {self._credit_limit:,.2f} руб.\n"
                f"📈 Ставка: {self._interest_rate:.1f}%\n"
                f"🔔 Статус: {status}")
    
    def compare_to(self, other: Any) -> int:
        if not isinstance(other, BankAccount):
            raise TypeError("Можно сравнивать только объекты BankAccount")
        if self._balance < other.balance:
            return -1
        elif self._balance > other.balance:
            return 1
        return 0
    
    def calculate_interest(self) -> float:
        if self._balance > 0:
            interest = self._balance * (self._interest_rate / 100)
            return interest
        return 0
    
    def process_monthly(self) -> Dict[str, Any]:
        result = {
            'type': 'Базовая операция',
            'interest': self.calculate_interest(),
            'balance_before': self._balance,
            'balance_after': self._balance
        }
        
        if result['interest'] > 0:
            self._balance += result['interest']
            result['balance_after'] = self._balance
            print(f"✅ Начислены проценты: {result['interest']:.2f}")
        
        return result
    
    def withdraw(self, amount: float) -> bool:
        if not self._is_active:
            print("❌ Нельзя снимать средства с закрытого счета.")
            return False
        if not isinstance(amount, (int, float)) or amount <= 0:
            print("❌ Сумма для снятия должна быть положительным числом.")
            return False

        available_funds = self._balance + self._credit_limit
        if amount > available_funds:
            print(f"❌ Недостаточно средств. Доступно: {available_funds:.2f}")
            return False

        self._balance -= amount
        print(f"✅ Снятие {amount:.2f}. Баланс: {self._balance:.2f}")
        return True
    
    def get_profit_forecast(self, months: int) -> float:
        """Прогноз прибыли (интерфейс DepositCalculable)"""
        if months <= 0:
            return 0
        monthly_rate = self._interest_rate / 100 / 12
        current_balance = self._balance
        total_profit = 0
        
        for _ in range(months):
            profit = current_balance * monthly_rate
            total_profit += profit
            current_balance += profit
        
        return total_profit
    
    def deposit(self, amount: float):
        if not self._is_active:
            raise PermissionError("Нельзя вносить средства на закрытый счет.")
        if not isinstance(amount, (int, float)) or amount <= 0:
            raise ValueError("Сумма для пополнения должна быть положительным числом.")

        self._balance += amount
        print(f"Пополнение на {amount:.2f}. Текущий баланс: {self._balance:.2f}")

    def close_account(self):
        if not self._is_active:
            print("Счет уже закрыт.")
            return
    
        if self._balance < 0:
            raise PermissionError(f"Невозможно закрыть счет. Есть задолженность: {-self._balance:.2f}")

        self._is_active = False
        print(f"Счет {self._account_number} успешно закрыт.")

    def __str__(self):
        return self.to_string(verbose=True)


class JoinAccount(BankAccount):
    
    def __init__(self, account_number: str, owner_name: str, initial_balance: float,
                 credit_limit: float, interest_rate: float, co_owners: List[str], 
                 withdrawal_limit: float = 50000.0):
        super().__init__(account_number, owner_name, initial_balance, 
                        credit_limit, interest_rate)
        self._co_owners = co_owners
        self._withdrawal_limit = withdrawal_limit
        
    @property
    def co_owners(self) -> List[str]:
        return self._co_owners.copy()
    
    @property
    def withdrawal_limit(self) -> float:
        return self._withdrawal_limit
    
    def to_string(self, verbose: bool = True) -> str:
        if not verbose:
            owners_str = f", {len(self._co_owners)} совл." if self._co_owners else ""
            return f"{self._account_number} | {self._owner_name}{owners_str} | {self._balance:.2f}"
        
        base_str = super().to_string(verbose=True)
        co_owners_str = ", ".join(self._co_owners) if self._co_owners else "Нет"
        return (base_str + 
                f"\n👥 Совладельцы: {co_owners_str}\n"
                f"🔒 Лимит снятия: {self._withdrawal_limit:,.2f} руб.")
    
    def process_monthly(self) -> Dict[str, Any]:
        result = super().process_monthly()
        result['type'] = 'Совместный счет'
        
        co_owner_bonus = min(len(self._co_owners) * 0.1, 0.5)
        bonus_amount = self._balance * (co_owner_bonus / 100)
        
        if bonus_amount > 0:
            self._balance += bonus_amount
            result['bonus'] = bonus_amount
            result['balance_after'] = self._balance
            print(f"🎁 Бонус за совместное владение: {bonus_amount:.2f} руб.")
        
        return result
    
    def compare_to(self, other) -> int:
        if not isinstance(other, JoinAccount):
            return super().compare_to(other)
        if len(self._co_owners) < len(other.co_owners):
            return -1
        elif len(self._co_owners) > len(other.co_owners):
            return 1
        return super().compare_to(other)
    
    def withdraw(self, amount: float) -> bool:
        if amount > self._withdrawal_limit:
            print(f"❌ Превышен лимит снятия ({self._withdrawal_limit:.2f} руб.)")
            return False
        return super().withdraw(amount)
    
    def add_co_owner(self, new_owner: str):
        if new_owner in self._co_owners:
            print(f"{new_owner} уже является совладельцем")
            return
        self._co_owners.append(new_owner)
        print(f"✅ Совладелец {new_owner} добавлен")
    
    def remove_co_owner(self, owner: str):
        if owner == self._owner_name:
            raise PermissionError("Нельзя удалить основного владельца")
        if owner not in self._co_owners:
            print(f"{owner} не является совладельцем")
            return
        self._co_owners.remove(owner)
        print(f"❌ Совладелец {owner} удален")


class CurrencyAccount(BankAccount):
    CURRENCIES = {
        'USD': 92.5,
        'EUR': 100.2,
        'CNY': 12.8
    }
    
    def __init__(self, account_number: str, owner_name: str, initial_balance: float,
                 credit_limit: float, interest_rate: float, currency: str = 'USD'):
        super().__init__(account_number, owner_name, initial_balance, 
                        credit_limit, interest_rate)
        
        if currency not in self.CURRENCIES:
            raise ValueError(f"Неподдерживаемая валюта. Доступны: {list(self.CURRENCIES.keys())}")
        
        self._currency = currency
        self._exchange_rate = self.CURRENCIES[currency]
    
    @property
    def currency(self) -> str:
        return self._currency
    
    @property
    def exchange_rate(self) -> float:
        return self._exchange_rate
    
    def to_string(self, verbose: bool = True) -> str:
        if not verbose:
            return f"{self._account_number} | {self._owner_name} | {self._balance:.2f} {self._currency}"
        
        base_str = super().to_string(verbose=True)
        rub_equivalent = self.get_balance_in_rub()
        return (base_str +
                f"\n💵 Валюта: {self._currency}\n"
                f"💱 Курс к RUB: {self._exchange_rate:.2f}\n"
                f"💰 Эквивалент в RUB: {rub_equivalent:,.2f}")
    
    def calculate_interest(self) -> float:
        base_interest = super().calculate_interest()
        
        if self._currency == 'USD' and self._exchange_rate < 90:
            bonus_interest = self._balance * 0.5 / 100
            return base_interest + bonus_interest
        
        return base_interest
    
    def process_monthly(self) -> Dict[str, Any]:
        old_rate = self._exchange_rate
        self._exchange_rate = self.CURRENCIES.get(self._currency, old_rate)
        
        result = super().process_monthly()
        result['type'] = f'Валютный счет ({self._currency})'
        result['old_rate'] = old_rate
        result['new_rate'] = self._exchange_rate
        
        if old_rate != self._exchange_rate:
            rate_change = ((self._exchange_rate - old_rate) / old_rate) * 100
            print(f"💱 Курс {self._currency} изменился на {rate_change:.2f}%")
        
        return result
    
    def compare_to(self, other) -> int:
        if not isinstance(other, CurrencyAccount):
            return super().compare_to(other)
        
        my_rub = self.get_balance_in_rub()
        other_rub = other.get_balance_in_rub()
        
        if my_rub < other_rub:
            return -1
        elif my_rub > other_rub:
            return 1
        return 0
    
    def get_profit_forecast(self, months: int) -> float:
        rub_balance = self.get_balance_in_rub()
        if rub_balance <= 0:
            return 0
        
        monthly_rate = self._interest_rate / 100 / 12
        total_profit = 0
        current_rub = rub_balance
        
        for _ in range(months):
            profit = current_rub * monthly_rate
            total_profit += profit
            current_rub += profit
        
        return total_profit
    
    def get_balance_in_rub(self) -> float:
        return self._balance * self._exchange_rate
    
    def convert_to(self, target_currency: str) -> float:
        if target_currency not in self.CURRENCIES:
            raise ValueError(f"Неподдерживаемая валюта: {target_currency}")
        
        rub_amount = self.get_balance_in_rub()
        target_rate = self.CURRENCIES[target_currency]
        return rub_amount / target_rate