import xlrd
import io


def open_from_bytes(b: bytes) -> xlrd.Book:
    """
    read a workbook from bytes
    """
    byteio = io.BytesIO(b)
    # Open the Excel workbook using xlrd
    return xlrd.open_workbook(file_contents=byteio.read())
