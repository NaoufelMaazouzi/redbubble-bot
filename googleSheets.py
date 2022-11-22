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
    for index, key in enumerate(data):
        values = list(key.values())
        print(f'Step {index}, find {values[0]} in sheets')
        if(not sheet.findall(values[0])):
            valuesToWrite.append([values[0], ",".join( values[1]), False])
    sheet.update(f'A{next_available_row(sheet)}', valuesToWrite)


# for item in sheet.findall("kfc korea"):
#     row = sheet.row_values(item.row)
#     if(row and len(row) == 3):
#         print('okkkk')

