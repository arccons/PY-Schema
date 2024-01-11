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
    print(f"Subject List = \n{rowList}")
    return Response(rowList)

@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def processFile(request):
    subjBaseExists = FP.checkSubject(request.data['subject'])
    fileDF = FP.processUploadedFile(request.data['uploadedFile'], request.data['fileType'])
    print(f"FileDF = \n{fileDF}")
    print(f"FileDF.dtypes = \n{fileDF.dtypes}")

    if not subjBaseExists:
        subjBaseExists = FP.createSubjectBase(fileDF, request.data['table'], request.data['subject'])

    recordsExist = False
    if subjBaseExists:
        recordsExist = FP.addFileRecords(fileDF, request.data['subject'])

    if recordsExist:
        return Response({"message": "File uploaded!"})
    else:
        return Response({"message": "Error!"})
