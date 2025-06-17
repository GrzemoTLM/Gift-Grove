from django.urls import path
from .views import CreateGiftPoolView, ListGiftPoolsView

urlpatterns = [
    path('create/', CreateGiftPoolView.as_view(), name='create_gift_pool'),
    path('all/', ListGiftPoolsView.as_view(), name='list_gift_pools'),
]
