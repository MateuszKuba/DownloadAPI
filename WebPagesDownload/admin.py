from django.contrib import admin

# Register your models here.
from WebPagesDownload.models import *

admin.site.register(Download)
admin.site.register(WebText)
admin.site.register(WebImage)