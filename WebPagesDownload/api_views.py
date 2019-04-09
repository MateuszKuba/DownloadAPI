from rest_framework import viewsets
from rest_framework.views import Response, status, APIView
from . import models
from . import serializers
import logging
from WebPagesDownload.tasks import download_text, download_images
from django.http import Http404
from django_celery_results.models import TaskResult
logger = logging.getLogger(__name__)


class DownloadViewSet(viewsets.ModelViewSet):
    queryset = models.Download.objects.all()
    serializer_class = serializers.DownloadSerializer

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `url` query parameter in the URL.
        """
        queryset = models.Download.objects.all()
        url = self.request.query_params.get('url', None)
        if url is not None:
            queryset = queryset.filter(url=url)
        return queryset

    def create(self,  request, *args, **kwargs):
        '''
        POST method equivalent for creation of resources. Creates empty Download resource and delegates text
        downloading and image downloading to celery broker
        '''
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        url = request.data['url']

        self.perform_create(serializer)

        text_task_id = download_text.delay(url)
        image_task_id = download_images.delay(url)

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
    '''
    View for checking archived celery results. They are stored inside TaskResult model that is created by
    django-celery-results plugin
    '''
    def get(self,request, pk):
        try:
            detail =  TaskResult.objects.get_task(task_id=pk)
            return Response(detail.result)
        except Exception:
            raise Http404
