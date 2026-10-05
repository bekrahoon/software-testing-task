import unittest

from bank_account import BankAccount, InsufficientFundsError


class TestCreation(unittest.TestCase):
    def test_stores_owner_and_number(self):
        acc = BankAccount("Иван", "KG001")
        self.assertEqual(acc.owner, "Иван")
        self.assertEqual(acc.account_number, "KG001")

    def test_initial_balance_is_zero(self):
        self.assertEqual(BankAccount("Иван", "KG001").get_balance(), 0)

    def test_invalid_owner(self):
        for bad in ("", "   ", None, 123):
            with self.subTest(owner=bad):
                with self.assertRaises(ValueError):
                    BankAccount(bad, "KG001")

    def test_invalid_number(self):
        for bad in ("", "  ", None, 123):
            with self.subTest(number=bad):
                with self.assertRaises(ValueError):
                    BankAccount("Иван", bad)


class TestDeposit(unittest.TestCase):
    def setUp(self):
        self.acc = BankAccount("Иван", "KG001")

    def test_deposit_increases_balance(self):
        self.acc.deposit(100)
        self.assertEqual(self.acc.get_balance(), 100)

    def test_multiple_deposits(self):
        self.acc.deposit(100)
        self.acc.deposit(50.5)
        self.assertAlmostEqual(self.acc.get_balance(), 150.5)

    def test_deposit_non_positive(self):
        for bad in (0, -10):
            with self.subTest(amount=bad):
                with self.assertRaises(ValueError):
                    self.acc.deposit(bad)
        self.assertEqual(self.acc.get_balance(), 0)

    def test_deposit_wrong_type(self):
        for bad in ("100", None, True, [1]):
            with self.subTest(amount=bad):
                with self.assertRaises(TypeError):
                    self.acc.deposit(bad)

    def test_deposit_nan_inf(self):
        for bad in (float("nan"), float("inf")):
            with self.subTest(amount=bad):
                with self.assertRaises(ValueError):
                    self.acc.deposit(bad)


class TestWithdraw(unittest.TestCase):
    def setUp(self):
        self.acc = BankAccount("Иван", "KG001")
        self.acc.deposit(100)

    def test_withdraw_decreases_balance(self):
        self.acc.withdraw(30)
        self.assertEqual(self.acc.get_balance(), 70)

    def test_withdraw_entire_balance(self):
        self.acc.withdraw(100)
        self.assertEqual(self.acc.get_balance(), 0)

    def test_withdraw_more_than_balance(self):
        with self.assertRaises(InsufficientFundsError):
            self.acc.withdraw(100.01)
        self.assertEqual(self.acc.get_balance(), 100)

    def test_withdraw_negative_or_zero(self):
        for bad in (-5, 0):
            with self.subTest(amount=bad):
                with self.assertRaises(ValueError):
                    self.acc.withdraw(bad)
        self.assertEqual(self.acc.get_balance(), 100)

    def test_withdraw_wrong_type(self):
        with self.assertRaises(TypeError):
            self.acc.withdraw("10")


class TestTransfer(unittest.TestCase):
    def setUp(self):
        self.a = BankAccount("Иван", "KG001")
        self.b = BankAccount("Пётр", "KG002")
        self.a.deposit(200)
        self.b.deposit(50)

    def test_successful_transfer(self):
        self.a.transfer(self.b, 80)
        self.assertEqual(self.a.get_balance(), 120)
        self.assertEqual(self.b.get_balance(), 130)

    def test_changes_are_equal(self):
        total_before = self.a.get_balance() + self.b.get_balance()
        a0, b0 = self.a.get_balance(), self.b.get_balance()
        self.a.transfer(self.b, 75)
        self.assertEqual(a0 - self.a.get_balance(), self.b.get_balance() - b0)
        self.assertEqual(total_before, self.a.get_balance() + self.b.get_balance())

    def test_insufficient_funds_keeps_state(self):
        with self.assertRaises(InsufficientFundsError):
            self.a.transfer(self.b, 500)
        self.assertEqual(self.a.get_balance(), 200)
        self.assertEqual(self.b.get_balance(), 50)

    def test_invalid_amount_keeps_state(self):
        for bad in (-1, 0):
            with self.subTest(amount=bad):
                with self.assertRaises(ValueError):
                    self.a.transfer(self.b, bad)
        with self.assertRaises(TypeError):
            self.a.transfer(self.b, "10")
        self.assertEqual(self.a.get_balance(), 200)
        self.assertEqual(self.b.get_balance(), 50)

    def test_transfer_to_self(self):
        with self.assertRaises(ValueError):
            self.a.transfer(self.a, 10)
        self.assertEqual(self.a.get_balance(), 200)

    def test_transfer_to_non_account(self):
        with self.assertRaises(TypeError):
            self.a.transfer("KG002", 10)
        self.assertEqual(self.a.get_balance(), 200)


class TestBalanceAndEmpty(unittest.TestCase):
    def test_balance_after_operations(self):
        a = BankAccount("Иван", "KG001")
        b = BankAccount("Пётр", "KG002")
        a.deposit(500)
        a.withdraw(100)
        a.transfer(b, 150)
        self.assertEqual(a.get_balance(), 250)
        self.assertEqual(b.get_balance(), 150)

    def test_new_account_is_empty(self):
        self.assertTrue(BankAccount("Иван", "KG001").is_empty())

    def test_not_empty_after_deposit(self):
        acc = BankAccount("Иван", "KG001")
        acc.deposit(1)
        self.assertFalse(acc.is_empty())

    def test_empty_after_full_withdraw(self):
        acc = BankAccount("Иван", "KG001")
        acc.deposit(10)
        acc.withdraw(10)
        self.assertTrue(acc.is_empty())


if __name__ == "__main__":
    unittest.main()
