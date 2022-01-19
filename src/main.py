from argparse import ArgumentParser
from kraken_api.api import KrakenAPI
from pathlib import Path

parser = ArgumentParser()
parser.add_argument("-f", "--fiat", type=str, dest='fiat', help="Specify fiat for conversion")
parser.add_argument("-k", "--key", "--key_path", type=str, dest='key_path', help="Specify key file to access Kraken account")

def main(
    fiat: str,
    key_path:str
):
    k_api = KrakenAPI(
        credentials=key_path,
        fiat=fiat
    )

    print(f'Total fiat: {fiat}: {k_api.balance.calculate_total_fiat()}')


if __name__ == '__main__':
    args = parser.parse_args()
    
    fiat = "USD"
    key_path = Path(__file__).parent.parent.__str__() + "/kraken.key"

    print(key_path)

    if args.fiat:
        fiat = args.fiat
    
    if args.key_path:
        key_path = args.key_path

    main(
        fiat=fiat,
        key_path = key_path
    )