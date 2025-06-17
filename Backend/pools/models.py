from bson import ObjectId
from django.db import models
from django_mongodb_backend.fields import ObjectIdAutoField

from users.models import AppUser


class GiftPool(models.Model):
    id = models.CharField(primary_key=True, default=lambda: str(ObjectId()), editable=False, max_length=50)
    owner = models.ForeignKey(AppUser, on_delete=models.CASCADE, related_name='owned_pools')
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    occasion = models.CharField(max_length=100)
    target_amount = models.DecimalField(max_digits=10, decimal_places=2)
    current_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def is_accessible_by(self, user):
        """Check if a user can access this pool (owner or invited)"""
        if self.owner == user:
            return True
        return self.invitations.filter(invited_user=user, accepted=True).exists()

    def get_invited_users(self):
        """Get all users who have accepted invitations to this pool"""
        return AppUser.objects.filter(
            pool_invitations__pool=self,
            pool_invitations__accepted=True
        )


class PoolInvitation(models.Model):
    id = ObjectIdAutoField(primary_key=True)
    pool = models.ForeignKey(GiftPool, on_delete=models.CASCADE, related_name='invitations')
    invited_user = models.ForeignKey(AppUser, on_delete=models.CASCADE, related_name='pool_invitations')
    invited_by = models.ForeignKey(AppUser, on_delete=models.CASCADE, related_name='sent_invitations')
    accepted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    accepted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ['pool', 'invited_user']

    def __str__(self):
        return f"Invitation to {self.pool.title} for {self.invited_user.username}"


class Donation(models.Model):
    id = ObjectIdAutoField(primary_key=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    donor = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    pool = models.ForeignKey(GiftPool, on_delete=models.CASCADE, related_name='donations')
    donated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.donor.email} - {self.amount} to {self.pool.title}"
