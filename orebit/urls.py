from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from app.views import AsteroideViewSet, NaveViewSet, MineracaoViewSet
from app import views 

app = DefaultRouter()
app.register(r'asteroides', AsteroideViewSet)
app.register(r'naves', NaveViewSet)
app.register(r'mineracoes', MineracaoViewSet)
app.register(r'historico', views.HistoricoViewSet, basename='historico') 
app.register(r'alvosradar', views.AlvoRadarViewSet, basename='alvosradar') 
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(app.urls)),
]