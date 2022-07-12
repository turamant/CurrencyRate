import csv
import io
import os
from datetime import datetime

import xlsxwriter
from reportlab.lib.pagesizes import elevenSeventeen
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from fpdf import FPDF, HTMLMixin

coin_rate = {}  # словарь котировок криптовалют


class HTML2PDF(FPDF, HTMLMixin):
    pass


def string_current_date_time():
    """строковое представление даты и времени"""
    dt = datetime.now()
    dt_string = dt.strftime("Date: %d/%m/%Y  time: %H:%M:%S")
    return dt_string


def make_pdf_file(file_name):
    pdf = HTML2PDF()
    table1 = f"""<h1 align="center">Rate of selected coins</h1>
    <p align="center">This is {string_current_date_time()}</p><table border="1" align="center" 
    width="100%"><thead><tr><th width=40%>CryptoCurrency</th><th width=20%>usd</th>
    <th width=20%>euro</th><th width=20%>gbp</th></tr></thead><tbody>"""
    table2 = f""
    for key, value in coin_rate.items():
        if key:
            table2 += f"<tr><td>{str(key)}</td>"
        for k, v in value.items():
            if k:
                table2 += f"<td>{str(v)}</td>"
        table2 += f"</tr>"
    table3 = f"""</tbody></table>"""
    table = f"{table1}{table2}{table3}"
    pdf.add_page()
    pdf.write_html(table)
    filepath = os.path.join("media", file_name)
    pdf.output(filepath)


def make_csv_file(response):
    writer = csv.writer(response)
    writer.writerow("cryptocurrency 2022 (c) turamant")
    writer.writerow({datetime.now()})
    writer.writerow(coin_rate.keys())
    writer.writerow(coin_rate.values())


def make_xlsx_file(response):
    workbook = xlsxwriter.Workbook(response)
    worksheet = workbook.add_worksheet("My sheet")
    worksheet.write("A3", "Crypto")
    worksheet.write("B3", "usd")
    worksheet.write("C3", "euro")
    worksheet.write("D3", "gbp")
    worksheet.write("F3", string_current_date_time())
    worksheet.write("E1", "CryptoCurrencyRate 2022 (c) turamant")
    scores = [
    ]
    count = 0
    for key, value in coin_rate.items():
        if key:
            scores.append([key])
        for k, v in value.items():
            if k:
                scores[count].append(v)
        count += 1
    row = 3
    col = 0
    for name, usd, euro, gbp in scores:
        worksheet.write(row, col, name)
        worksheet.write(row, col + 1, usd)
        worksheet.write(row, col + 2, euro)
        worksheet.write(row, col + 3, gbp)
        row += 1
    workbook.close()
