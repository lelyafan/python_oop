from typing import List
from lib.base import BankAccount


class JoinAccount(BankAccount):
    """
    Совместный банковский счет (для нескольких владельцев)
    Дополнительные атрибуты:
    - co_owners: список совладельцев
    - withdrawal_limit: лимит на снятие для каждого совладельца
    """
    
    def __init__(self, account_number: str, owner_name: str, initial_balance: float,
                 credit_limit: float, interest_rate: float, co_owners: List[str], 
                 withdrawal_limit: float = 50000.0):
        """
        Конструктор совместного счета
        Использует super() для вызова конструктора базового класса
        """
        super().__init__(account_number, owner_name, initial_balance, 
                        credit_limit, interest_rate)
        
        # Новые атрибуты для совместного счета
        self._co_owners = co_owners
        self._withdrawal_limit = withdrawal_limit
        
    @property
    def co_owners(self) -> List[str]:
        """Список совладельцев счета"""
        return self._co_owners.copy()
    
    @property
    def withdrawal_limit(self) -> float:
        """Лимит снятия для совладельца"""
        return self._withdrawal_limit
    
    @withdrawal_limit.setter
    def withdrawal_limit(self, new_limit: float):
        """Изменение лимита снятия"""
        if new_limit <= 0:
            raise ValueError("Лимит должен быть положительным числом")
        self._withdrawal_limit = new_limit
        print(f"Лимит снятия изменен на {self._withdrawal_limit:.2f} руб.")
    
    # Новый метод: добавление совладельца
    def add_co_owner(self, new_owner: str):
        """Добавление нового совладельца счета"""
        if new_owner in self._co_owners:
            print(f"{new_owner} уже является совладельцем счета")
            return
        self._co_owners.append(new_owner)
        print(f"✅ Совладелец {new_owner} добавлен на счет {self._account_number}")
    
    # Новый метод: удаление совладельца
    def remove_co_owner(self, owner: str):
        """Удаление совладельца со счета"""
        if owner == self._owner_name:
            raise PermissionError("Нельзя удалить основного владельца счета")
        if owner not in self._co_owners:
            print(f"{owner} не является совладельцем счета")
            return
        self._co_owners.remove(owner)
        print(f"❌ Совладелец {owner} удален со счета {self._account_number}")
    
    # Переопределенный метод снятия средств с учетом лимита
    def withdraw(self, amount: float):
        """Переопределенный метод снятия с учетом лимита"""
        if amount > self._withdrawal_limit:
            raise ValueError(f"Превышен лимит снятия ({self._withdrawal_limit:.2f} руб.)")
        super().withdraw(amount)
    
    # Переопределенный метод ежемесячной обработки (полиморфизм)
    def process_monthly(self) -> dict:
        """Для совместного счета: начисляем бонус за количество владельцев"""
        result = super().process_monthly()
        result['type'] = 'Совместный счет'
        
        # Бонус: +0.1% за каждого совладельца (максимум +0.5%)
        co_owner_bonus = min(len(self._co_owners) * 0.1, 0.5)
        bonus_amount = self._balance * (co_owner_bonus / 100)
        
        if bonus_amount > 0:
            self._balance += bonus_amount
            result['bonus'] = bonus_amount
            result['balance_after'] = self._balance
            print(f"🎁 Бонус за совместное владение: {bonus_amount:.2f} руб.")
        
        return result
    
    def __str__(self):
        """Переопределенный метод __str__ для отображения совместного счета"""
        base_str = super().__str__()
        co_owners_str = ", ".join(self._co_owners) if self._co_owners else "Нет"
        return (base_str + 
                f"\n👥 Совладельцы: {co_owners_str}\n"
                f"🔒 Лимит снятия: {self._withdrawal_limit:,.2f} руб.")


class CurrencyAccount(BankAccount):
    """
    Валютный банковский счет
    Дополнительные атрибуты:
    - currency: валюта счета (USD, EUR, CNY)
    - exchange_rate: курс к рублю
    """
    
    CURRENCIES = {
        'USD': 92.5,  
        'EUR': 100.2,
        'CNY': 12.8
    }
    
    def __init__(self, account_number: str, owner_name: str, initial_balance: float,
                 credit_limit: float, interest_rate: float, currency: str = 'USD'):
        """
        Конструктор валютного счета
        Использует super() для вызова конструктора базового класса
        """
        super().__init__(account_number, owner_name, initial_balance, 
                        credit_limit, interest_rate)
        
        if currency not in self.CURRENCIES:
            raise ValueError(f"Неподдерживаемая валюта. Доступны: {list(self.CURRENCIES.keys())}")
        
        self._currency = currency
        self._exchange_rate = self.CURRENCIES[currency]
    
    @property
    def currency(self) -> str:
        """Валюта счета"""
        return self._currency
    
    @property
    def exchange_rate(self) -> float:
        """Текущий курс к рублю"""
        return self._exchange_rate
    
    # Новый метод: конвертация баланса в рубли
    def get_balance_in_rub(self) -> float:
        """Получение баланса в рублях по текущему курсу"""
        return self._balance * self._exchange_rate
    
    # Новый метод: конвертация в другую валюту
    def convert_to(self, target_currency: str) -> float:
        """Конвертация баланса в другую валюту (без изменения счета)"""
        if target_currency not in self.CURRENCIES:
            raise ValueError(f"Неподдерживаемая валюта: {target_currency}")
        
        rub_amount = self.get_balance_in_rub()
        target_rate = self.CURRENCIES[target_currency]
        converted_amount = rub_amount / target_rate
        return converted_amount
    
    # Переопределенный метод расчета процентов (полиморфизм)
    def calculate_interest(self) -> float:
        """Для валютного счета: повышенный процент если курс выгодный"""
        base_interest = super().calculate_interest()
        
        # Если курс USD ниже 90, повышенный процент
        if self._currency == 'USD' and self._exchange_rate < 90:
            bonus_interest = self._balance * 0.5 / 100  # +0.5%
            return base_interest + bonus_interest
        
        return base_interest
    
    # Переопределенный метод ежемесячной обработки (полиморфизм)
    def process_monthly(self) -> dict:
        """Для валютного счета: обновление курса и начисление процентов"""
        # Обновляем курс к актуальному
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
    
    def __str__(self):
        """Переопределенный метод __str__ для отображения валютного счета"""
        base_str = super().__str__()
        rub_equivalent = self.get_balance_in_rub()
        return (base_str +
                f"\n💵 Валюта: {self._currency}\n"
                f"💱 Курс к RUB: {self._exchange_rate:.2f}\n"
                f"💰 Эквивалент в RUB: {rub_equivalent:,.2f}")