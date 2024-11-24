from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from portfolio_app import views 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='home'),
    path('upload/', views.upload_project, name='upload_project'),
    path('graph/', views.display_graph, name='display_graph'),
    path('portfolio/', include('portfolio_app.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
