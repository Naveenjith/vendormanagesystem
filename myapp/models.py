
from django.db import models
from django.db.models import Avg, ExpressionWrapper, F, DurationField
from django.db.models.signals import post_save
from django.dispatch import receiver

class Vendor(models.Model):
    name = models.CharField(max_length=255)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(max_length=50, unique=True)
    on_time_delivery_rate = models.FloatField(default=0)
    quality_rating_avg = models.FloatField(default=0)
    average_response_time = models.FloatField(default=0)
    fulfillment_rate = models.FloatField(default=0)

    def __str__(self):
        return self.name
    
    def calculate_performance_metrics(self):
        completed_orders = PurchaseOrder.objects.filter(vendor=self, status='completed')
        total_orders = PurchaseOrder.objects.filter(vendor=self)

        on_time_delivery_count = completed_orders.filter(delivery_date__lte=F('order_date')).count()
        self.on_time_delivery_rate = (on_time_delivery_count / completed_orders.count()) * 100 if completed_orders.count() > 0 else 0

        self.quality_rating_avg = completed_orders.aggregate(Avg('quality_rating'))['quality_rating__avg'] or 0

        response_times = completed_orders.exclude(acknowledgment_date__isnull=True).annotate(
            response_time=ExpressionWrapper(F('acknowledgment_date') - F('issue_date'), output_field=DurationField())
        )
        self.average_response_time = response_times.aggregate(Avg('response_time'))['response_time__avg'].total_seconds() if response_times else 0

        self.fulfillment_rate = (completed_orders.filter(status='completed').count() / total_orders.count()) * 100 if total_orders.count() > 0 else 0

        self.save()


class PurchaseOrder(models.Model):
    po_number = models.CharField(max_length=50, unique=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='purchase')
    order_date = models.DateTimeField()
    delivery_date = models.DateTimeField()
    items = models.JSONField()
    quantity = models.IntegerField()
    status = models.CharField(max_length=50)
    quality_rating = models.FloatField(null=True, blank=True)
    issue_date = models.DateTimeField(null=True, blank=True)
    acknowledgment_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"PO#{self.po_number} - {self.vendor.name}"

class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='historical_performances')
    date = models.DateTimeField()
    on_time_delivery_rate = models.FloatField()
    quality_rating_avg = models.FloatField()
    average_response_time = models.FloatField()
    fulfillment_rate = models.FloatField()

    def __str__(self):
        return f"{self.vendor} - {self.date}"

#--------------------------------------------------------------------------------------#


@receiver(post_save, sender=PurchaseOrder)
def update_vendor_performance(sender, instance, **kwargs):
    if kwargs.get('created'):
        instance.vendor.calculate_performance_metrics()