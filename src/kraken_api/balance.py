import krakenex

FIAT_CURRENCIES = [
    'USD',
    'EUR',
    'CAD',
    'AUD',
    'GBP',
    'CHF',
    'JPY'
]


class KrakenBalance():
    client: krakenex.API

    """
        Inherits from KrakenAPI. This class is used for balance-related operations, such as retrieving the account balance, spot to fiat rates, and calculating totals.
    """

    fiat: str = None
    """
        Code for the fiat to use for conversions.

        Example: "USD"
    """

    spot_fiat_rates: dict[str, str] = {}
    """
        Holds the price conversions of spots to the configured fiat. For example, how much 1 BTC (XBT) converts to USD.

        Example:

        {
            "XBT": "3212.00000"
        }
    """

    account_balance: dict[str, str] = None
    """
        Stores user's account balance.

        Example:

        {
            "XBT": "0.4912",
            "USD": "459.23"
        }
    """

    def __init__(self, client: krakenex.API, fiat: str = "USD") -> None:
        """
            @param fiat string
            Code for the fiat to use for conversions.\n
            Default: "USD"
        """

        self.client = client

        if fiat not in FIAT_CURRENCIES:
            raise Exception('Invalid fiat provided: ', fiat)
        self.fiat = fiat

        self.update_balance()
        self.update_spot_fiat_rates()
    
    def __del__(self):
        self.client.close()

    def update_spot_fiat_rates(self):
        """
            Retrieves fresh conversions for each of the user's spots to the configured fiat.
        """
        assert self.account_balance

        # Maps a query to the currency type.
        # i.e.: If fiat is USD, then XETHUSD is mapping for 1 ETH's value when converted to USD.
        # { "XETH" : "ETH" }
        spot_queries: dict[str, str] = {}
        query_str = ''

        for currency in self.account_balance:
            # Skip the fiat entries
            if currency in FIAT_CURRENCIES:
                continue

            # Normalize the input. Currencies that have less than 4 digits have prefixing "F"s. Spots and fiats are separated by a "Z".
            spot = currency
            while spot.__len__() < 4:
                spot = f'X{spot}'

            query = f'{spot}Z{self.fiat}'
            spot_queries[query] = currency
            query_str += f'{query},'

        assert spot_queries.__len__() > 0
        query_str = query_str.removesuffix(",")

        response = self.client.query_public('Ticker', data={
            'pair': query_str
        })

        if response['error'].__len__() > 0:
            raise Exception(
                'Received errors while attempting to update spot fiat conversions.\n',
                f'Query: {query_str}',
                response['error'])

        # Each key here corresponds to a spot_queries key.
        for key in response['result']:
            currency = spot_queries[key]
            self.spot_fiat_rates[currency] = response['result'][key]['o']

    def update_balance(self):
        """
            Retrieves the user's account balance.
        """
        response = self.client.query_private('Balance')

        if response['error'].__len__() > 0:
            raise Exception(
                'Received errors while attempting to update balance. ', response['error'])

        if 'result' not in response or response['result'] is None:
            raise Exception(
                'Empty response while attempting to update balance.')

        self.account_balance = response['result']

    def calculate_total_fiat(self, update=False) -> float:
        """
            Calculates the total fiat based on the account's balance and the retrieved spot to fiat rates.

            Note that by default this doesn't update either the balance or the spot to fiat races, but instead uses what's already stored.
        """
        if (update):
            self.update_balance()
            self.update_spot_fiat_rates()

        total = 0

        for spot in self.spot_fiat_rates:
            currency_amount = float(self.account_balance[spot])
            spot_to_fiat = float(self.spot_fiat_rates[spot])

            total += currency_amount * spot_to_fiat

        # Add the fiat itself.
        if self.fiat in self.account_balance:
            total += float(self.account_balance[self.fiat])

        return total
