"""
Exports Activity Tracker tab to CSV for easy import to Google Sheets.
"""
import csv
import openpyxl

wb = openpyxl.load_workbook("PankhuriGovila_YIRP_Project_Tracker.xlsx")
ws = wb["Activity Tracker"]

with open("PankhuriGovila_YIRP_Project_Tracker.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    for row in ws.iter_rows(values_only=True):
        writer.writerow(row)

print("Exported PankhuriGovila_YIRP_Project_Tracker.csv successfully.")

