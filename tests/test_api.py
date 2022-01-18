import unittest
from unittest.mock import patch
from kraken_balance.api import KrakenAPI
from pathlib import Path

# Useful in order to test the calculated fiat while you don't have access to an account with a balance.
MOCK_BALANCE: dict[str, str] = {
    'XBT': '1.203256',
    'USDT': '1.4030',
    'XETH': '3.29120',
    'USD': '150.00'
}


def mock_update_balance(self: KrakenAPI):
    self.balance = MOCK_BALANCE


class ApiTestCases(unittest.TestCase):
    api: KrakenAPI

    @patch.object(KrakenAPI, 'update_balance', mock_update_balance)
    def setUp(self) -> None:
        self.api = KrakenAPI(Path(__file__).parent.parent.__str__() + "/kraken.key")
        assert self.api

        return super().setUp()

    def test_update_spot_fiat(self):
        self.api.update_spot_fiat_rates()
        assert self.api.spot_fiat_rates

    def test_update_balance(self):
        self.api.update_balance()
        assert self.api.balance

    def test_calculate_total_fiat(self):
        api = self.api
        api.balance = MOCK_BALANCE

        total = api.calculate_total_fiat()
        print(f'Total fiat: {self.api.fiat} ', total)


if __name__ == '__main__':
    unittest.main()
