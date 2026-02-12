from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor
from pypdf import PdfReader, PdfWriter
import qrcode

from utils_ar import ar
from config import FONT_PATH, TEXT_COLOR, PDF_TEMPLATE, TEXT_BOLD_STEPS, TEXT_BOLD_OFFSET, QR_X, QR_Y, QR_SIZE

pdfmetrics.registerFont(TTFont("arabic", FONT_PATH))

COLOR = HexColor(TEXT_COLOR)

POSITIONS = {
    "leave_id": (260, 640),
    "name": (260, 490),
    "national_id": (260, 460),
}


def build_pdf(template, data):

    c = canvas.Canvas("overlay.pdf")
    c.setFont("arabic", 12)
    c.setFillColor(COLOR)

    for k, v in data.items():
        if k not in POSITIONS:
            continue

        x, y = POSITIONS[k]
        t = ar(str(v))

        for i in range(TEXT_BOLD_STEPS):
            c.drawString(x + i * TEXT_BOLD_OFFSET, y, t)

    qr = qrcode.make(data["leave_id"])
    qr.save("qr.png")
    c.drawImage("qr.png", QR_X, QR_Y, QR_SIZE, QR_SIZE)

    c.save()

    base = PdfReader(template)
    over = PdfReader("overlay.pdf")

    page = base.pages[0]
    page.merge_page(over.pages[0])

    w = PdfWriter()
    w.add_page(page)

    with open("result.pdf", "wb") as f:
        w.write(f)

    return "result.pdf"
