from rest_framework import routers
from WebPagesDownload import api_views

router = routers.DefaultRouter()

router.register(r'download', api_views.DownloadViewSet)
router.register(r'images',api_views.ImagesViewSet)
router.register(r'texts',api_views.TextsViewSet)
