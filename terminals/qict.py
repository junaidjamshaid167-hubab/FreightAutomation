import json
import requests
from openpyxl import load_workbook

API_URL = "https://lfs.qict.com.pk/API/api/ds/v1/Ctr-Inq"

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json, text/plain, */*",
    "Origin": "https://lfs.qict.com.pk",
    "Referer": "https://lfs.qict.com.pk/"
}


def get_container_info(container_no):
    payload = {
        "ctrnbr": container_no,
        "UserID": "Test",
        "Password": "Test",
        "Cellno": "123456"
    }

    response = requests.post(
        API_URL,
        data=payload,
        headers=HEADERS,
        timeout=30
    )

    response.raise_for_status()

    data = response.json()

    if isinstance(data, str):
        data = json.loads(data)

    result = {}

    for item in data:
        result[item["FIELD_NAME"]] = item["FIELD_VALUE"]

    return result


def process_excel(input_file,
                  output_file,
                  progress_callback=None,
                  log_callback=None):

    wb = load_workbook(input_file)
    ws = wb.active

    headers = {}
    next_col = 2

    total = ws.max_row - 1

    for index, row in enumerate(range(2, ws.max_row + 1), start=1):

        container = ws.cell(row=row, column=1).value

        if not container:
            continue

        if log_callback:
            log_callback(f"Checking {container}")

        try:

            info = get_container_info(container)

            for field, value in info.items():

                if field not in headers:

                    headers[field] = next_col
                    ws.cell(row=1, column=next_col).value = field
                    next_col += 1

                ws.cell(row=row,
                        column=headers[field]).value = value

        except Exception as e:

            ws.cell(row=row, column=2).value = str(e)

        if progress_callback:

            percent = int(index / total * 100)

            progress_callback(percent)

    wb.save(output_file)