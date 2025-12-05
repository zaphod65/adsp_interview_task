import json
import requests
from urllib3.exceptions import HTTPError


class ApiClient:
    def request_searches(force: str, date: str) -> list[dict]:
        # TODO: configurable date
        # On some testing it seems that data is not available for this or last
        # month, API returns 502

        try:
            response = requests.get(
                'https://data.police.uk/api/stops-force',
                params={
                    'date': date,
                    'force': force,
                },
                headers={
                    'accept': 'application/json',
                }
            )
            response.raise_for_status()
        except HTTPError as http_error:
            print(f'HTTP error: {http_error}')
        except Exception as error:
            print(f'Non-http error: {error}')

        return json.loads(response.text)