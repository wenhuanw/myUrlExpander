from .models import ExpandedUrl
from .forms import ExpandedUrlForm
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
import lxml
from lxml.html import fromstring
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
import requests
from .myservice import get_url
from django.utils import timezone
import pdb
# Create your views here.

@login_required(login_url='')
def url_list(request):
    expandedUrls = ExpandedUrl.objects.all()
    return render(request, 'myurlex/url_list.html', {'expandedurls': expandedUrls})

@login_required(login_url='')
def url_detail(request, pk):
    url = get_object_or_404(ExpandedUrl, pk=pk)
    return render(request, 'myurlex/url_detail.html', {'expandedurl': url})

    if request.method == "POST":
        form=ExpandedUrlForm(request.POST)
        if form.is_valid():
            url = form.save(commit=False)
            res = requests.get(url.origin)
            if (url.timestamp is None):
                url.timestamp = timezone.now()
                url.waybackUrl = get_url(url.origin, url.timestamp)
            else:
                url.waybackUrl = get_url(url.origin, url.timestamp)
            url.status = res.status_code
            url.destination = res.url
            siteTree = fromstring(res.content)
            url.title = siteTree.findtext('.//title')
            url.save()
            return redirect('myurlex.views.url_detail', pk=url.pk)
    else:
        form = ExpandedUrlForm()
        return render(request, 'myurlex/url_form.html', {'form': form})

@login_required(login_url='')
def url_create(request):
   # pdb.set_trace()
    if request.method == "POST":
        form=ExpandedUrlForm(request.POST)
        if form.is_valid():
            url = form.save(commit=False)
            res = requests.get(url.origin)
            if (url.timestamp == ''):
                url.timestamp = timezone.now()
                url.waybackUrl = get_url(url.origin, url.timestamp)
            else:
                url.waybackUrl = get_url(url.origin, url.timestamp)
                if (url.waybackUrl is None):
                     return redirect('myurlex.views.url_create')
            url.status = res.status_code
            url.destination = res.url
            siteTree = fromstring(res.content)
            url.title = siteTree.findtext('.//title')
            url.save()
            return redirect('myurlex.views.url_detail', pk=url.pk)
    else:
        form = ExpandedUrlForm()
        return render(request, 'myurlex/url_form.html', {'form': form})

@login_required(login_url='')
def url_edit(request, pk):
    url = get_object_or_404(ExpandedUrl, pk=pk)
    if request.method == "POST":
        form=ExpandedUrlForm(request.POST, instance=url)
        if form.is_valid():
            url = form.save(commit=False)
            res = requests.get(url.origin)
            if (url.timestamp == ''):
                url.timestamp = timezone.now()
                url.waybackUrl = get_url(url.origin, url.timestamp)
            else:
                url.waybackUrl = get_url(url.origin, url.timestamp)
            url.status = res.status_code
            url.destination = res.url
            siteTree = fromstring(res.content)
            url.title = siteTree.findtext('.//title')
            url.save()
            return redirect('myurlex.views.url_detail', pk=url.pk)
    else:
        form = ExpandedUrlForm(instance=url)
        return render(request, 'myurlex/url_form.html', {'form': form})

@login_required(login_url='')
def url_delete(request, pk):
  url = get_object_or_404(ExpandedUrl, pk=pk)
  url.delete()
  return url_list(request)
