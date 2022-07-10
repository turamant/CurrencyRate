from datetime import datetime
import json
import os

import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import elevenSeventeen

import requests
import csv
import xlsxwriter
from fpdf import FPDF, HTMLMixin

from django.http import JsonResponse, FileResponse, HttpResponse
from django.shortcuts import render, redirect

from parser import models
from parser.forms import CoinForm
from parser.models import Document


class HtmlPdf(FPDF, HTMLMixin):
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
    return render(request, 'parser/index-all.html', {'data': data})


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
    file_name = '{}.csv'.format(datetime.now().strftime("%d%m%Y_%H%M%S"))
    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': f'attachment; filename={file_name}'},
    )
    writer = csv.writer(response)
    writer.writerow("cryptocurrency 2022 (c) turamant")
    writer.writerow({datetime.now()})
    writer.writerow(coin_rate.keys())
    writer.writerow(coin_rate.values())
    return response


def export_to_pdf(request):
    """экспортировать в pdf"""
    file_name = '{}.pdf'.format(datetime.now().strftime("%d%m%Y_%H%M%S"))
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=elevenSeventeen, bottomup=0)
    text_obj = c.beginText()
    text_obj.setTextOrigin(inch, inch)
    text_obj.setFont("Helvetica", 12)

    lines = []

    for key, value in coin_rate.items():
        lines.append(str(key))
        for k, v in value.items():
            lines.append((str(k)))
            lines.append(str(v))

    for line in lines:
        text_obj.textLine(line)

    c.drawString(20, 10, f'{string_current_date_time()}')
    c.drawString(300, 20, "Cryptocurrency rate 2022 (c) turamant")
    c.drawText(text_obj)
    c.showPage()
    c.save()
    buf.seek(0)
    response = FileResponse(buf, as_attachment=True, filename=file_name)
    return response


def export_to_xlsx(request):
    """экспортировать в pdf"""
    file_name = '{}.xlsx'.format(datetime.now().strftime("%d%m%Y_%H%M%S"))
    response = HttpResponse(
        content_type='text/xlsx',
        headers={'Content-Disposition': f'attachment; filename={file_name}'},
    )
    workbook = xlsxwriter.Workbook(response)
    worksheet = workbook.add_worksheet("My sheet")
    worksheet.write('A3', 'Crypto')
    worksheet.write('B3', 'usd')
    worksheet.write('C3', 'euro')
    worksheet.write('D3', 'gbp')
    worksheet.write('F3', string_current_date_time())
    worksheet.write('E1', 'CryptoCurrencyRate 2022 (c) turamant')
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
    return response

#===========================================  дополнительные ф-ции

def all_file_view(request):
    """Показать список всех файлов в БД"""
    documents = models.Document.objects.all()
    return render(request, 'parser/all-file.html', context={
        "files": documents})


def pdf_view(request, id):
    """ Готово вывод на экран файла PDF"""
    obj = Document.objects.get(pk=id)
    file = str(obj.uploadedFile)
    filepath = os.path.join('media', file)
    return FileResponse(open(filepath, 'rb'), content_type='application/pdf')


def uploadFile(request):
    """Загрузить в БД свои файлы"""
    if request.method == "POST":
        # Fetching the form data
        fileTitle = request.POST["fileTitle"]
        uploadedFile = request.FILES["uploadedFile"]

        # Saving the information in the database
        document = models.Document(
            title=fileTitle,
            uploadedFile=uploadedFile
        )
        document.save()

    documents = models.Document.objects.all()

    return render(request, "parser/upload-file.html", context={
        "files": documents
    })

