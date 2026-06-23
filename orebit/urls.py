from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from app.views import AsteroideViewSet, MineracaoViewSet

router = DefaultRouter()
router.register(r'asteroides', AsteroideViewSet)
router.register(r'mineracoes', MineracaoViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]