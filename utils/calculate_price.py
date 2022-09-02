import decimal
from dashboard.models import *
import dashboard
from django.utils import timezone
from datetime import date, datetime, timedelta
import datetime
from django.utils import timezone
from datetime import datetime


def calculate_price(product_order_obj, include_initial_order=False, **kwargs):
    company_qs = Company.objects.all().last()
    total_price = 0.0
    grand_total_price = 0.0
    hundred = 100.00
    discount_amount_without_promo_code = 0.0
    discount_amount_with_promo_code = 0.0
    discount_amount = 0.0
    packaging_price = 0.0
    delivery_charge = 0.0

    today = timezone.now()
    current_time = datetime.now().time()

    if include_initial_order:
        ordered_items_qs = product_order_obj.ordered_items.exclude(
            status__in=["3_CANCELLED"])
    else:
        ordered_items_qs = product_order_obj.ordered_items.exclude(
            status__in=["3_CANCELLED"])

    for ordered_item in ordered_items_qs:
        discount_qs = ordered_item.product_option.product.discount
        item_price = ordered_item.quantity * ordered_item.product_option.product.price
        total_price += item_price

        if discount_qs:
            if discount_qs.schedule_type =='Time_Wise':
                valid_discount_qs = Discount.objects.filter(pk = discount_qs.id, start_time__lte=current_time,
                                                            closing_time__gte=current_time).last()
            else:
                valid_discount_qs = Discount.objects.filter(pk=discount_qs.id,start_date__lte=today,
                                                            end_date__gte=today).last()
            if valid_discount_qs:
                if valid_discount_qs.discount_type == 'PERCENTAGE':
                    discount_amount_without_promo_code += (ordered_item.product_option.product.discount.amount/hundred)*item_price
                else:
                    discount_amount_without_promo_code += ordered_item.product_option.product.discount.amount

        elif product_order_obj.applied_promo_code:
            promo_code = product_order_obj.applied_promo_code
            promo_code_qs = PromoCode.objects.filter(code = promo_code).last()
            if promo_code_qs:
                if promo_code_qs.promo_type== 'PERCENTAGE':
                    discount_amount_with_promo_code += (promo_code_qs.amount/hundred)*item_price
                else:
                    discount_amount_with_promo_code += promo_code_qs.amount

    discount_amount = discount_amount_without_promo_code+discount_amount_with_promo_code
    # total price save in database
    packaging_price += company_qs.packaging_charge
    if product_order_obj.location == 'INSIDE_DHAKA':
        delivery_charge = company_qs.delivery_charge_inside_dhaka
    else:
        delivery_charge = company_qs.delivery_charge_outside_dhaka

    # packaging_price = company_qs.packaging_charge

    grand_total_price = total_price - discount_amount
    payable_amount = grand_total_price + packaging_price + delivery_charge

    product_order_obj.grand_total = grand_total_price
    product_order_obj.discount_amount = discount_amount
    product_order_obj.payable_amount = payable_amount
    product_order_obj.save()

    grand_total_price = grand_total_price
    discount_amount = discount_amount
    payable_amount = payable_amount


    response_dict = {
        "product_total_price": round(total_price, 2),
        'discount_amount': round(discount_amount, 2),
        "grand_total_price": round(grand_total_price, 2),
        'packaging_price': round(packaging_price, 2),
        'delivery_charge': round(delivery_charge, 2),
        'payable_amount': round(payable_amount, 2)
    }

    return response_dict


