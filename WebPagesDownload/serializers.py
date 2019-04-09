from WebPagesDownload.models import Download, WebImage, WebText
from rest_framework import serializers
import base64
from django.core.files import File


class WebImageSerializer(serializers.ModelSerializer):
    data = serializers.SerializerMethodField()

    class Meta:
        model = WebImage
        fields = ('id','data','download')

    def get_data(self, obj):
        f = open(obj.data.path, 'rb')
        image = File(f)
        data = base64.b64encode(image.read())
        f.close()
        return data


class WebTextSerializer(serializers.ModelSerializer):
    data = serializers.SerializerMethodField()

    class Meta:
        model = WebText
        fields = ('id','data','download')

    def get_data(self, obj):
        f = open(obj.data.path, 'r')
        text = File(f)
        data = text.read()
        f.close()
        return data


class DownloadSerializer(serializers.ModelSerializer):
    webimage = serializers.HyperlinkedRelatedField(many=True, read_only=True)
    webtext = serializers.HyperlinkedRelatedField(many=True,  read_only=True)

    class Meta:
        model = Download
        fields = ('id','url', 'webimage', 'webtext')
