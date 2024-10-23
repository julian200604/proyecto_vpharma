import io
import csv
from django.shortcuts import render
from django.http import FileResponse, HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Table, TableStyle, Paragraph, SimpleDocTemplate
from django.db.models import Sum, F
from django.utils.timezone import make_aware
from datetime import datetime
from orders.models import Order, OrderItem
from .forms import SalesReportForm
from reportlab.lib.enums import TA_CENTER

def sales_report_pdf(request):
    # Inicializamos el formulario
    form = SalesReportForm(request.GET or None)
    orders = []
    start_date = None
    end_date = None

    if form.is_valid():
        start_date = form.cleaned_data['start_date']
        end_date = form.cleaned_data['end_date']
        
        start_date = make_aware(datetime.combine(start_date, datetime.min.time()))
        end_date = make_aware(datetime.combine(end_date, datetime.max.time()))
        orders = Order.objects.filter(created__range=[start_date, end_date])

    if not orders:
        return HttpResponse("No se encontraron pedidos para las fechas seleccionadas.", content_type='text/plain')

    # Estadísticas
    total_sales = sum(order.get_total_cost() for order in orders) or 0
    total_orders = orders.count()
    avg_sales_per_order = total_sales / total_orders if total_orders else 0

    # Ventas por producto
    product_sales = OrderItem.objects.filter(order__in=orders).values('product__name').annotate(
        total_quantity=Sum('quantity'),
        total_sales=Sum(F('quantity') * F('price'))
    )

    # Crear el PDF
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)

    # Estilos
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "title_style",
        parent=styles["Title"],
        fontSize=16,
        textColor=colors.HexColor("#4CAF50"),
        alignment=TA_CENTER,
        spaceAfter=20
    )

    header_style = ParagraphStyle(
        "header_style",
        parent=styles["Heading2"],
        fontSize=12,
        textColor=colors.HexColor("#3730A3"),
        spaceAfter=15
    )

    text_style = styles["BodyText"]
    text_style.fontSize = 10

    elements = []

    # Título del informe
    elements.append(Paragraph(f"Informe de Ventas del {start_date.date()} al {end_date.date()}", title_style))

    # Sección de estadísticas
    elements.append(Paragraph("Ventas Generales", header_style))
    stats_data = [
        ["Total de Ventas", f"${total_sales:.2f}"],
        ["Total de Órdenes", str(total_orders)],
        ["Venta Promedio por Pedido", f"${avg_sales_per_order:.2f}"]
    ]
    stats_table = Table(stats_data, colWidths=[3*inch, 3*inch], hAlign='LEFT')
    stats_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#F5F5F5")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    elements.append(stats_table)
    elements.append(Paragraph("<br/>", text_style))  # Espacio

    # Tabla de ventas por producto
    elements.append(Paragraph("Ventas por Producto", header_style))
    product_data = [["Producto", "Cantidad Vendida", "Total Vendido"]]
    for item in product_sales:
        product_data.append([
            item['product__name'],
            item['total_quantity'],
            f"${item['total_sales']:.2f}"
        ])

    product_table = Table(product_data, colWidths=[3*inch, 1.5*inch, 1.5*inch], hAlign='LEFT')
    product_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#4CAF50")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('TOPPADDING', (0, 1), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
    ]))
    elements.append(product_table)

    # Build the PDF
    doc.build(elements)
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename=f"sales_report_{start_date.date()}_to_{end_date.date()}.pdf")


def sales_report_csv(request):
    # Inicializamos el formulario
    form = SalesReportForm(request.GET or None)
    orders = []
    start_date = None
    end_date = None

    if form.is_valid():
        start_date = form.cleaned_data['start_date']
        end_date = form.cleaned_data['end_date']
        
        start_date = make_aware(datetime.combine(start_date, datetime.min.time()))
        end_date = make_aware(datetime.combine(end_date, datetime.max.time()))
        orders = Order.objects.filter(created__range=[start_date, end_date])

    if not orders:
        return HttpResponse("No se encontraron pedidos para las fechas seleccionadas.", content_type='text/plain')

    # Preparar respuesta CSV
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="sales_report_{start_date.date()}_to_{end_date.date()}.csv"'

    writer = csv.writer(response)
    
    # Escribir encabezados en el archivo CSV
    writer.writerow(['Fecha', 'Número de Orden', 'Cliente', 'Total de Venta', 'Estado'])
    
    # Escribir las filas de datos de las órdenes
    for order in orders:
        customer_name = f"{order.first_name} {order.last_name}"  # Concatenar first_name y last_name
        writer.writerow([order.created.date(), order.id, customer_name, f"${order.get_total_cost():.2f}", order.get_status_display()])
    
    return response
