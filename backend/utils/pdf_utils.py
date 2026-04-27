import base64
from datetime import datetime
from io import BytesIO

# Lazy imports for reportlab - these are only needed when generating PDFs
_reportlab_loaded = False
colors = None
A4 = None
cm = None
ImageReader = None
canvas = None


def _load_reportlab():
    global _reportlab_loaded, colors, A4, cm, ImageReader, canvas
    if _reportlab_loaded:
        return
    
    try:
        from reportlab.lib import colors as _colors
        from reportlab.lib.pagesizes import A4 as _A4
        from reportlab.lib.units import cm as _cm
        from reportlab.lib.utils import ImageReader as _ImageReader
        from reportlab.pdfgen import canvas as _canvas
        
        colors = _colors
        A4 = _A4
        cm = _cm
        ImageReader = _ImageReader
        canvas = _canvas
        _reportlab_loaded = True
    except ImportError as e:
        raise ImportError(f"ReportLab is required for PDF generation: {e}")


def _image_from_base64(data):
    _load_reportlab()
    return ImageReader(BytesIO(base64.b64decode(data)))


def build_report_pdf(record):
    _load_reportlab()
    pdf_bytes = BytesIO()
    c = canvas.Canvas(pdf_bytes, pagesize=A4)
    width, height = A4

    c.setFont("Helvetica-Bold", 16)
    c.drawString(2 * cm, height - 2 * cm, "AI-Powered Brain Tumor Detection Report")
    c.setFont("Helvetica", 10)
    c.setFillColor(colors.grey)
    c.drawString(2 * cm, height - 2.7 * cm, "Hospital/Project: Brain Tumor AI Diagnostic Suite")
    c.setFillColor(colors.black)

    patient = record.get("patient", {})
    prediction = record.get("prediction", {})
    created_at = record.get("createdAt")
    if isinstance(created_at, datetime):
        created_at = created_at.strftime("%Y-%m-%d %H:%M:%S")

    y = height - 4 * cm
    c.setFont("Helvetica-Bold", 12)
    c.drawString(2 * cm, y, "Patient Information")
    c.setFont("Helvetica", 10)
    y -= 0.8 * cm
    info_lines = [
        f"Name: {patient.get('fullName', '-')}",
        f"Age: {patient.get('age', '-')}",
        f"Gender: {patient.get('gender', '-')}",
        f"Phone: {patient.get('phone', '-')}",
        f"Email: {patient.get('email', '-')}",
        f"Address: {patient.get('address', '-')}",
        f"Symptoms: {patient.get('symptoms', '-')}",
    ]
    for line in info_lines:
        c.drawString(2 * cm, y, line)
        y -= 0.6 * cm

    c.setFont("Helvetica-Bold", 12)
    c.drawString(2 * cm, y - 0.2 * cm, "Prediction")
    c.setFont("Helvetica", 10)
    y -= 1 * cm
    c.drawString(2 * cm, y, f"Predicted Class: {prediction.get('predictedClass', '-')}")
    y -= 0.6 * cm
    c.drawString(2 * cm, y, f"Confidence: {prediction.get('confidence', 0)}%")
    y -= 0.6 * cm
    c.drawString(2 * cm, y, f"Date & Time: {created_at}")
    y -= 1 * cm
    c.drawString(
        2 * cm,
        y,
        "AI Recommendation: Refer to a specialist radiologist for final medical diagnosis.",
    )

    images = record.get("images", {})
    top = y - 1.2 * cm
    image_w = 5.5 * cm
    image_h = 5.5 * cm

    if images.get("original"):
        c.drawImage(_image_from_base64(images["original"]), 2 * cm, top - image_h, image_w, image_h)
        c.drawString(2 * cm, top - image_h - 0.4 * cm, "Original MRI")
    if images.get("heatmap"):
        c.drawImage(
            _image_from_base64(images["heatmap"]),
            8.5 * cm,
            top - image_h,
            image_w,
            image_h,
        )
        c.drawString(8.5 * cm, top - image_h - 0.4 * cm, "Grad-CAM Heatmap")
    if images.get("overlay"):
        c.drawImage(
            _image_from_base64(images["overlay"]),
            15 * cm,
            top - image_h,
            image_w,
            image_h,
        )
        c.drawString(15 * cm, top - image_h - 0.4 * cm, "Overlay")

    c.showPage()
    c.save()
    pdf_bytes.seek(0)
    return pdf_bytes
