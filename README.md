The intent of this application is to retrieve a user's Kraken balance as a fiat value. Any spot values present in the account's balance are converted to fiat using [Kraken's ticker](https://www.kraken.com/en-us/prices?quote=USD).

If not specified, the application uses USD as the fiat.

# Requirements

1. Python version 3.0 or greater and `pip`.
2. A Kraken account with at least some balance.
    - If your Kraken account has no balance, the app will fail.
        - Tests still work though, using mock data. These can be run with `python -m unittest test_api.py` from within the tests folder.
3. Credentials for an API key (public key and private key) with access to query funds.

Make sure you aren't confusing `Kraken` with `Kraken Futures`. These use different APIs and currently this project doesn't support Kraken Futures.

# Setup

1. Run `setup.py` and `pip install -r requirements.txt` to setup the project.

2. Create a `kraken.key` file at the project root. It should follow this format:
```
    PUBLICAPIKEY
    PRIVATEAPIKEY
```

3. Run `python src/main.py`. This will log your account balance as a fiat.


### Options

You can add the following arguments to `python src/main.py`:

- `-k --key --key_path`: Specify a different authentication key file path. Defaults to "../kraken.key".

- `-f --fiat`: Specify a fiat value to convert the account balance to. Defaults to USD. [List of supported fiats](https://support.kraken.com/hc/en-us/articles/360000381846).

## TO-DO

- Currently doesn't make conversions from one fiat to another. This means that if you have 100 EUR and attempt to get your balance in USD, the USD tally will not include the EUR.
