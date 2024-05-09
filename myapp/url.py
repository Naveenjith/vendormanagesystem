from django.urls import path
from . import views

urlpatterns = [
    path('vendors/', views.vendors_list),
    path('vendors/<int:vendor_id>/', views.vendor_detail),
    path('purchase/', views.purchase_orders_list),
    path('purchase/<int:po_id>/', views.purchase_order_detail),
    path('vendors/<int:vendor_id>/performance/', views.vendor_performance)
]
