from datetime import datetime
from typing import List
import xlrd

from transaction import Transaction

STARTING_ROW_INDEX = 13
"""transactions start at A14 and end with one blank line"""


def get_date(DDMMYYYY: str):
    parsed_date = datetime.strptime(DDMMYYYY, "%d.%m.%Y")
    output_date = parsed_date.strftime("%Y-%m-%d")
    return output_date


def transformer(workbook: xlrd.Book) -> List[Transaction]:
    sheet: xlrd.sheet.Sheet = workbook.sheet_by_index(0)
    print(f'Using "{sheet.name}" sheet.')
    transactions: List[Transaction] = []
    for i in range(STARTING_ROW_INDEX, sheet.nrows):
        # we're switching payee and memo fields here as
        # memo is more descriptive from my experience

        date = sheet.cell_value(i, 0)
        # remember, transaction list ends with a blank line
        if date == '':
            break

        t = Transaction(
            get_date(date),  # date
            sheet.cell_value(i, 1),  # memo (originally payee)
            sheet.cell_value(i, 2),  # out
            sheet.cell_value(i, 3),  # in
            sheet.cell_value(i, 4),  # payee (originally memo)
            1
        )

        similar = list(filter(lambda T: T.is_similar(t), transactions))
        t.import_order = len(similar) + 1

        transactions.append(t)
    return transactions
