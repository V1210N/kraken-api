import unittest
from kraken_balance.api import KrakenAPI

class ApiTestCases(unittest.TestCase):
    api: KrakenAPI

    def setUp(self) -> None:
        self.api = KrakenAPI("../kraken.key")
        assert self.api

        return super().setUp()

    def test_ticker(self):
        print(self.api.spot_fiat)


if __name__ == '__main__':
    unittest.main()
