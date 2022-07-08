from datetime import datetime
import json
import os

import requests
import csv
import xlsxwriter
from fpdf import FPDF, HTMLMixin

from django.http import JsonResponse
from django.shortcuts import render, redirect

from parser.forms import CoinForm


class PDF(FPDF, HTMLMixin):
    """HTML -> PDF"""
    pass


URL = "https://api.coingecko.com/api/v3/simple/price/?ids=bitcoin,ethereum,ripple,cardano," \
      "litecoin,monero,dogecoin,tether,solana,polkadot&vs_currencies=usd,eur,gbp"

coin_rate = {}  # словарь котировок криптовалют


def string_current_date_time():
    """строковое представление даты и времени"""
    dt = datetime.now()
    dt_string = dt.strftime("Date: %d/%m/%Y  time: %H:%M:%S")
    return dt_string


def response_api():
    """ответ на запрос от URL"""
    response = requests.get(URL)
    data = json.loads(response.content.decode("utf-8"))
    return data


def view_index_all(request):
    """показ котировок всех монет"""
    data = response_api()
    for k, v in data.items():
        coin_rate[k] = v
    return render(request, 'parser/index_all.html', {'data': data})


def view_homepage(request):
    """показ главной страницы"""
    coin_rate.clear()
    return render(request, 'parser/homepage.html')


def view_json(request):
    """показ api/json"""
    data = response_api()
    return JsonResponse(data)


def came_back_and_clear_dict(request):
    """очистить словарь и вернуться назад к форме"""
    coin_rate.clear()
    return redirect("form")


def select_coins_from_form(request):
    """выбрать монеты из формы"""
    data = response_api()
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
                        coin_rate[k] = v
            return render(request, "parser/detail.html", {"data": coin_rate})
    context = {
        "form": form,
    }
    return render(request, "parser/form.html", context)


def export_to_csv(request):
    """экспортировать в csv"""
    directory = "directCSV"
    file_name = 'file_{}.csv'.format(datetime.now().strftime("%d%m%Y_%H%M%S"))
    if not os.path.isdir(directory):
        os.makedirs(directory)
    os.chdir(directory)
    with open(file_name, 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(string_current_date_time())
        w.writerow(coin_rate.keys())
        w.writerow(coin_rate.values())
    os.chdir(r'../')
    coin_rate.clear()
    return redirect("form")


def export_to_pdf(request):
    """экспортировать в pdf"""
    directory = "directPDF"
    file_name = 'file_{}.pdf'.format(datetime.now().strftime("%d%m%Y_%H%M%S"))
    if not os.path.isdir(directory):
        os.makedirs(directory)
    os.chdir(directory)
    table1 = f"""<h1 align="center">Rate of selected coins</h1>
    <p align="center">This is {string_current_date_time()}</p><table border="2" align="center" 
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
    pdf = PDF()
    pdf.add_page()
    pdf.write_html(table)
    pdf.output(file_name)
    os.chdir(r'../')
    coin_rate.clear()
    return redirect("form")


def export_to_xlsx(request):
    """экспортировать в pdf"""
    directory = "directXLSX"
    file_name = 'file_{}.xlsx'.format(datetime.now().strftime("%d%m%Y_%H%M%S"))
    if not os.path.isdir(directory):
        os.makedirs(directory)
    os.chdir(directory)
    workbook = xlsxwriter.Workbook(file_name)
    worksheet = workbook.add_worksheet("My sheet")
    worksheet.write('A1', 'CryptoCurrency')
    worksheet.write('B1', 'usd')
    worksheet.write('C1', 'euro')
    worksheet.write('D1', 'gbp')
    worksheet.write('F1', string_current_date_time())
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
    row = 1
    col = 0
    for name, usd, euro, gbp in scores:
        worksheet.write(row, col, name)
        worksheet.write(row, col + 1, usd)
        worksheet.write(row, col + 2, euro)
        worksheet.write(row, col + 3, gbp)
        row += 1
    workbook.close()
    os.chdir(r'../')
    coin_rate.clear()
    return redirect("form")



