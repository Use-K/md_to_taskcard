from weasyprint import HTML
from weasyprint.fonts import FontConfiguration

def html_to_pdf(html, pdf_out_dir, pdf_options=None):
    HTML(string=html).write_pdf(pdf_out_dir)
