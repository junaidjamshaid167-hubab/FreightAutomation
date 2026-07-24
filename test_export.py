from services.excel_export import ExcelExporter

headers = [
    "Vessel",
    "Voyage",
    "ETD",
    "ETA"
]

rows = [
    ["MSC DEMO", "001E", "28-Jul-2026", "03-Aug-2026"],
    ["MSC TEST", "002W", "29-Jul-2026", "04-Aug-2026"],
]

ExcelExporter().export(
    "output/test_schedule.xlsx",
    headers,
    rows
)

print("Done")   