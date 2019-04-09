from WebPagesDownload.models import Download, WebImage, WebText
from rest_framework import serializers


class WebImageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = WebImage
        fields = ('id','data','download')


class WebTextSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = WebText
        fields = ('id','data','download')


class DownloadSerializer(serializers.ModelSerializer):
    webimage = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    webtext = serializers.PrimaryKeyRelatedField(many=True,  read_only=True)

    class Meta:
        model = Download
        fields = ('id','url', 'webimage', 'webtext')
