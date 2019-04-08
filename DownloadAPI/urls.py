from django.contrib import admin
from django.urls import include, path
from .api import router

urlpatterns = [
    path('', include('WebPagesDownload.urls')),
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls) )
]