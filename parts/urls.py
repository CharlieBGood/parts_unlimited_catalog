from django.urls import path
from parts.views import PartsViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'', PartsViewSet, basename='parts')

urlpatterns = router.urls


