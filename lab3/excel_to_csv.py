import openpyxl
import csv
import pandas as pd

def excel_to_csv(excel_file, excel_name, csv_file):
    # Cargar el archivo Excel
    excel = openpyxl.load_workbook(excel_file)
    sheet = excel.active

    # Escribir los datos en un archivo CSV
    with open(csv_file, 'w', newline="") as f:
        writer = csv.writer(f)
        for row in sheet.rows:
            writer.writerow([cell.value for cell in row])
            
    pd.DataFrame(pd.read_csv(csv_file)).to_csv(excel_name, index=False)
    