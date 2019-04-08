from rest_framework import viewsets
from rest_framework.views import Response, status, APIView
from . import models
from . import serializers
import logging
from WebPagesDownload.tasks import download_text, download_images
from django.http import Http404
from django_celery_results.models import TaskResult
logger = logging.getLogger(__name__)
from django.db import transaction

class DownloadViewSet(viewsets.ModelViewSet):
    queryset = models.Download.objects.all()
    serializer_class = serializers.DownloadSerializer

    def get_queryset(self):
        query_set = self.queryset
        url = self.request.query_params.get('url',None)
        if url is not None:
            query_set = query_set.filter(download__url=url)
        return query_set

    def create(self,  request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        url = request.data['url']
        with transaction.atomic():
            download = self.perform_create(serializer)
        text_task_id = download_text.delay(url, download)
        image_task_id = download_images.delay(url, download)

        # print(type(text_task_id))
        #
        response = {
            'status': 'accepted',
            'data': {
                "image": {
                    "task_id": image_task_id.id
                },
                "text": {
                    "task_id": text_task_id.id
                }
            }
        }

        headers = self.get_success_headers(serializer.data)
        return Response(response, status=status.HTTP_202_ACCEPTED, headers=headers)


class ImagesViewSet(viewsets.ModelViewSet):
    queryset = models.WebImage.objects.all()
    serializer_class = serializers.WebImageSerializer


class TextsViewSet(viewsets.ModelViewSet):
    queryset = models.WebText.objects.all()
    serializer_class = serializers.WebTextSerializer


class StatusDetail(APIView):
    def get(self,request, pk):
        try:
            detail =  TaskResult.objects.get_task(task_id=pk)
            return Response(detail.result)
        except Exception:
            raise Http404
