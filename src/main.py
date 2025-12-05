import argparse
from datetime import date
from dateutil.relativedelta import relativedelta
from dotenv import load_dotenv
import os
from store import Store
from api import ApiClient

def get_forces_from_env() -> list[str]:
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


if __name__ == '__main__':
    load_dotenv()
    args = parse_args()

    store = Store()
    if args.force is not None:
        forces = [args.force]
    else:
        forces = get_forces_from_env()

    for force in forces:
        print(f'Getting records for force: {force}')
        if args.date is None:
            two_months_ago = date.today() + relativedelta(months=-2)
            search_date = two_months_ago.strftime('%Y-%m')
        else:
            search_date = args.date

        stop_and_search_records = ApiClient.request_searches(force, search_date)

        # Append force name to record so we can use this in database
        for record in stop_and_search_records:
            record['force'] = force

        if args.no_store:
            print(stop_and_search_records.pop())
            exit(0)

        store.mass_upsert(stop_and_search_records)