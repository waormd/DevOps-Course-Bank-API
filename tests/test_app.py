"""Integration tests for app.py"""
import pytest

from dataclasses import asdict
from bank_api.app import app
from bank_api.bank import Account


@pytest.fixture
def client():
    app.config['TESTING'] = True
    return app.test_client()


def test_account_creation(client):
    testAccount = "Account1"

    response = client.post(f"/accounts/{testAccount}")
    assert response.status_code == 200

    response = client.get(f"/accounts/{testAccount}")
    assert response.status_code == 200
    assert response.json == asdict(Account(testAccount))


def test_get_account_that_doesnt_exist_gives_404(client):
    uncreatedAccount = "UncreatedAccount"

    response = client.get(f"/accounts/{uncreatedAccount}")
    assert response.status_code == 404
    assert response.json == {"message": "Account not found"}