"""Unit tests for bank.py"""

import pytest

from bank_api.bank import Bank, Account


@pytest.fixture
def bank() -> Bank:
    return Bank()


def test_accounts_are_immutable():
    account = Account('Immutable')
    with pytest.raises(Exception):
        # This operation should raise an exception
        account.name = 'Mutable'


def test_bank_creates_empty(bank):
    assert len(bank.accounts) == 0
    assert len(bank.transactions) == 0


def test_can_create_and_get_account(bank):
    bank.create_account('Test')
    account = bank.get_account('Test')

    assert len(bank.accounts) == 1
    assert account.name == 'Test'


def test_cannot_duplicate_accounts(bank):
    bank.create_account('duplicate')
    bank.create_account('duplicate')

    assert len(bank.accounts) == 1


def test_cannot_modify_accounts_set(bank):
    accounts = bank.accounts
    accounts.add(Account('New Account'))

    assert len(bank.accounts) == 0


def test_add_funds_to_account(bank):

    expectedAccount = bank.create_account('Test')

    amount = 100
    bank.add_funds(expectedAccount.name, amount)

    transactions = bank.transactions
    transaction = transactions.pop()

    assert transaction.amount == amount
    assert transaction.account == expectedAccount

def test_transactions_count_to_account(bank):

    account1 = bank.create_account('Account1')
    account2 = bank.create_account('Account2')
    amount = 100

    noTransactions = len(bank.transactions)

    bank.add_funds(account1.name, amount)
    bank.add_funds(account2.name, amount + 10)
    bank.add_funds(account1.name, amount + 20)
    bank.add_funds(account2.name, amount - 40)

    fourTransactions = len(bank.transactions)    

    assert noTransactions == 0
    assert fourTransactions == 4

def test_same_amount_of_transaction_adds_separately(bank):
    account1 = bank.create_account('Account1')
    amount = 100

    noTransactions = len(bank.transactions)

    bank.add_funds(account1.name, amount)
    bank.add_funds(account1.name, amount)

    twoTransactions = len(bank.transactions)    

    assert noTransactions == 0
    assert twoTransactions == 2
    

def test_can_add_negative_amount(bank):
    account1 = bank.create_account('Account1')
    amount = -100

    bank.add_funds(account1.name, amount)

    transactions = bank.transactions
    transaction = transactions.pop()

    assert transaction.amount == amount