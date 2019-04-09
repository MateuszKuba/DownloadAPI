from django.http import HttpResponse


def index(request):
    return HttpResponse("Hey !! Have fun with the api. Check /api/v1/")