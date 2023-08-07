from http import HTTPStatus
from open_from_bytes import open_from_bytes
from transformers.mbank import transformer
from sender import send
import base64


def main(args):

    budget_id = args.get("budget_id", None)
    account_id = args.get("account_id", None)
    bearer = args.get("ynab_token", None)
    data = args.get("data", None)
    if not budget_id:
        return {
            "statusCode": HTTPStatus.BAD_REQUEST,
            "body": "Budget ID is not provided"
        }
    if not account_id:
        return {
            "statusCode": HTTPStatus.BAD_REQUEST,
            "body": "Account ID is not provided"
        }
    if not bearer:
        return {
            "statusCode": HTTPStatus.BAD_REQUEST,
            "body": "Bearer token is not provided"
        }

    if not data:
        return {
            "statusCode": HTTPStatus.BAD_REQUEST,
            "body": "Input data is missing"
        }

    source_bytes = base64.b64decode(data)

    book = open_from_bytes(source_bytes)
    transactions = transformer(book)
    result = send(transactions, budget_id, account_id, bearer)
    return {
        "statusCode": HTTPStatus.OK,
        "body": result
    }
