import base64
from io import BytesIO
import uuid
import qrcode
from weasyprint import HTML, CSS
from jinja2 import Environment, FileSystemLoader
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
STATIC_DIR = os.path.join(BASE_DIR, "static")

env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))


def generate_certificate(user, event, certificate):
    code = certificate["hash"]
    validation_url = f"https://localhost:8085/certificados/validar/{code}"

    qr_base64 = _generate_qrcode(validation_url)

    template = env.get_template("certificate.html")
    html_content = template.render(
        user=user,
        event=event,
        code=code,
        qr_code=qr_base64,
        validation_url=validation_url
    )

    pdf_path = os.path.join("/tmp", f"certificado_{code}.pdf")
    css_path = os.path.join(STATIC_DIR, "base.css")

    HTML(string=html_content).write_pdf(
        pdf_path, stylesheets=[CSS(filename=css_path)]
    )

    return pdf_path


def _generate_qrcode(validation_url):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=5,
        border=2,
    )
    qr.add_data(validation_url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    buffer = BytesIO()
    img.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode("utf-8")
