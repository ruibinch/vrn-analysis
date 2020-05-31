import gspread
from typing import Dict, List, Union

from utils import constants

def load_worksheet(spreadsheet_id: str,
                   ws_title: str) -> List[List[str]]:
    """Loads an individual worksheet from the sheet in Google Sheets.

    Args:
        spreadsheet_id: Google Sheets ID
        ws_title: Worksheet title
    
    Returns:
        All values from the worksheet, as a list of lists.
    """

    gc = gspread.service_account(filename=constants.FILEPATH_GSHEET_CREDS)
    sheet = gc.open_by_key(spreadsheet_id)

    ws = sheet.worksheet(ws_title)
    return ws.get_all_values()

def save_to_worksheet(spreadsheet_id: str,
                      ws_title: str,
                      data: List[List[str]],
                      keep_header_row: bool) -> Dict[str, Union[str, int]]:
    """Saves the data to the specified worksheet.
    
    Steps:
    1. Add a new row to the end.
    2. Delete rows from row 2 till the 2nd-last row (omit header row).
    3. Insert new data from row 2 onwards.

    Args:
        spreadsheet_id: Google Sheets IDb
        ws_title: Worksheet title
        data: New data, in a list of lists
        keep_header_row: Whether the header row should be kept

    Returns:
        A dict with the following keys:
            - updatedRange: Cell range updated
            - updatedRows: Number of rows updated
    """

    gc = gspread.service_account(filename=constants.FILEPATH_GSHEET_CREDS)
    sheet = gc.open_by_key(spreadsheet_id)
    ws = sheet.worksheet(ws_title)

    start_row_idx = 2 if keep_header_row else 1 

    # 1. Add a new row to the end.
    ws.add_rows(1)
    # 2. Delete rows from start_row_idx till the 2nd-last row.
    ws.delete_rows(start_row_idx, ws.row_count - 1)
    # 3. Insert new data from start_row_idx onwards.
    resp = ws.insert_rows(data, start_row_idx)
    print(resp)

    return {
        constants.UPDATED_RANGE: resp[constants.UPDATES][constants.UPDATED_RANGE],
        constants.UPDATED_ROWS: resp[constants.UPDATES][constants.UPDATED_ROWS],
    }
