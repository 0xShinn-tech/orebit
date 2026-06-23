from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from app.views import AsteroideViewSet, NaveViewSet, MineracaoViewSet
from app import views 

router = DefaultRouter()
router.register(r'asteroides', AsteroideViewSet)
router.register(r'naves', NaveViewSet)
router.register(r'mineracoes', MineracaoViewSet)
router.register(r'historico', views.HistoricoViewSet, basename='historico') 
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]