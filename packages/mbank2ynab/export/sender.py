import json
from typing import List
import requests
from transaction import Transaction


def send(
    transactions: List[Transaction],
    budget_id: str, account_id: str, auth_token: str
):
    try:

        _transactions = list(map(lambda T: {
            "account_id": account_id,
            "date": T.date,
            "amount": T.get_milliunits(),
            "memo": T.memo[:200],
            "payee_name": T.payee[:100],
            "cleared": "uncleared",
            "flag_color": "red",
            "import_id": T.get_import_id(),
        }, transactions))

        data = json.dumps({"transactions": _transactions})
        result = requests.post(
            f'https://api.ynab.com/v1/budgets/{budget_id}/transactions',
            headers={
                "Authorization": f"Bearer {auth_token}",
                "Content-Type": "application/json"
            },
            data=data
        )
        if not result.ok:
            return result.text, result.status_code
        data = result.json()['data']
        duplicate_import_ids = data['duplicate_import_ids']
        transaction_ids = data['transaction_ids']

        return f'Imported {len(transaction_ids)} transactions and {len(duplicate_import_ids)} duplicates discarded', 200
    except Exception as ex:
        return str(ex), 500
