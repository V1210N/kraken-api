import krakenex
from kraken_api.balance import KrakenBalance

class KrakenCredentials():
    key: str
    secret: str

    def __init__(self, key: str, secret: str) -> None:
        self.key = key
        self.secret = secret

class KrakenAPI():
    """
        Base class for wrapper around the krakenex package, used for accessing the Kraken API. Currently works in the context of a single user.
    """

    client: krakenex.API

    balance: KrakenBalance

    def __init__(
        self,
        credentials: str | KrakenCredentials,
        fiat:str="USD"
        ) -> None:
        """
            @param credentials string | KrakenCredentials\n
            Either a path to the Kraken API key file or the actual content.
            The key file must be in the following format:

            PUBLICKEY\n
            SECRETKEY\n

            You may also provide it as a KrakenCredentials class.
        """
        
        if isinstance(credentials, KrakenCredentials):
            self.client = krakenex.API(key=credentials.key, secret=credentials.secret)
        else:
            self.client = krakenex.API()
            self.client.load_key(credentials)

        self.balance = KrakenBalance(self.client, fiat)

    def __del__(self):
        self.client.close()