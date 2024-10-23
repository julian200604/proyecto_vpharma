from django.urls import path
from . import views
from .views import sales_report_pdf, sales_report_csv

app_name = 'reports'

urlpatterns = [
    path('sales-report/', views.sales_report_pdf, name='sales_report'),
    path('salesreport/<int:pk>/download-pdf/', sales_report_pdf, name='download_pdf'),
    path('salesreport/download-csv/', sales_report_csv, name='download_csv'),  # Añadir esta ruta para CSV
]
