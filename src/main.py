from dotenv import load_dotenv
import os
from store import Store
from api import ApiClient

def get_forces() -> list[str]:
    return os.environ['FORCES'].split(',')


if __name__ == '__main__':
    load_dotenv()
    store = Store()
    print(store.database.database.list_collection_names())
    print(ApiClient.request_searches('leicestershire')[0])
    for force in get_forces():
        stop_and_search_records = ApiClient.request_searches(force)
