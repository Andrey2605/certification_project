from rest_framework.routers import DefaultRouter

from market.apps import MarketConfig
from market.views import ConsumerViewSet, ProductViewSet, SupplierViewSet

app_name = MarketConfig.name

router = DefaultRouter()

router.register(r"product", ProductViewSet, basename="product")
router.register(r"supplier", SupplierViewSet, basename="supplier")
router.register(r"consumer", ConsumerViewSet, basename="consumer")

urlpatterns = [] + router.urls
