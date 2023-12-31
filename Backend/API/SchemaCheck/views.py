# from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from SchemaCheck.src.Test import processUploadedFile

""" @renderer_classes(...)
@parser_classes(...)
@authentication_classes(...)
@throttle_classes(...)
@permission_classes(...)
 """
# Create your views here.
@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def getData(request):
    return Response()

@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def processFile(request):
    prtStr = processUploadedFile(request.data['uploadedFile'], request.data['fileType'], request.data['subject'])
    #print(type(request))
    print(prtStr)
    return Response({"message": "Got some data!"})
