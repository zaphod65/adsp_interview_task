import argparse
from datetime import date
from dateutil.relativedelta import relativedelta
from dotenv import load_dotenv
import os
from store import Store
from api import ApiClient

def __get_forces_from_env() -> list[str]:
    return os.environ['FORCES'].split(',')


def parse_args():
    parser = argparse.ArgumentParser(
        prog='Police stop and search records',
        description='Retrieves stop and search records for police forces',
    )
    parser.add_argument(
        '-f',
        '--force',
        help='A valid force ID, as taken from https://data.police.uk/api/forces, defaults to a list in .env'
    )
    parser.add_argument(
        '-d',
        '--date',
        help='A date to store data for, in the format YYYY-MM, e.g. 2014-01, defaults to two months ago'
    )
    parser.add_argument(
        '--no_store',
        action='store_true',
        help='Do not persist the records to the database, display first result and exit'
    )

    return parser.parse_args()

def main(args, store, apiClient):
    if args.get('force') is not None:
        forces = [args.get('force')]
    else:
        forces = __get_forces_from_env()

    for force in forces:
        print(f'Getting records for force: {force}')
        if args.get('date') is None:
        # On some testing it seems that data is not available for this or last
        # month, API returns 502
            two_months_ago = date.today() + relativedelta(months=-2)
            search_date = two_months_ago.strftime('%Y-%m')
        else:
            search_date = args.get('date')

        try:
            stop_and_search_records = apiClient.request_searches(force, search_date)
        except Exception:
            # Assume logging happened at the site of the error
            exit(255)

        # Append force name to record so we can use this in database
        for record in stop_and_search_records:
            record['force'] = force

        if args.get('no_store'):
            try:
                print(stop_and_search_records.pop())
            except:
                print('No records returned')
            exit(0)

        try:
            store.mass_upsert(stop_and_search_records)
        except Exception:
            # Assume logging happened at the site of the error
            exit(255)


if __name__ == '__main__':
    load_dotenv()
    args = parse_args()
    main(vars(args), Store(), ApiClient)
