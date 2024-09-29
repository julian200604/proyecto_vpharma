import io
from django.shortcuts import render
from django.http import FileResponse, HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER
from django.db.models import Sum, F
from django.utils.timezone import make_aware
from datetime import datetime
from orders.models import Order, OrderItem
from .forms import SalesReportForm

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

    # Calcular estadísticas
    total_sales = OrderItem.objects.filter(order__created__range=[start_date, end_date])\
        .aggregate(total_sales=Sum(F('price') * F('quantity')))['total_sales'] or 0
    total_orders = orders.count()
    avg_sales_per_order = total_sales / total_orders if total_orders > 0 else 0

    product_sales = OrderItem.objects.filter(
        order__created__range=[start_date, end_date]
    ).values('product__name').annotate(
        total_quantity=Sum('quantity'),
        total_sales=Sum(F('quantity') * F('price'))
    ).order_by('-total_sales')

    # Crear el PDF
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)

    # Estilos personalizados
    p.setStrokeColor(colors.HexColor("#4CAF50"))  # Color verde para líneas
    p.setLineWidth(1)
    p.setFont("Helvetica-Bold", 14)
    
    # Encabezado del informe con un rectángulo
    p.setFillColor(colors.HexColor("#F5F5F5"))
    p.rect(50, 770, 500, 40, fill=1)
    p.setFillColor(colors.HexColor("#000000"))
    p.drawCentredString(300, 780, f"Informe de ventas del {start_date.date()} al {end_date.date()}")

    # Sección de estadísticas con líneas divisorias
    p.setFont("Helvetica", 10)
    y = 740
    p.drawString(100, y, f"Total de ventas: ${total_sales:.2f}")
    y -= 20
    p.drawString(100, y, f"Total de órdenes: {total_orders}")
    y -= 20
    p.drawString(100, y, f"Venta promedio por pedido: ${avg_sales_per_order:.2f}")
    y -= 30

    p.setStrokeColor(colors.HexColor("#000000"))
    p.line(80, y, 520, y)
    y -= 20

    # Ventas por producto
    p.setFont("Helvetica-Bold", 12)
    p.drawString(100, y, "Ventas por producto:")
    y -= 20
    p.setFont("Helvetica", 10)
    for item in product_sales:
        product_info = f"{item['product__name']} - Cantidad: {item['total_quantity']} - Total vendido: ${item['total_sales']:.2f}"
        p.drawString(100, y, product_info)
        y -= 20
        if y < 100:
            p.showPage()
            p.setFont("Helvetica", 10)
            y = 800
    

    # Finalizar el PDF
    p.showPage()
    p.save()

    # Volver al inicio del buffer
    buffer.seek(0)

    # Devolver el archivo PDF como respuesta
    return FileResponse(buffer, as_attachment=True, filename=f'sales_report_{start_date.date()}_to_{end_date.date()}.pdf')
