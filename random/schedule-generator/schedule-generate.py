import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
from pprint import pprint
from gspread.models import Cell

weekday_text = ['Monday', 'Tuesday', 'Wednesday',
                'Thursday', 'Friday', 'Saturday', 'Sunday']

spread_sheet_name = 'uet path'
sheet_name = 'schedule'
sheet_id = 0
sheet_max_rows = 13
sheet_max_cols = 8
sheet_col_px = 80
sheet_row_px = 50

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]


def clear_formatting(spread_sheet):
    body = {
        "requests": [
            {
                "updateCells": {
                    "range": {
                        "sheetId": sheet_id
                    },
                    "fields": "userEnteredFormat"
                }
            }
        ]
    }
    return spread_sheet.batch_update(body)


def clear_data(spread_sheet):
    body = {
        "requests": [
            {
                "updateCells": {
                    "range": {
                        "sheetId": sheet_id
                    },
                    "fields": "userEnteredValue"
                }
            }
        ]
    }
    return spread_sheet.batch_update(body)


def clear_all(spread_sheet):
    """Merged cells are hard to detect, create a blank sheet instead"""
    global sheet_id
    new_worksheet = spread_sheet.add_worksheet(
        title=sheet_name + '_new', rows=sheet_max_rows, cols=sheet_max_cols)
    try:
        current_sheet = spread_sheet.worksheet(sheet_name)
        spread_sheet.del_worksheet(current_sheet)
    except gspread.WorksheetNotFound:
        pass
    new_worksheet.update_title(sheet_name)
    sheet_id = new_worksheet.id
    return new_worksheet


def merge(spread_sheet, from_cell: tuple, to_cell: tuple, merge_type='MERGE_ALL'):
    """
    Fking important note: from_cell starts from 0 BUT to_cell starts from 1. haha funny
    """
    body = {
        "requests": [
            {
                "mergeCells": {
                    "mergeType": merge_type,
                    "range": {
                        "sheetId": sheet_id,
                        "startRowIndex": from_cell[0],
                        "endRowIndex": to_cell[0],
                        "startColumnIndex": from_cell[1],
                        "endColumnIndex": to_cell[1]
                    }
                }
            }
        ]
    }
    return spread_sheet.batch_update(body)


def format(spread_sheet, from_cell: tuple, to_cell: tuple,
           bg_color=(255, 255, 255), text_color=(0, 0, 0),
           wrap_strategy='LEGACY_WRAP', horizontal='TOP', vertical='LEFT'):
    """
    "from_cell" starts from 0
    "to_cell" starts from 1
    Using "repeatCell" instead of "updateCells" for editing multiple cells at once.
    """
    body = {
        "requests": [
            {
                "repeatCell": {
                    "range": {
                        "sheetId": sheet_id,
                        "startRowIndex": from_cell[0],
                        "endRowIndex": to_cell[0],
                        "startColumnIndex": from_cell[1],
                        "endColumnIndex": to_cell[1]
                    },
                    "cell": {
                        "userEnteredFormat": {
                            "backgroundColor": {
                                "red": bg_color[0] / 255,
                                "green": bg_color[1] / 255,
                                "blue": bg_color[2] / 255,
                                "alpha": 1
                            },
                            "textFormat": {
                                "foregroundColor": {
                                    "red": text_color[0] / 255,
                                    "green": text_color[1] / 255,
                                    "blue": text_color[2] / 255,
                                    "alpha": 1
                                }
                            },
                            "horizontalAlignment": horizontal,
                            "verticalAlignment": vertical,
                            "wrapStrategy": wrap_strategy
                        }
                    },
                    "fields": "userEnteredFormat"
                }
            }
        ]
    }
    return spread_sheet.batch_update(body)


