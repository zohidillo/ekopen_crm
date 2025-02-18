import os
from weasyprint import HTML
from django.conf import settings
from django.templatetags.static import static
from django.template.loader import get_template
from xhtml2pdf.tags import pisaTag


def generate_pdf(order, request):
    template = get_template('docs/waybill.html')
    order_items = order.items.select_related('product__product__category')

    category_totals = {}
    for item in order_items:
        category_name = item.product.product.category.name
        sale_sum = item.sale_sum
        if not category_totals.get(category_name):
            category_totals[category_name] = sale_sum
        else:
            category_totals[category_name] += sale_sum
    logo_url = request.build_absolute_uri(static('images/logo.jpg'))

    context = {
        'order': order,
        "logo_url": logo_url,
        'customer': order.customer,
        "category_totals": category_totals,
        'total_sum': f"{order.total_sum:,.2f}" if order.total_sum else 0,
        'paid_amount': f"{order.paid_amount:,.2f}" if order.paid_amount else 0,
        'order_items': order.items.all().order_by('category'),
        'remaining_debt': f"{order.remaining_balance:,.2f}" if order.remaining_balance else 0,
        "total_debt": f"{order.customer.debts.all().first().total_debt:,.2f}",
    }

    html = template.render(context)
    directory = os.path.join(settings.MEDIA_ROOT, 'docs')
    waybill_number = order.waybill_number or f'{order.id}'
    pdf_file_name = f'waybill_{waybill_number}.pdf'
    pdf_file_path = os.path.join(directory, pdf_file_name)
    os.makedirs(directory, exist_ok=True)

    HTML(string=html).write_pdf(pdf_file_path)

    relative_pdf_path = os.path.join('docs', pdf_file_name)
    full_url = os.path.join(settings.MEDIA_URL, relative_pdf_path)

    return full_url
