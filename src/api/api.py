from datetime import date
from dateutil.relativedelta import relativedelta
import json
import requests


class ApiClient:
    def request_searches(force: str) -> list[dict]:
        # TODO: configurable date
        # On some testing it seems that data is not available for this or last
        # month, API returns 502
        two_months_ago = date.today() + relativedelta(months=-2)

        try:
            response = requests.get(
                'https://data.police.uk/api/stops-force',
                params={
                    #'date': two_months_ago.strftime('%Y-%m'),
                    'date': '2024-01',
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