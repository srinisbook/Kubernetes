from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
import xhtml2pdf.pisa as pisa
import datetime


class Render:

    @staticmethod
    def render(path: str, params: dict):
        template = get_template(path)
        html = template.render(params)
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = "inline; filename=Kubernetes.pdf"
        pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), response)
        
        if not pdf.err:
            return response
        else:
            return HttpResponse("Error Rendering PDF", status=400)
