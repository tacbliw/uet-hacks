import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
from pprint import pprint
from gspread.models import Cell

weekday_text = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

spread_sheet_name = 'test_sheet'
# spread_sheet_id = '1_x3ON-UsXnPHbDF9vEMzMXTSb-Nh3uqY6PHaFf-O-OE'
sheet_name = 'test_s'
sheet_id = 0

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
    new_worksheet = spread_sheet.add_worksheet(title=sheet_name + '_new', rows=1000, cols=26)
    current_sheet = spread_sheet.worksheet(sheet_name)
    spread_sheet.del_worksheet(current_sheet)
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

def format(spread_sheet, cell: tuple, data: str):
    pass

def add_subject(sheet, text: str, time: str):
    # where to write ?
    weekday = int(time.split(' ')[0][1])
    from_hour = int(time.split(' ')[1].split('-')[0])
    to_hour = int(time.split(' ')[1].split('-')[1])
    merge(sheet.spreadsheet, (from_hour, weekday-1), (to_hour+1, weekday), merge_type='MERGE_ALL')
    sheet.update_cell(from_hour + 1, weekday, text)

if __name__ == '__main__':
    creds = ServiceAccountCredentials.from_json_keyfile_name('creds.json', scope)
    client = gspread.authorize(creds)

    spread_sheet = client.open(spread_sheet_name)
    sheet = spread_sheet.worksheet(sheet_name)
    sheet_id = sheet.id
    # merge(spread_sheet, (1, 1), (3, 3))

    # build base schedule
    clear_all(spread_sheet)
    weekday_cells = sheet.range('B1:F1')
    for i, cell in enumerate(weekday_cells, start=2):
        cell.value = weekday_text[i-2]

    index_cells = sheet.range('A2:A13')
    for i, cell in enumerate(index_cells, start=1):
        cell.value = i

    time_cells = sheet.range('G2:G13')
    for i, cell in enumerate(time_cells, start=7):
        cell.value = f'{i}h - {i + 1}h'

    cell_list = weekday_cells + index_cells + time_cells
    sheet.update_cells(cell_list)
    
    # importing schedule
    cell_list = []
    schedule = json.loads(open('./schedule.json', 'rb').read(), encoding='utf-8')
    for subject in schedule:
        # getting values
        code = subject['code']
        name = subject['name']
        time = subject['time']
        location = subject['location']
        labs = []
        if 'labs' in subject.keys():
            labs = subject['labs']
        
        # let's go
        text = name + '\n' + location
        add_subject(sheet, text, time)
        if labs:
            for lab in labs:
                text = name + ' (TH) \n' + lab['location']
                add_subject(sheet, text, lab['time'])

    pprint(sheet_id)