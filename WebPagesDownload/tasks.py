from celery import shared_task
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import urllib
from urllib.parse import urlparse
from .models import WebImage, Download, WebText
from django.core.files import File
from django.core.files.base import ContentFile

url = 'https://www.onet.pl'

def images_urls(url):
    img = []
    html = urlopen(url)
    bs = BeautifulSoup(html, 'html.parser')
    images = bs.find_all('img', {'src': re.compile('([-\w]+\.(?:jpg|gif|png))')})
    for image in images:
        img.append(image['src'])
    return img

@shared_task
def download_images(url):
    urls = images_urls(url)
    res = None
    for image in urls:
        if image[0]+image[1] == "//":
            res = urllib.request.urlretrieve('http:' + image)
        elif image[0] == 'h':
            res = urllib.request.urlretrieve(image)
        else:
            parsed_uri = urlparse(url)
            result = '{uri.scheme}://{uri.netloc}'.format(uri=parsed_uri)
            res = urllib.request.urlretrieve(result + image)
        download = Download.objects.get(url=url)
        print(res)
        webimage = WebImage.objects.create(download=download)
        webimage.data.save(url.split("/")[-1],File(open(res[0], 'rb')))
        webimage.save()

    return {'status': 'success'}

@shared_task
def download_text(url):
    webpage = str(urllib.request.urlopen(url).read().decode('utf-8'))
    soup = BeautifulSoup(webpage, features="lxml")

    for script in soup(["script", "style"]):
        script.extract()

    text = soup.body.get_text()
    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)

    download = Download.objects.get(url=url)
    webtext = WebText.objects.create(download=download)
    webtext.data.save(url.split('/')[-1], ContentFile(text))
    webtext.save()

    return text

#download_images(url)

# print(download_text(url))