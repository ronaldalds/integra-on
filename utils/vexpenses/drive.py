import requests
from datetime import datetime
from . models import TokenVexpenses
from time import sleep


REPORT_EXPENSES = "https://api.vexpenses.com/v2/expenses"


class Vexpenses:
    def __init__(self) -> None:
        self.session = requests.Session()
        self.report_expenses = REPORT_EXPENSES

    def _make_request(self, url, headers):
        try:
            response = self.session.get(f"{self.report_expenses}{url}", headers=headers)
            response.raise_for_status()
            return response
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except Exception as err:
            print(f"Other error occurred: {err}")
        return None

    def list_expenses(self, data: datetime):
        include = "report"
        search = f"date%3A{data.strftime("%Y-%m-%d")}"
        searchFields = "date%3A="
        searchJoin = "and"
        headers = {"Authorization": TokenVexpenses.objects.filter(nome="Administrador").first().token}
        response = self._make_request(
            f"?include={include}&search={search}&searchFields={searchFields}&searchJoin={searchJoin}",
            headers
        )
        sleep(0.25)
        if response.status_code == 200:
            chave = response.json().get("data")
            return chave
        return None
