from django.urls import path

from parser.views import view_index_all, export_to_csv, export_to_pdf, export_to_xlsx, \
    view_homepage, view_json, select_coins_from_form, came_back_and_clear_dict

urlpatterns = [
    path('all/', view_index_all, name='index_all'),
    path('api/', view_json, name='api_json'),
    path('export_to_csv/', export_to_csv, name='export_to_csv'),
    path('export_to_pdf/', export_to_pdf, name='export_to_pdf'),
    path('export_to_xlsx/', export_to_xlsx, name='export_to_xlsx'),
    path('back/', came_back_and_clear_dict, name='back'),
    path('form/', select_coins_from_form, name='form'),
    path('', view_homepage, name='homepage')

]
