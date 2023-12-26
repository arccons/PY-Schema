# from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from SchemaCheck.src.Test import processUploadedFile, getFileSubject

# Create your views here.
@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def getData(request):
    row = getFileSubject(request.data['subject'])
    return Response(row)

@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def processFile(request):
    row = getFileSubject(request.data['subject'])
    if not row:
        return Response(None)
    fileDtypes = processUploadedFile(request.data['uploadedFile'], request.data['fileType'])
    print(fileDtypes)
    return Response({"message": "Got some data!"})
