from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *
from .serializers import *
from rest_framework import generics
# Create your views here.

@api_view(['GET'])
def retrieve(request):
    obj=Student.objects.all()
    serializer =StudentSerializer(obj,many=True)
    return Response({'status':200,'message': serializer.data})

@api_view(['POST'])
def create(request):
    serializer=StudentSerializer(data=request.data)
    if  not serializer.is_valid():
        print(serializer.errors)
        return Response({'status':403,'errors':serializer.errors,'message':'something went wrong'})
    serializer.save()
    return Response({'status':200,'payload':serializer.data,'message':'you sent'})

@api_view(['GET'])
def getparticular(request,pk):
    obj=Student.objects.get(id=pk)
    serializer=StudentSerializer(obj,many=False)
    return Response({'status':200,'message': serializer.data})

@api_view(['POST'])
def update(request,pk):
    task=Student.objects.get(id=pk)
    serializer=StudentSerializer(instance=task,data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response('Updated')

@api_view(['DELETE'])
def delete(request,pk):
    obj=Student.objects.get(id=pk)
    obj.delete()
    return Response("Item successfully deleted")


















"""class ListToDo(generics.ListAPIView):
    queryset=ToDo.objects.all()
    serializer_class=ToDoserializer

class DetailToDo(generics.RetrieveUpdateAPIView):
    queryset=ToDo.objects.all()
    serializer_class=ToDoserializer

class CreateToDo(generics.CreateAPIView):
    queryset=ToDo.objects.all()
    serializer_class=ToDoserializer

class DeleteToDo(generics.DestroyAPIView):
    queryset=ToDo.objects.all()
    serializer_class=ToDoserializer"""

