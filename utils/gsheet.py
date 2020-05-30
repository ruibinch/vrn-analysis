import gspread
from typing import List

def load_worksheet(spreadsheet_id: str,
                   ws_title: str) -> List[List[str]]:
    """Loads an individual worksheet from the sheet in Google Sheets.

    Args:
        spreadsheet_id: Google Sheets ID
        ws_title: Worksheet title
    
    Returns:
        All values from the worksheet, as a list of lists.
    """

    gc = gspread.service_account(filename='configs/gsheet_creds.json')
    sheet = gc.open_by_key(spreadsheet_id)

    ws = sheet.worksheet(ws_title)
    return ws.get_all_values()

def save_to_worksheet(ws_title: str, data: List[List[str]]) -> None:
    """Saves the data to the specified worksheet."""

    # TODO: most likely needed