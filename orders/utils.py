from io import BytesIO
from django.http import HttpResponse
from django.conf import settings
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Image, Spacer
from .models import Order
import os

def create_invoice_pdf(order_id):
    try:
        # Obtener el pedido
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return HttpResponse('El pedido no existe.', status=404)

    # Crear un buffer en memoria para el PDF
    buffer = BytesIO()

    # Crear un objeto SimpleDocTemplate para el PDF
    doc = SimpleDocTemplate(buffer, pagesize=letter)

    # Estilos
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('Title', fontSize=18, spaceAfter=12, alignment=1)  # Centrado
    normal_style = ParagraphStyle('Normal', fontSize=12, alignment=0, spaceAfter=6)

    # Estilo de tabla
    table_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),  # Fondo de encabezado
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),  # Color de texto en encabezado
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Texto centrado
        ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),  # Fondo de filas
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),  # Bordes de celdas
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Fuente en encabezado
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica')  # Fuente en cuerpo
    ])

    # Contenido
    content = []

    # Encabezado con logotipo
    logo_path = os.path.join(settings.BASE_DIR, 'static/img/logo_v_pharma.png')  # Ajusta la ruta según tus archivos
    if os.path.isfile(logo_path):
        logo = Image(logo_path, width=2*inch, height=1*inch)
        content.append(logo)
    else:
        content.append(Paragraph('Logotipo no encontrado', normal_style))

    # Espacio después del logo
    content.append(Spacer(1, 12))

    # Información de la empresa
    content.append(Paragraph('V-Pharma', title_style))
    content.append(Paragraph('Número Teléfono: 312 6647917', normal_style))
    content.append(Paragraph('Correo: v-pharma@gmail.com', normal_style))
    
    # Espacio adicional
    content.append(Spacer(1, 12))

    # Detalles de la factura
    content.append(Paragraph(f'Factura #{order.id}', title_style))
    content.append(Paragraph(f'Fecha: {order.created.strftime("%Y-%m-%d")}', normal_style))
    content.append(Paragraph(f'Nombre: {order.first_name} {order.last_name}', normal_style))
    content.append(Paragraph(f'Correo: {order.email}', normal_style))
    content.append(Paragraph(f'Dirección: {order.address}', normal_style))
    content.append(Paragraph(f'Ciudad: {order.city}', normal_style))
    
    # Espacio adicional
    content.append(Spacer(1, 12))
    
    # Generar tabla de detalles de la orden
    data = [['Cantidad', 'Producto', 'Precio']]
    for item in order.items.all():
        data.append([item.quantity, item.product.name, f'${item.price:.2f}'])
    data.append(['', 'Total', f'${order.get_total_cost():.2f}'])

    # Crear la tabla con estilo
    table = Table(data)
    table.setStyle(table_style)
    
    # Agregar la tabla al contenido
    content.append(table)

    # Pie de página
    content.append(Spacer(1, 24))  # Espacio adicional antes del pie de página
    content.append(Paragraph('¡Gracias por tu compra!', normal_style))
    content.append(Paragraph('Esta es una factura descargable. Por favor guárdela para sus registros.', normal_style))
    
    # Construir el PDF
    doc.build(content)

    # Obtener el contenido del PDF
    pdf_content = buffer.getvalue()
    buffer.close()

    # Crear una respuzzesta HTTP para el archivo PDF
    response = HttpResponse(pdf_content, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="invoice_{order_id}.pdf"'
    
    return response

