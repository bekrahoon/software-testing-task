"""Система банковского счёта."""
import math


class InsufficientFundsError(Exception):
    """Недостаточно средств на счёте."""


class BankAccount:
    def __init__(self, owner, account_number):
        if not isinstance(owner, str) or not owner.strip():
            raise ValueError("Имя владельца должно быть непустой строкой")
        if not isinstance(account_number, str) or not account_number.strip():
            raise ValueError("Номер счёта должен быть непустой строкой")
        self.owner = owner
        self.account_number = account_number
        self._balance = 0  # начальный баланс всегда равен 0

    @staticmethod
    def _validate_amount(amount):
        if isinstance(amount, bool) or not isinstance(amount, (int, float)):
            raise TypeError("Сумма должна быть числом")
        if math.isnan(amount) or math.isinf(amount):
            raise ValueError("Сумма должна быть конечным числом")
        if amount <= 0:
            raise ValueError("Сумма должна быть положительной")

    def deposit(self, amount):
        """Пополнить счёт на amount."""
        self._validate_amount(amount)
        self._balance += amount

    def withdraw(self, amount):
        """Снять amount со счёта."""
        self._validate_amount(amount)
        if amount > self._balance:
            raise InsufficientFundsError("Недостаточно средств")
        self._balance -= amount

    def transfer(self, target, amount):
        """Перевести amount на счёт target. При ошибке оба счёта не меняются."""
        if not isinstance(target, BankAccount):
            raise TypeError("Получатель должен быть BankAccount")
        if target is self:
            raise ValueError("Нельзя переводить деньги на тот же счёт")
        self._validate_amount(amount)
        if amount > self._balance:
            raise InsufficientFundsError("Недостаточно средств")
        self._balance -= amount
        target._balance += amount

    def get_balance(self):
        return self._balance

    def is_empty(self):
        return self._balance == 0