def resize(spread_sheet, start=(0, 0), end=(sheet_max_rows, sheet_max_cols),
           col_px=sheet_col_px, row_px=sheet_row_px):
    body = {
        "requests": [
            {
                "updateDimensionProperties": {
                    "range": {
                        "sheetId": sheet_id,
                        "dimension": "COLUMNS",
                        "startIndex": start[1],
                        "endIndex": end[1]
                    },
                    "properties": {
                        "pixelSize": col_px
                    },
                    "fields": "pixelSize"
                }
            },
            {
                "updateDimensionProperties": {
                    "range": {
                        "sheetId": sheet_id,
                        "dimension": "ROWS",
                        "startIndex": start[0],
                        "endIndex": end[0]
                    },
                    "properties": {
                        "pixelSize": row_px
                    },
                    "fields": "pixelSize"
                }
            }
        ]
    }
    return spread_sheet.batch_update(body)


def add_subject(sheet, text: str, time: str):
    # where to write ?
    weekday = int(time.split(' ')[0][1])
    from_hour = int(time.split(' ')[1].split('-')[0])
    to_hour = int(time.split(' ')[1].split('-')[1])
    merge(sheet.spreadsheet, (from_hour, weekday-1), (to_hour+1, weekday),
          merge_type='MERGE_ALL')
    format(sheet.spreadsheet, (from_hour, weekday-1), (from_hour+1, weekday),
           bg_color=(0xff, 0xd9, 0x66), wrap_strategy='LEGACY_WRAP',
           horizontal='CENTER', vertical='MIDDLE')
    sheet.update_cell(from_hour + 1, weekday, text)


if __name__ == '__main__':
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        'creds.json', scope)
    client = gspread.authorize(creds)

    spread_sheet = client.open(spread_sheet_name)
    try:
        sheet = spread_sheet.worksheet(sheet_name)
        sheet_id = sheet.id
    except:
        pass

    # build base schedule
    clear_all(spread_sheet)
    resize(spread_sheet)
    resize(spread_sheet, start=(1, 0), end=(sheet_max_rows, 1), col_px=20)
    resize(spread_sheet, start=(0, 1), end=(1, sheet_max_cols), row_px=20)
    resize(spread_sheet, start=(1, sheet_max_cols-1), end=(sheet_max_rows, sheet_max_cols),
           col_px=70)
    format(spread_sheet, (0, 0), (13, 8),
           bg_color=(0xa5, 0xc8, 0x69), text_color=(0x0, 0x0, 0x0),
           horizontal='CENTER', vertical='MIDDLE')
    format(spread_sheet, (0, 0), (1, 8),
           bg_color=(0x57, 0xad, 0x7a), text_color=(0xff, 0xff, 0xff),
           horizontal='CENTER', vertical='MIDDLE')
    format(spread_sheet, (0, 0), (13, 1),
           bg_color=(0x57, 0xad, 0x7a), text_color=(0xff, 0xff, 0xff),
           horizontal='CENTER', vertical='MIDDLE')
    format(spread_sheet, (0, 7), (13, 8),
           bg_color=(0x57, 0xad, 0x7a), text_color=(0xff, 0xff, 0xff),
           horizontal='CENTER', vertical='MIDDLE')

    sheet = spread_sheet.worksheet(sheet_name)
    weekday_cells = sheet.range('B1:G1')
    for i, cell in enumerate(weekday_cells, start=2):
        cell.value = weekday_text[i-2]

    index_cells = sheet.range('A2:A13')
    for i, cell in enumerate(index_cells, start=1):
        cell.value = i

    time_cells = sheet.range('H2:H13')
    for i, cell in enumerate(time_cells, start=7):
        cell.value = f'{i}h - {i + 1}h'

    cell_list = weekday_cells + index_cells + time_cells
    sheet.update_cells(cell_list)

    # importing schedule
    cell_list = []
    schedule = json.loads(
        open('./schedule.json', 'rb').read(), encoding='utf-8')
    for subject in schedule:
        # getting values
        code = subject['code']
        name = subject['name']
        time = subject['time']
        location = subject['location']
        labs = []
        if 'labs' in subject:
            labs = subject['labs']

        # let's go
        text = code + '\n' + name + '\n' + location
        add_subject(sheet, text, time)
        if labs:
            for lab in labs:
                text = code + '\n' + name + ' (TH) \n' + lab['location']
                add_subject(sheet, text, lab['time'])
    pprint(sheet_id)
