# Система банковского счёта

Задание 5 по дисциплине «Тестирование ПО»: разработка и модульное тестирование системы банковского счёта на Python с использованием `unittest`.

## Возможности

- создание счёта с именем владельца и номером счёта (начальный баланс равен 0);
- пополнение счёта;
- снятие денег (нельзя снять больше, чем на счёте);
- перевод денег на другой счёт (при ошибке оба счёта не меняются);
- получение текущего баланса;
- проверка, пуст ли счёт.

## Структура проекта

```
.
├── bank_account.py        # класс BankAccount и исключение InsufficientFundsError
├── test_bank_account.py   # модульные тесты (24 теста)
└── README.md
```

## Требования

- Python 3.8 или новее
- Внешние библиотеки не нужны, используется только стандартная `unittest`

## Запуск тестов

Из папки проекта:

```bash
python3 -m unittest -v
```

Запуск одного тестового класса или теста:

```bash
python3 -m unittest test_bank_account.TestTransfer -v
python3 -m unittest test_bank_account.TestTransfer.test_successful_transfer -v
```

Ожидаемый результат:

```
Ran 24 tests in 0.00s

OK
```

## Пример использования

```python
from bank_account import BankAccount, InsufficientFundsError

a = BankAccount("Иван", "KG001")
b = BankAccount("Пётр", "KG002")

a.deposit(500)
a.withdraw(100)
a.transfer(b, 150)

print(a.get_balance())  # 250
print(b.get_balance())  # 150
print(a.is_empty())     # False

try:
    a.withdraw(1000)
except InsufficientFundsError:
    print("Недостаточно средств")
```

## API

| Метод | Описание |
|---|---|
| `BankAccount(owner, account_number)` | Создаёт счёт, баланс равен 0 |
| `deposit(amount)` | Пополняет счёт на `amount` |
| `withdraw(amount)` | Снимает `amount` со счёта |
| `transfer(target, amount)` | Переводит `amount` на счёт `target` |
| `get_balance()` | Возвращает текущий баланс |
| `is_empty()` | `True`, если баланс равен 0 |

## Обработка ошибок

| Ситуация | Исключение |
|---|---|
| Пустое или не строковое имя владельца либо номер счёта | `ValueError` |
| Сумма не число (строка, `None`, `bool`) или получатель не `BankAccount` | `TypeError` |
| Сумма ноль, отрицательная, `NaN` или `inf`; перевод на тот же счёт | `ValueError` |
| Сумма больше баланса | `InsufficientFundsError` |

## Что покрывают тесты

| Класс | Проверяется |
|---|---|
| `TestCreation` | хранение данных, начальный баланс, неверные имя и номер |
| `TestDeposit` | рост баланса, неверные суммы и типы |
| `TestWithdraw` | уменьшение баланса, превышение баланса, неверные суммы |
| `TestTransfer` | равенство изменений счетов, неизменность при ошибке, перевод самому себе |
| `TestBalanceAndEmpty` | баланс после цепочки операций, признак пустого счёта |

## Автор

Умуржанов Аба-Бекрахун, группа IT-124, Международный университет Центральной Азии.
