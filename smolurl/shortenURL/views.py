from django.shortcuts import render
from rest_framework import viewsets
from .models import URL
from .serializers import UrlSerializer
from rest_framework.response import Response
from django.http import HttpResponse, HttpResponseRedirect
import re
import json
# Create your views here.

def validateURL(url):
    regex = re.compile(
    r'^(?:http|ftp)s?://' # http:// or https://
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
    r'localhost|' #localhost...
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
    r'(?::\d+)?' # optional port
    r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    return (re.match(regex, url) is not None)

class UrlView(viewsets.ModelViewSet):
    queryset= URL.objects.all()
    serializer_class= UrlSerializer


    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return HttpResponseRedirect(serializer.data['address'])

    def create(self, request, *args, **kwargs):
        if validateURL(request.data['address']):    
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            #return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
            
            return Response(serializer.data)
        else:
            jsonResp= {
                'message': 'Please try again with a valid URL'
            }
            return Response(jsonResp)