from django.urls import path
from .views import CreateGiftPoolView, ListGiftPoolsView, DonateToGiftPoolView, ListDonationsView, DonationHistoryView

urlpatterns = [
    path('create/', CreateGiftPoolView.as_view(), name='create_gift_pool'),
    path('all/', ListGiftPoolsView.as_view(), name='list_gift_pools'),
    path('<str:pool_id>/donate/', DonateToGiftPoolView.as_view(), name='donate-to-pool'),
    path("donations/<str:pool_id>/", DonationHistoryView.as_view(), name="donation-history"),


]
