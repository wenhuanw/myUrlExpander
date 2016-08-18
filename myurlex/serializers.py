from django.forms import widgets 
from rest_framework import serializers
from myurlex.models import ExpandedUrl

class UrlSerializer(serializers.ModelSerializer):
       class Meta:
              model = ExpandedUrl
              fields = ('destination', 'origin', 'status', 'title', 'waybackUrl', 'timestamp', 'imageUrl','imageId')
       destination = serializers.URLField(default='')
       origin = serializers.URLField(default='http://')
       status = serializers.IntegerField(default=0)
       title = serializers.CharField(max_length=150)
       waybackUrl = serializers.URLField(default='')
       timestamp = serializers.CharField(max_length=50,default='')
       imageUrl = serializers.URLField(default='')
       imageId = serializers.IntegerField(default=0)  


def create(self, validated_data): 
       """ 
       Create and return a new `Users` instance, given the validated data.      
       """   
       return Users.objects.create(**validated_data)

def update(self, instance, validated_data):
      instance.destination = validated_data.get('destination', instance.destination)      
      instance.origin = validated_data.get('origin', instance.origin)      
      instance.status = validated_data.get('status', instance.status)      
      instance.title = validated_data.get('title', instance.title)      
      instance.waybackUrl = validated_data.get('waybackUrl', instance.waybackUrl)
      instance.timestamp = validated_data.get('timestamp', instance.timestamp)
      instance.imageUrl = validated_data.get('imageUrl', instance.imageUrl)
      instance.imageId = validated_data.get('imageId',instance.imageId)
      instance.save()
      return instance

