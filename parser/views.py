import datetime
import json
import os

import requests
import csv
import xlsxwriter

from fpdf import FPDF, HTMLMixin

from django.http import JsonResponse
from django.shortcuts import render, redirect

from parser.forms import CoinForm

URL = "https://api.coingecko.com/api/v3/simple/price/?ids=bitcoin,ethereum,ripple,cardano," \
      "litecoin,monero,dogecoin,tether,solana,polkadot&vs_currencies=usd,eur,gbp"

my_value = {}


def current_date_time():
    dt = datetime.datetime.now()
    dt_string = dt.strftime("Date: %d/%m/%Y  time: %H:%M:%S")
    return dt_string


def parser(url):
    response = requests.get(url)
    data = json.loads(response.content.decode("utf-8"))
    return data


def index(request):
    data = parser(URL)
    return render(request, 'parser/index.html', {'data': data})


def apiView(request):
    data = parser(URL)
    return JsonResponse(data)


def coin_create(request):
    data = parser(URL)
    select_keys = []
    form = CoinForm()
    if request.method == "POST":
        form = CoinForm(request.POST)
        if form.is_valid():
            for key, value in form.cleaned_data.items():
                if value:
                    select_keys.append(key)

            for k, v in data.items():
                for i in select_keys:
                    if k == i:
                        my_value[k] = v
            return render(request, "parser/detail.html", {"data": my_value})
    context = {
        "form": form,
    }
    return render(request, "parser/homepage.html", context)


def export_csv(request):
    directory = "directCSV"
    basename = "csv"
    suffix = datetime.datetime.now().strftime("%y%m%d_%H%M%S")
    file_name = ".".join([suffix, basename])
    if not os.path.isdir(directory):
        os.makedirs(directory)
    os.chdir(directory)
    with open(file_name, 'w') as f:
        w = csv.writer(f)
        w.writerow(my_value.keys())
        w.writerow(my_value.values())
    os.chdir(r'../')
    my_value.clear()
    return redirect("/")


class PDF(FPDF, HTMLMixin):
    pass


def export_pdf(request):
    directory = "directPDF"
    basename = "pdf"
    suffix = datetime.datetime.now().strftime("%y%m%d_%H%M%S")
    file_name = ".".join([suffix, basename])
    if not os.path.isdir(directory):
        os.makedirs(directory)
    os.chdir(directory)

    table1 = f"""<h1 align="center">Rate of selected coins</h1>
    <p align="center">This is {current_date_time()}</p><table border="2" align="center" width="100%">
        <thead>
            <tr>
        <th width=40%>Moneta</th>
        <th width=20%>usd</th>
        <th width=20%>euro</th>
        <th width=20%>gbp</th>
            </tr>
        </thead>
        <tbody>"""
    table2 = f""
    for key, value in my_value.items():
        if key:
            table2 += f"<tr><td>{str(key)}</td>"
        for k, v in value.items():
            if k:
                table2 += f"<td>{str(v)}</td>"
        table2 += f"</tr>"
    table3 = f"""</tbody></table>"""
    table = f"{table1}{table2}{table3}"
    pdf = PDF()
    pdf.add_page()
    pdf.write_html(table)
    pdf.output(file_name)
    os.chdir(r'../')
    my_value.clear()
    return redirect("/")


def export_xlsx(request):
    directory = "directXLSX"
    basename = "xlsx"
    suffix = datetime.datetime.now().strftime("%y%m%d_%H%M%S")
    file_name = ".".join([suffix, basename])
    if not os.path.isdir(directory):
        os.makedirs(directory)
    os.chdir(directory)

    workbook = xlsxwriter.Workbook(file_name)
    worksheet = workbook.add_worksheet("My sheet")
    worksheet.write('A1', 'Moneta..')
    worksheet.write('B1', 'usd')
    worksheet.write('C1', 'euro')
    worksheet.write('D1', 'gbp')

    # Some data we want to write to the worksheet.
    scores = [

    ]
    count = 0
    for key, value in my_value.items():
        if key:
            print("key...", key)
            scores.append([key])
        for k, v in value.items():
            if k:
                print("k...", k)
                scores[count].append(v)
        count += 1
    print("---scores---...", scores)
    # Start from the first cell. Rows and
    # columns are zero indexed.
    row = 1
    col = 0

    # Iterate over the data and write it out row by row.
    for name, usd, euro, gbp in scores:
        worksheet.write(row, col, name)
        worksheet.write(row, col + 1, usd)
        worksheet.write(row, col + 2, euro)
        worksheet.write(row, col + 3, gbp)
        row += 1
    workbook.close()
    os.chdir(r'../')
    my_value.clear()
    return redirect("/")


def back(request):
    my_value.clear()
    return redirect("/")
