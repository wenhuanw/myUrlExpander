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
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from myurlex.serializers import UrlSerializer
from .myservice import get_url,upload_image,delete_image,get_id
from django.utils import timezone
import pdb
from ratelimit.decorators import ratelimit
# Create your views here.

@ratelimit(key='ip', rate='10/m', block=True)
@login_required(login_url='')
def url_list(request):
    expandedUrls = ExpandedUrl.objects.all()
    return render(request, 'myurlex/url_list.html', {'expandedurls': expandedUrls})

@ratelimit(key='ip', rate='10/m', block=True)
@api_view(['GET'])
@login_required(login_url='')
def url_list_api(request):
    if request.method == "GET":
        expandedUrls = ExpandedUrl.objects.all()
        serializer = UrlSerializer(expandedUrls, many = True)
        return Response(serializer.data)


@ratelimit(key='ip', rate='10/m', block=True)
@login_required(login_url='')
def url_detail(request, pk):
    url = get_object_or_404(ExpandedUrl, pk=pk)
    return render(request, 'myurlex/url_detail.html', {'expandedurl': url})
    
   # if request.method == "POST":
    #    form=ExpandedUrlForm(request.POST)
     #   if form.is_valid():
      #      url = form.save(commit=False)
       #     res = requests.get(url.origin)
        #    if (url.timestamp is None):
         #       url.timestamp = timezone.now()
          #      url.waybackUrl = get_url(url.origin, url.timestamp)
           # else:
            #    url.waybackUrl = get_url(url.origin, url.timestamp)
           # url.status = res.status_code
           # url.destination = res.url
           # siteTree = fromstring(res.content)
           # url.title = siteTree.findtext('.//title')
           # url.save()
           # return redirect('myurlex.views.url_detail', pk=url.pk)
   # else:
    #    form = ExpandedUrlForm()
     #   return render(request, 'myurlex/url_form.html', {'form': form})



@ratelimit(key='ip', rate='10/m', block=True)
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
                url.imageId = get_id(url.waybackUrl)
                url.imageUrl = 'https://s3.amazonaws.com/wwhb1/image/'+url.imageId+'.png'
                upload_image(url.waybackUrl, url.imageId)
            else:
                url.waybackUrl = get_url(url.origin, url.timestamp)
                if (url.waybackUrl is None):
                     return redirect('myurlex.views.url_create')
                url.imageId = get_id(url.waybackUrl)
                url.imageUrl = 'https://s3.amazonaws.com/wwhb1/image/'+url.imageId+'.png'
                upload_image(url.waybackUrl, url.imageId)
            url.status = res.status_code
            url.destination = res.url
            siteTree = fromstring(res.content)
            url.title = siteTree.findtext('.//title')
            url.save()
            return redirect('myurlex.views.url_detail', pk=url.pk)
    else:
        form = ExpandedUrlForm()
        return render(request, 'myurlex/url_form.html', {'form': form})

@ratelimit(key='ip', rate='10/m', block=True)
@api_view(['POST'])
@login_required(login_url='')
def url_create_api(request):
   # pdb.set_trace()
    if request.method == "POST":
        serializer = UrlSerializer(data=request.data)         
        if serializer.is_valid():             
            serializer.save()             
            return Response(serializer.data, status=status.HTTP_201_CREATED)         
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@ratelimit(key='ip', rate='10/m', block=True)
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
                if (url.imageId == 0 or url.imageId != get_id(url.waybackUrl)):
                    url.imageId = get_id(url.waybackUrl)
                    url.imageUrl = 'https://s3.amazonaws.com/wwhb1/image/'+url.imageId+'.png'
                    upload_image(url.waybackUrl, url.imageId)
            else:
                url.waybackUrl = get_url(url.origin, url.timestamp)
                if (url.waybackUrl is None):
                     return redirect('myurlex.views.url_detail',pk=url.pk)
                url.imageId = get_id(url.waybackUrl)
                url.imageUrl = 'https://s3.amazonaws.com/wwhb1/image/'+url.imageId+'.png'
                upload_image(url.waybackUrl, url.imageId)
            url.status = res.status_code
            url.destination = res.url
            siteTree = fromstring(res.content)
            url.title = siteTree.findtext('.//title')
            url.save()
            return redirect('myurlex.views.url_detail', pk=url.pk)
    else:
        form = ExpandedUrlForm(instance=url)
        return render(request, 'myurlex/url_form.html', {'form': form})


@ratelimit(key='ip', rate='10/m', block=True)
@api_view(['GET','PUT','DELETE'])
@login_required(login_url='')
def url_edit_api(request, pk, format=None):
    try:
        url = ExpandedUrl.objects.get(pk=pk)
    except url.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':         
        serializer = UrlSerializer(url)         
        return Response(serializer.data)

    elif request.method == 'PUT':         
        serializer = UrlSerializer(user, data=request.data)         
        if serializer.is_valid():             
            serializer.save()             
            return Response(serializer.data)         
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    elif request.method == 'DELETE':
        if (url.imageId is not 0):
            delete_image(url.imageId)         
        url.delete()         
        return Response(status=status.HTTP_204_NO_CONTENT)


@ratelimit(key='ip', rate='10/m', block=True)
@login_required(login_url='')
def url_delete(request, pk):
  url = get_object_or_404(ExpandedUrl, pk=pk)
  if (url.imageId is not 0):
    delete_image(url.imageId)   
  url.delete()
  return url_list(request)
