import gspread
from os import getenv
from os.path import dirname

gc = gspread.service_account(
    filename=dirname(__file__) + "/" + "./credentials-spreadsheet.json"
)


# Google Sheets API
def add_values_to_gsheet(
    row: list,
    spreadsheet_id: str,
    index: int = 2,
):
    if spreadsheet_id:
        spreadsheet = gc.open_by_key(spreadsheet_id)
        sheet_in_spreadsheet = spreadsheet.get_worksheet(0)
        sheet_in_spreadsheet.insert_row(values=row, index=index)
    else:
        print("Spreadsheet ID not given")


def write_to_gsheet(row, spreadsheet_id=getenv("SPREADSHEET_ID")):
    add_values_to_gsheet(row=row, spreadsheet_id=spreadsheet_id)
