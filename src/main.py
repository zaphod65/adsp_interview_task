from dotenv import load_dotenv
import os
from store import Store
from api import ApiClient

def get_forces() -> list[str]:
    return os.environ['FORCES'].split(',')


if __name__ == '__main__':
    load_dotenv()
    store = Store()
    for force in get_forces():
        print(f'Getting records for force: {force}')
        stop_and_search_records = ApiClient.request_searches(force)
        # Append force name to record so we can use this in database
        for record in stop_and_search_records:
            record['force'] = force
        store.mass_upsert(stop_and_search_records)