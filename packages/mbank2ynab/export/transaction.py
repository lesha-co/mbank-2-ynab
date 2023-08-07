from dataclasses import dataclass
from typing import Union


def to_milliunits(currency: Union[int, float, str]) -> int:

    # we shouldn't use floats with monetary values
    # but YNAB operates on "milliunits", basically
    # thousandths a unit and floats are fine in this case
    # moreover, I anticipate some floats to come from Excel
    # so I have to deal with them anyway
    if type(currency) == float:
        return int(currency * 1000)
    if type(currency) == int:
        return currency * 1000

    currency2 = currency.replace(",", ".").replace(' ', '')
    return int(float(currency2)*1000)


@dataclass
class Transaction:
    date: str
    memo: str
    outflow: str
    inflow: str
    payee: str
    import_order: int

    def get_milliunits(self):
        return to_milliunits(self.inflow) - to_milliunits(self.outflow)

    def get_import_id(self):
        return f'YNAB:{self.get_milliunits()}:{self.date}:{self.import_order}'

    def is_similar(self, other: "Transaction"):
        return \
            self.get_milliunits() == other.get_milliunits() and \
            self.date == other.date
