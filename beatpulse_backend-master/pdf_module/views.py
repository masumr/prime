from io import BytesIO

from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from pdfdocument.utils import pdf_response
from rest_framework.decorators import api_view
from xhtml2pdf import pisa

from models.models import OrderItem, Profile, Order, ProducerPayout


def _generate_pdf_from_html(html, filename: str):
    buffer = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("utf-8")), buffer)
    if not pdf.err:
        return HttpResponse(buffer.getvalue(), content_type='application/pdf')
        # return FileResponse(buffer, as_attachment=True, filename=filename)
    else:
        return HttpResponse('an error occcured while generating the pdf')


@api_view(['GET'])
def generate_contract_pdf(request: HttpRequest, order_item_id: int, filename: str):
    user: Profile = request.user
    order_item = get_object_or_404(OrderItem, pk=order_item_id,
                                   order__status=Order.STATUS_COMPLETE,
                                   order__profile=user)
    beat = order_item.beat
    bought_license = order_item.license
    html = order_item.license.contract_html
    
    file_types = 'MP3'
    if bought_license.has_wav:
        file_types += ', WAV'
    if bought_license.has_trackout:
        file_types += ' and Trackout'
    
    # replace of variables with real values
    order_date = order_item.order.date.strftime('%m/%d/%Y')
    html = html.replace('%ORDER_DATE%', order_date) \
        .replace('%CLIENT_NAME%', user.first_name) \
        .replace('%PRODUCER_NAMES%', ', '.join([x.display_name for x in beat.producers.all()])) \
        .replace('%BEAT_NAME%', beat.name) \
        .replace('%LICENSE_NAME%', bought_license.name) \
        .replace('%FILE_TYPES%', file_types) \
        .replace('%BEAT_PRICE%', f"{bought_license.price_discounted:.2f}") \
        .replace('%BEAT_ID%', str(beat.id)) \
        .replace('%PRODUCER_FULLNAMES%', ', '.join([x.profile.first_name for x in beat.producers.all()])) \
        # .replace('\n', '<br/>') \
        # .replace('<br>', '<br/>')  # license should contain an open br tag
    
    return _generate_pdf_from_html(html, filename=filename)
    # if filename.endswith('.pdf'):
    #     filename = filename[:-4]
    # pdf, response = pdf_response(filename)
    # pdf.init_report()
    # pdf.p_markup(html)
    # pdf.generate()
    # return response


# @api_view(['GET'])
def generate_producer_payout_pdf(request: HttpRequest, producer_payout_id: int):
    # user: Profile = request.user
    producer_payout: ProducerPayout = get_object_or_404(ProducerPayout, pk=producer_payout_id)
    
    # if not (producer_payout.producer == user.producer or user.is_admin()):
    #    return HttpResponseBadRequest("You don't have permission to view this file")
    
    # render the html to replace the dynamic data
    template_data = {'payout': producer_payout}
    html = render_to_string('producer_payout.html', template_data)
    return _generate_pdf_from_html(html, filename=f'producer_payout_{producer_payout_id}.pdf')
