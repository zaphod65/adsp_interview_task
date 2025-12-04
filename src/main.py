from dotenv import load_dotenv
import os

def get_forces() -> list[str]:
    return os.environ['FORCES'].split(',')


if __name__ == '__main__':
    load_dotenv()
    for force in get_forces():
        print(force)
