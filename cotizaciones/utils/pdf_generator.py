"""
Generador de PDFs para cotizaciones
Utiliza ReportLab para crear documentos profesionales
"""
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
from io import BytesIO
from datetime import datetime
import os
from django.conf import settings

from .folio import calcular_precio_con_iva


def generate_quote_pdf(cotizacion):
    """
    Genera un PDF profesional para una cotizacion
    
    Args:
        cotizacion: Instancia del modelo Cotizacion
        
    Returns:
        BytesIO: Buffer con el PDF generado
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter,
                           rightMargin=2*cm, leftMargin=2*cm,
                           topMargin=2*cm, bottomMargin=2*cm)
    
    # Contenedor para los elementos del PDF
    elements = []
    
    # Estilos globales
    styles = getSampleStyleSheet()
    
    # Estilo personalizado para el título
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#2C3E50'),
        spaceAfter=30,
        alignment=TA_CENTER
    )
    
    # Estilo para subtítulos
    subtitle_style = ParagraphStyle(
        'Subtitle',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#34495E'),
        spaceAfter=12,
        spaceBefore=20
    )
    
    # Estilo para texto normal
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=10,
        leading=14,
    )
    
    # ===== ENCABEZADO =====
    # Logo (si existe)
    logo_path = os.path.join(settings.BASE_DIR, 'static', 'img', 'logo.jpg')
    if os.path.exists(logo_path):
        try:
            logo = Image(logo_path, width=3*cm, height=3*cm)
            logo.hAlign = 'LEFT'
            elements.append(logo)
            elements.append(Spacer(1, 0.5*cm))
        except:
            pass  # Si hay error con el logo, continuar sin él
    
    # Información de la empresa
    empresa_data = [
        [Paragraph('<b>MUEBLES BARGUAY</b>', normal_style), ''],
        [Paragraph('Av Lo Espejo 964, El Bosque, Santiago', normal_style), ''],
        [Paragraph('Email: contacto@mueblesbarguay.cl', normal_style), ''],
        [Paragraph('Teléfono: +569 1234 5678', normal_style), '']
    ]
    
    empresa_table = Table(empresa_data, colWidths=[10*cm, 6*cm])
    empresa_table.setStyle(TableStyle([
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#2C3E50')),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    elements.append(empresa_table)
    elements.append(Spacer(1, 1*cm))
    
    # Folio y fecha
    folio_data = [
        [Paragraph(f'<b>COTIZACIÓN Nº {cotizacion.folio}</b>', 
                  ParagraphStyle('FolioStyle', fontSize=16, textColor=colors.HexColor('#E74C3C'), alignment=TA_RIGHT))]
    ]
    folio_table = Table(folio_data, colWidths=[16*cm])
    elements.append(folio_table)
    
    fecha_actual = datetime.now().strftime('%d de %B de %Y')
    elements.append(Paragraph(f'Fecha: {fecha_actual}', 
                             ParagraphStyle('DateStyle', fontSize=10, alignment=TA_RIGHT, spaceAfter=20)))
    elements.append(Spacer(1, 0.5*cm))
    
    # Línea separadora
    line_data = [['', '']]
    line_table = Table(line_data, colWidths=[16*cm])
    line_table.setStyle(TableStyle([
        ('LINEABOVE', (0, 0), (-1, 0), 2, colors.HexColor('#34495E')),
    ]))
    elements.append(line_table)
    elements.append(Spacer(1, 0.5*cm))
    
    # ===== INFORMACIÓN DEL CLIENTE =====
    elements.append(Paragraph('DATOS DEL CLIENTE', subtitle_style))
    
    cliente_data = [
        ['Nombre:', cotizacion.nombre_completo],
        ['RUT:', cotizacion.rut if cotizacion.rut else 'No proporcionado'],
        ['Email:', cotizacion.email],
        ['Dirección:', cotizacion.direccion if cotizacion.direccion else 'No proporcionada'],
        ['Teléfono:', cotizacion.telefono if cotizacion.telefono else 'No proporcion ado'],
    ]
    
    cliente_table = Table(cliente_data, colWidths=[4*cm, 12*cm])
    cliente_table.setStyle(TableStyle([
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#2C3E50')),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    elements.append(cliente_table)
    elements.append(Spacer(1, 0.7*cm))
    
    # ===== DETALLES DEL PRODUCTO =====
    elements.append(Paragraph('DETALLES DEL PRODUCTO', subtitle_style))
    
    producto_nombre = cotizacion.producto.nombre if cotizacion.producto else "Diseño Personalizado"
    producto_desc = cotizacion.producto.descripcion if cotizacion.producto else "Mueble a medida según especificaciones del cliente"
    
    producto_data = [
        ['Producto:', producto_nombre],
        ['Descripción:', producto_desc],
        ['Material Preferido:', cotizacion.get_material_preferido_display()],
    ]
    
    producto_table = Table(producto_data, colWidths=[4*cm, 12*cm])
    producto_table.setStyle(TableStyle([
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#2C3E50')),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    elements.append(producto_table)
    elements.append(Spacer(1, 0.5*cm))
    
    # ===== DIMENSIONES =====
    elements.append(Paragraph('DIMENSIONES DEL ESPACIO', subtitle_style))
    
    dimensiones_data = [
        ['Ancho:', f'{cotizacion.medidas_ancho} cm'],
        ['Alto:', f'{cotizacion.medidas_alto} cm'],
        ['Fondo/Profundidad:', f'{cotizacion.medidas_profundidad} cm'],
    ]
    
    dimensiones_table = Table(dimensiones_data, colWidths=[4*cm, 12*cm])
    dimensiones_table.setStyle(TableStyle([
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#2C3E50')),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    elements.append(dimensiones_table)
    elements.append(Spacer(1, 0.7*cm))
    
    # ===== DESGLOSE DE PRECIOS =====
    elements.append(Paragraph('COTIZACIÓN', subtitle_style))
    
    # Calcular precios
    if cotizacion.precio_cotizado:
        precios = calcular_precio_con_iva(cotizacion.precio_cotizado)
        subtotal_str = f'${precios["subtotal"]:,.0f}'.replace(',', '.')
        iva_str = f'${precios["iva"]:,.0f}'.replace(',', '.')
        total_str = f'${precios["total"]:,.0f}'.replace(',', '.')
    else:
        subtotal_str = 'Por definir'
        iva_str = 'Por definir'
        total_str = 'Por definir'
    
    precios_data = [
        ['', 'CONCEPTO', 'VALOR'],
        ['', 'Subtotal (Neto)', subtotal_str],
        ['', 'IVA (19%)', iva_str],
        ['', 'TOTAL', total_str],
    ]
    
    precios_table = Table(precios_data, colWidths=[4*cm, 8*cm, 4*cm])
    precios_table.setStyle(TableStyle([
        # Encabezado
        ('BACKGROUND', (1, 0), (-1, 0), colors.HexColor('#34495E')),
        ('TEXTCOLOR', (1, 0), (-1, 0), colors.whitesmoke),
        ('FONTNAME', (1, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (1, 0), (-1, 0), 11),
        ('ALIGN', (1, 0), (-1, 0), 'CENTER'),
        
        # Contenido
        ('FONTSIZE', (1, 1), (-1, -1), 10),
        ('ALIGN', (2, 1), (2, -1), 'RIGHT'),
        ('FONTNAME', (1, 1), (1, -1), 'Helvetica'),
        
        # Fila total
        ('BACKGROUND', (1, -1), (-1, -1), colors.HexColor('#ECF0F1')),
        ('FONTNAME', (1, -1), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (1, -1), (-1, -1), 12),
        ('TEXTCOLOR', (1, -1), (-1, -1), colors.HexColor('#E74C3C')),
        
        # Bordes
        ('GRID', (1, 0), (-1, -1), 1, colors.HexColor('#BDC3C7')),
        ('TOPPADDING', (1, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (1, 0), (-1, -1), 8),
    ]))
    elements.append(precios_table)
    elements.append(Spacer(1, 1*cm))
    
    # ===== NOTA IMPORTANTE =====
    nota_style = ParagraphStyle(
        'Nota',
        parent=styles['Normal'],
        fontSize=9,
        textColor=colors.HexColor('#7F8C8D'),
        leftIndent=1*cm,
        rightIndent=1*cm,
        spaceBefore=10,
        spaceAfter=10,
        borderColor=colors.HexColor('#E74C3C'),
        borderWidth=1,
        borderPadding=10,
        backColor=colors.HexColor('#FEF5E7')
    )
    
    nota_texto = """
    <b>NOTA IMPORTANTE:</b> Esta cotización es de carácter REFERENCIAL y está sujeta a evaluación 
    en terreno por parte de nuestro equipo técnico. El precio final puede variar según las 
    condiciones del espacio, materiales seleccionados y complejidad de la instalación. 
    Validez de la cotización: 30 días.
    """
    # ===== PIE DE PÁGINA =====
    elements.append(Spacer(1, 1.5*cm))
    footer_text = """
    <para align=center>
    <font size=8 color="#95A5A6">
    Muebles Barguay - Diseño y fabricación de muebles a medida<br/>
    www.mueblesbarguay.cl | contacto@mueblesbarguay.cl<br/>
    © 2025 Todos los derechos reservados
    </font>
    </para>
    """
    elements.append(Paragraph(footer_text, normal_style))
    
    # Generar el PDF
    doc.build(elements)
    buffer.seek(0)
    
    return buffer
