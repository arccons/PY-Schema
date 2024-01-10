# from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
import SchemaCheck.src.FileProcessor as FP # processUploadedFile, getFileSubject, getTableColumns

# Create your views here.
@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def getData(request):
    row = FP.getSubjectList(request.data['subject'])
    return Response(row)

@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def getSubjectList(request):
    rowList = FP.getSubjectList()
    print(rowList)
    return Response(rowList)

@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def processFile(request):
    subjExists = FP.checkSubject(request.data['subject'])
    fileDF = FP.processUploadedFile(request.data['uploadedFile'], request.data['fileType'])
    print(fileDF)
    print(fileDF.dtypes)

    if subjExists:
        tableDF = FP.getTableColumns(request.data['subject'])
        FP.addFileRecords(tableDF)
    else:
        FP.createDBobjects(fileDF, request.data['table'], request.data['subject'])
        FP.addFileRecords(fileDF)

    return Response({"message": "Got some data!"})
