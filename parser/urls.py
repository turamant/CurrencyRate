from django.urls import path

from parser.views import view_index_all, export_to_csv, export_to_pdf, export_to_xlsx, \
    view_homepage, view_json, select_coins_from_form, come_back_and_clear_dict, \
    uploadFile, pdf_file_view, all_file_view

urlpatterns = [
    path('all/', view_index_all, name='index_all'),
    path('api/', view_json, name='api_json'),
    path('export_to_csv/', export_to_csv, name='export_to_csv'),
    path('export_to_pdf/', export_to_pdf, name='export_to_pdf'),
    path('export_to_xlsx/', export_to_xlsx, name='export_to_xlsx'),
    path('comeback/', come_back_and_clear_dict, name='back'),
    path('form/', select_coins_from_form, name='form'),

    path('upload/', uploadFile, name="uploadFile"),  #загрузить файл в БД
    path('all_file/', all_file_view, name='all_file'), # архивные файлы
    path('pdf_file_view/<int:id>/', pdf_file_view, name='pdf_view'),  # просмотр файла PDF из БД

    path('', view_homepage, name='home')

]
