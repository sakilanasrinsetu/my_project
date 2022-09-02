from dashboard.models import ProductOrder



def generate_order_no(company_id:int, order_qs: ProductOrder = None):
    DIGITS_FOR_ORDER = 6
    last_order_no = str(0).zfill(DIGITS_FOR_ORDER)
    if order_qs:
        last_order_qs = ProductOrder.objects.all().exclude(pk=order_qs.pk).order_by('-created_at').first()
    else:
        last_order_qs = ProductOrder.objects.filterall().order_by('-created_at').first()

    if not last_order_qs == None:
        if last_order_qs.order_no:
            last_order_no = last_order_qs.order_no

    try:
        order_no = str(int(last_order_no)+1).zfill(DIGITS_FOR_ORDER)
    except:
        order_no = str(0).zfill(DIGITS_FOR_ORDER)
    return order_no

