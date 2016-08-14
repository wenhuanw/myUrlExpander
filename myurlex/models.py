from django.db import models
import lxml
from lxml.html import fromstring
import requests
from .myservice import get_url

# Create your models here.
class ExpandedUrl(models.Model):
    destination = models.URLField(default='')
    origin = models.URLField(default='http://')
    status = models.IntegerField(default=0)
    title = models.CharField(max_length=150)
    waybackUrl = models.URLField(default='')
    timestamp = models.CharField(max_length=50,default='')

    def publish(self):
        if str(self.origin).startswith('http://'):
            response = requests.get(self.origin)
        else:
            response = requests.get('http://' + self.origin)
        self.destination = response.url
        self.status = response.status
        siteTree = fromstring(response.content)
        self.title = siteTree.findtext('.//title')
        self.save()

    def __str__(self):
        return self.title
