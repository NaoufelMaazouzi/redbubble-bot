import gspread
from oauth2client.service_account import ServiceAccountCredentials

def next_available_row(worksheet):
    str_list = list(filter(None, worksheet.col_values(1)))
    return str(len(str_list)+1)

scopes = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds = ServiceAccountCredentials.from_json_keyfile_name("secret_key.json", scopes=scopes)
file = gspread.authorize(creds)
workbook = file.open("test redbubble")
sheet = workbook.sheet1

valuesToWrite = []
def writeData(data):
    for key in data:
        values = list(key.values())
        valuesToWrite.append([values[0], ",".join( values[1]), False])
    print(f'Add {len(valuesToWrite)} values in sheets')
    if len(valuesToWrite):
        sheet.update(f'A{next_available_row(sheet)}', valuesToWrite)

def getAllNichesFromSheets():
    list_of_lists = sheet.get_all_records()
    return [o['Niches'] for o in list_of_lists]
