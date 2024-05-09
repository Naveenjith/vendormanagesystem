from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Vendor, PurchaseOrder
from .serializers import VendorSerializer, PurchaseOrderSerializer

@api_view(['POST', 'GET'])
def vendors_list(request):
    if request.method == 'GET':
        vendors = Vendor.objects.all()
        serializer = VendorSerializer(vendors, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = VendorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

@api_view(['GET', 'PUT', 'DELETE'])
def vendor_detail(request, vendor_id):
    try:
        vendor = Vendor.objects.get(id=vendor_id)
    except Vendor.DoesNotExist:
        return Response(status=404)

    if request.method == 'GET':
        serializer = VendorSerializer(vendor)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = VendorSerializer(vendor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        vendor.delete()
        return Response('vendor deleted')

@api_view(['GET', 'POST'])
def purchase_orders_list(request):
    if request.method == 'GET':
        vendor_id = request.query_params.get('vendor_id')
        if vendor_id:
            purchase_orders = PurchaseOrder.objects.filter(vendor_id=vendor_id)
        else:
            purchase_orders = PurchaseOrder.objects.all()
        serializer = PurchaseOrderSerializer(purchase_orders, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = PurchaseOrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

@api_view(['GET', 'PUT', 'DELETE'])
def purchase_order_detail(request, po_id):
    try:
        purchase_order = PurchaseOrder.objects.get(id=po_id)
    except PurchaseOrder.DoesNotExist:
        return Response(status=404)

    if request.method == 'GET':
        serializer = PurchaseOrderSerializer(purchase_order)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = PurchaseOrderSerializer(purchase_order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        purchase_order.delete()
        return Response('order deleted')


@api_view(['GET'])
def vendor_performance(request, vendor_id):
    try:
        vendor = Vendor.objects.get(id=vendor_id)
    except Vendor.DoesNotExist:
        return Response(status=404)

    vendor.calculate_performance_metrics()
    serializer = VendorSerializer(vendor)
    return Response(serializer.data)