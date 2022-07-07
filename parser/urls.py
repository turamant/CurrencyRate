from django.urls import path

from parser.views import index, coin_create, export_csv, export_pdf, back, export_xlsx

urlpatterns = [
    path('all/', index, name='index'),
    path('export_csv/', export_csv, name='export_csv'),
    path('export_pdf/', export_pdf, name='export_pdf'),
    path('export_xlsx/', export_xlsx, name='export_xlsx'),
    path('back/', back, name='back'),
    path('', coin_create, name='homepage'),

]
