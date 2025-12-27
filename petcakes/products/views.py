from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from .models import Order

def confirm_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return redirect(order.whatsapp_url())
