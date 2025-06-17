from django.urls import path
from .views import (
    CreateGiftPoolView, ListGiftPoolsView, DonateToGiftPoolView, 
    ListDonationsView, DonationHistoryView, InviteUserToPoolView,
    AcceptPoolInvitationView, ListMyInvitationsView, EditGiftPoolView, DeleteGiftPoolView
)

urlpatterns = [
    path('create/', CreateGiftPoolView.as_view(), name='create_gift_pool'),
    path('all/', ListGiftPoolsView.as_view(), name='list_gift_pools'),
    path('<str:pool_id>/donate/', DonateToGiftPoolView.as_view(), name='donate-to-pool'),
    path("donations/<str:pool_id>/", DonationHistoryView.as_view(), name="donation-history"),
    path('<str:pool_id>/invite/', InviteUserToPoolView.as_view(), name='invite-user-to-pool'),
    path('invitations/', ListMyInvitationsView.as_view(), name='list-my-invitations'),
    path('invitations/<str:invitation_id>/accept/', AcceptPoolInvitationView.as_view(), name='accept-invitation'),
    path('<str:pool_id>/edit/', EditGiftPoolView.as_view(), name='edit-gift-pool'),
    path('<str:pool_id>/delete/', DeleteGiftPoolView.as_view(), name='delete-gift-pool'),
]
