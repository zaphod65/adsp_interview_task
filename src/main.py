from dotenv import load_dotenv
import os
from store import Store

def get_forces() -> list[str]:
    return os.environ['FORCES'].split(',')


if __name__ == '__main__':
    load_dotenv()
    store = Store()
    print(store.database.database.list_collection_names())
    for force in get_forces():
        print(force)
