from bson import ObjectId
from django.db import models


class GiftPool(models.Model):
    id = models.CharField(primary_key=True, default=lambda: str(ObjectId()), editable=False, max_length=50)

    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    occasion = models.CharField(max_length=100)
    target_amount = models.DecimalField(max_digits=10, decimal_places=2)
    current_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
