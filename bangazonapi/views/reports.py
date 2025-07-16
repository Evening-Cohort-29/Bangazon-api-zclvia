"""View module for handling requests about reports"""
from django.shortcuts import render
from django.contrib.humanize.templatetags.humanize import intcomma
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from bangazonapi.models import Order, OrderProduct, Product


class Reports(ViewSet):
    """View for getting reports"""

    @action(detail=False, methods=['get'], url_path='orders')
    def orders(self, request):
        """Custom URL: /reports/orders/?status=incomplete"""
        status = request.GET.get('status', 'all')
        if status == 'incomplete':
            orders = Order.objects.filter(payment_type=None)
        elif status == 'complete':
            orders = Order.objects.exclude(payment_type=None)
        else:
            orders = Order.objects.all()

        for order in orders:
            order.total = 0
            order_products = list(OrderProduct.objects.filter(
                order_id=order.id).values_list('product_id', flat=True))

            for product_id in order_products:
                product = Product.objects.get(id=product_id)
                order.total += product.price
            order.total = f"{intcomma(f'{order.total:.2f}')}"
        context = {
            'orders': orders,
            'status': status
        }
        return render(request, 'orders_report.html', context)
