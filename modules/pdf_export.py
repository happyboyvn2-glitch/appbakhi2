"""PDF invoice generation for SmartBill"""
import io
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def generate_pdf(items, subtotal, disc_amt, vat_amt, total, split_n=1, order_id=None, created_at=None):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=20*mm, leftMargin=20*mm, topMargin=15*mm, bottomMargin=15*mm)
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle("TitleVN", parent=styles["Heading1"], fontSize=18, alignment=1, spaceAfter=6, textColor=colors.HexColor("#E85D04"))
    sub_style = ParagraphStyle("SubVN", parent=styles["Normal"], fontSize=10, alignment=1, textColor=colors.HexColor("#555555"))
    normal = ParagraphStyle("NormalVN", parent=styles["Normal"], fontSize=10, leading=14)
    elements = []

    elements.append(Paragraph("SMARTBILL — HÓA ĐƠN", title_style))
    elements.append(Paragraph("Mini App Fintech • Nhóm Bá Khí", sub_style))
    elements.append(Spacer(1, 4*mm))
    elements.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#E85D04")))
    elements.append(Spacer(1, 4*mm))

    info_text = f"<b>Mã đơn:</b> #{order_id or 'DEMO'} &nbsp;&nbsp;|&nbsp;&nbsp; <b>Thời gian:</b> {created_at or datetime.now().strftime('%H:%M:%S %d/%m/%Y')}"
    elements.append(Paragraph(info_text, normal))
    elements.append(Spacer(1, 5*mm))

    data = [["STT", "Tên món", "Đơn giá", "SL", "Thành tiền"]]
    for i, it in enumerate(items, 1):
        data.append([
            str(i),
            it.get("Tên món", ""),
            f"{it.get('Đơn giá', 0):,.0f}".replace(",", "."),
            str(it.get("Số lượng", 0)),
            f"{it.get('Thành tiền', 0):,.0f}".replace(",", ".")
        ])
    data.append(["", "", "", "Tạm tính", f"{subtotal:,.0f}".replace(",", ".")])
    data.append(["", "", "", "Chiết khấu", f"-{disc_amt:,.0f}".replace(",", ".")])
    data.append(["", "", "", "VAT", f"+{vat_amt:,.0f}".replace(",", ".")])
    data.append(["", "", "", "TỔNG CỘNG", f"{total:,.0f}".replace(",", ".")])

    col_widths = [12*mm, 70*mm, 30*mm, 15*mm, 35*mm]
    table = Table(data, colWidths=col_widths)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E85D04")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTSIZE", (0, 0), (-1, 0), 10),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("ALIGN", (0, 0), (-1, 0), "CENTER"),
        ("FONTSIZE", (0, 1), (-1, -1), 9),
        ("ALIGN", (0, 1), (0, -1), "CENTER"),
        ("ALIGN", (2, 1), (-1, -1), "RIGHT"),
        ("GRID", (0, 0), (-1, -5), 0.4, colors.HexColor("#CCCCCC")),
        ("BACKGROUND", (0, -4), (-1, -1), colors.HexColor("#FFF5F0")),
        ("FONTNAME", (3, -1), (-1, -1), "Helvetica-Bold"),
        ("TEXTCOLOR", (3, -1), (-1, -1), colors.HexColor("#E85D04")),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    elements.append(table)
    elements.append(Spacer(1, 6*mm))

    if split_n > 1:
        per = total / split_n
        elements.append(Paragraph(f"<b>Chia {split_n} người → mỗi người: {per:,.0f} ₫</b>".replace(",", "."), normal))
        elements.append(Spacer(1, 3*mm))

    elements.append(HRFlowable(width="100%", thickness=0.8, color=colors.HexColor("#CCCCCC")))
    elements.append(Spacer(1, 3*mm))
    elements.append(Paragraph("Cảm ơn quý khách! — SmartBill by Bá Khí Team", sub_style))
    elements.append(Paragraph("Hóa đơn mang tính minh họa • Không có giá trị pháp lý", sub_style))

    doc.build(elements)
    buffer.seek(0)
    return buffer
