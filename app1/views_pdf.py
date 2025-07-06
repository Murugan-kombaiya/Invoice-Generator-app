from django.http import HttpResponse
from django.template.loader import get_template
from django.shortcuts import get_object_or_404
from xhtml2pdf import pisa

from .models import Invoice, InvoiceItem

def download_invoice_pdf(request, invoice_id):  # Match with urls.py
    invoice = get_object_or_404(Invoice, pk=invoice_id)
    items = InvoiceItem.objects.filter(invoice=invoice)
    
    template = get_template("invoice_app/invoice_pdf.html")
    html = template.render({
        "invoice": invoice,
        "items": items,
    })

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="invoice_{invoice.id}.pdf"'

    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse("Error generating PDF", status=500)

    return response
