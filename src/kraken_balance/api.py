import krakenex


class KrakenAPI():
    """
        Wrapper around the krakenex package, used for accessing the Kraken API. Currently works in the context of a single user.
    """

    client: krakenex.API

    fiat: str = None
    """
        Code for the fiat to use for conversions.

        Example: "USD"
    """

    spot_fiat: dict[str, str] = {}
    """
        Holds the price conversions of spots to the configured fiat. For example, how much 1 BTC (XBT) converts to USD.

        Example:
        
        {
            "XBT": "3212.00000"
        }
    """


    balance: dict[str, str] = None
    """
        Stores user's account balance.

        Example:

        {
            "XBT": "0.4912",
            "USD": "459.23"
        }
    """

    def __init__(self, key_path: str, fiat: str="USD"):
        """
            @param key_path string\n
            Path to the Kraken API key file.
            The key must be in the following format:

            PUBLICKEY\n
            PRIVATEKEY\n

            @param fiat string\n
            Code for the fiat to use for conversions.\n
            Default: "USD"
        """

        self.fiat = fiat

        self.client = krakenex.API()
        self.client.load_key(key_path)

        self.update_balance()
        self.update_spot_fiat()



    def update_spot_fiat(self):
        """
            Retrieves fresh conversions for each of the user's spots to the configured fiat.
        """
        assert self.balance

        for spot in self.balance:
            response = self.client.query_public('Ticker', data={
                'pair': f'{spot}{self.fiat}'
            })
            
            assert response['errors'].__len__() == 0

            for key in response['result']:
                self.spot_fiat[spot] = response['result'][key]['o']
                break



    def update_balance(self):
        """
            Retrieves the user's account balance.
        """
        response = self.client.query_private('Balance')

        assert response['errors'].__len__() == 0
        assert response['result']

        self.balance = response['result']

    def get_total_fiat(self) -> float:
        total = 0

        for spot in self.spot_fiat:
            currency_amount = float(self.balance[spot])
            spot_to_fiat = float(self.spot_fiat[spot])

            total += currency_amount * spot_to_fiat

        

        return total

