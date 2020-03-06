# schedule-generator

UET google sheets based timetable generator using Google Sheets API.

## Environment

Python `gspread` and `oauth2client` are required for using Google API.
```bash
python -m pip install -r requirements.txt
```

## Running the script

### The `creds.json` file

Follow the instruction [here](https://www.youtube.com/watch?v=cnPlKLEGR7E) to get a `creds.json` file. Remember to share your sheet with your Google API bot.

### Prepare `schedule.json`

Contains an array of all subjects.
```json
{
    "code": "INT1003 5",
    "name": "Tin học cơ sở 1",
    "time": "T2 10-12",
    "location": "PM208-G2",
    "labs": [
        {
            "time": "T5 5-6",
            "location": "308-GD2"
        }
    ]
}
```
- `code`: code of the subject and class.
- `name`: full name of the subject.
- `time`: a string represent the position of the class in a week `{weekday} {from}-{to}`.
- `location`: location of the class.
- `labs`: optional, some subject have one or more labs hour.

### Update your schedule

Change the spreadsheet and worksheet name to match your sheet.
```py
spread_sheet_name = 'test_sheet'
sheet_name = 'schedule'
```
Run the script
```
python schedule_generator.py
```

## References

- Google Sheets API documentation: [https://developers.google.com/sheets/api/reference/rest](https://developers.google.com/sheets/api/reference/rest)
- Python `gspread` package documentation: [https://gspread.readthedocs.io/en/latest/api.html](https://gspread.readthedocs.io/en/latest/api.html)