from django.db import models
from users.models import AppUser

class GiftPool(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    occasion = models.CharField(max_length=100)
    target_amount = models.DecimalField(max_digits=10, decimal_places=2)
    current_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    #organizer = models.ForeignKey(AppUser, on_delete=models.CASCADE, related_name="organized_pools")
    #invited_users = models.ManyToManyField(AppUser, related_name="invited_pools")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
