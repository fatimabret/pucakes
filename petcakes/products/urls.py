from django.urls import path
#   from products.views.catalog_views import product_catalog
from products.views.order_views import confirm_order
from products.views.home_views import home

urlpatterns = [
    path('', home, name='home'),
#    path('', product_catalog, name='product_catalog'),
    path('confirm-order/', confirm_order, name='confirm_order'),
]
