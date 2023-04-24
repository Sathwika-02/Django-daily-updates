from django.shortcuts import render,HttpResponse
from .models import Student,Article
from .serializers import StudentSerializer,ArticleSerializer,Userserialzer
from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from django.http import HttpResponse,JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import mixins
from rest_framework.authentication import SessionAuthentication,BasicAuthentication,TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
# Create your views here.
# serialization -> converting complex data type into python native datatype it is serialzation and rendering it to json so that it is understandable to frontend
def student_detail(request):
    stu=Student.objects.get(id=1)
    serializer=StudentSerializer(stu)  #converted complex datatype to python datatype
    json_data=JSONRenderer().render(serializer.data)
    return HttpResponse(json_data,content_type='application/json')
#get allstudents data
def student_list(request):
    stu=Student.objects.all()
    serializer=StudentSerializer(stu,many=True)  #converted complex datatype to python datatype
    json_data=JSONRenderer().render(serializer.data)
    return HttpResponse(json_data,content_type='application/json')

#derserislizatipn-> JSONParser() > converts parsed data into native python datatype
# afer validating data converts into complex data type

@api_view(['GET','POST','PATCH'])
def get_home(request):
    if request.method=='GET':
        return Response({
            'status':200,
            'message':'You called get method'
        })
    elif request.method=='POST':
        return Response({
            'status':200,
            'message':'You called post method'
        })
    elif request.method=='PATCH':
         return Response({
            'status':200,
            'message':'You called patch method'
        })
    else:
         return Response({
            'status':200,
            'message':'You called invalid method'
        })
@csrf_exempt
def article_list(request):
    if request.method=='GET':
        articles=Article.objects.all()
        serializer=ArticleSerializer(articles,many=True)
        return JsonResponse(serializer.data,safe=False)
    elif request.method=='POST':
        data=JSONParser().parse(request)
        serializer=ArticleSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data,status=201)
        return JsonResponse(serializer.errors,status=401)

@api_view(['GET','POST'])
def article_list(request):
    if request.method=='GET':
        articles=Article.objects.all()
        serializer=ArticleSerializer(articles,many=True)
        return Response(serializer.data)
    elif request.method=='POST':
        serializer=ArticleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','PUT','DELETE'])
def article_detail(request,pk):
    article=Article.objects.get(pk=pk)
    if request.method=='GET':
        serializer=ArticleSerializer(article)
        return Response(serializer.data)
    elif request.method=='PUT':
        serializer=ArticleSerializer(article,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    elif request.method=='DELETE':
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
#class based api views 

class ArticleAPIView(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    def get(self, request):
        article=Article.objects.all()
        serializer=ArticleSerializer(article,many=True)
        return Response(serializer.data)
    def post(self,request):
        serializer=ArticleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    

class ArticleDetails(APIView):
    def  get_object(self,id):
        return Article.objects.get(id=id)
    
    def get(self,request,id):
         article=self.get_object(id)
         serializer=ArticleSerializer(article)
         return Response(serializer.data)
    def put(self,request,id):
         article=self.get_object(id)
         serializer=ArticleSerializer(article,data=request.data)
         if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
    def delete(self,request,id):
         article=self.get_object(id)
         article.delete()
         return Response(status=status.HTTP_204_NO_CONTENT)


#Generic views and mixins
#     
class GenericAPIView(generics.GenericAPIView,mixins.ListModelMixin,mixins.CreateModelMixin,mixins.UpdateModelMixin,mixins.RetrieveModelMixin,mixins.DestroyModelMixin):
    serializer_class=ArticleSerializer
    queryset=Article.objects.all()
    lookup_field='id'
   # authentication_classes=[SessionAuthentication,BasicAuthentication]
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    def get(self,request,id=None):
        if id:
            return self.retrieve(request)
        else:
            return self.list(request)
        
        return self.list(request)
    
    def post(self,request):
        return self.create(request)
    
    def put(self,request,id=None):
        return self.update(request,id)
    def delete(self,request,id):
        return self.destroy(request,id)

class ArticleViewset(viewsets.ViewSet):
    def list(self,request):
         article=Article.objects.all()
         serializer=ArticleSerializer(article,many=True)
         return Response(serializer.data)
    def create(self,request):
        serializer=ArticleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self,request,pk=None):
        queryset=Article.objects.all()
        article=get_object_or_404(queryset,pk=pk)
        serializer=ArticleSerializer(article)
        return Response(serializer.data)
    
    def update(self,request,pk=None):
        article=Article.objects.get(pk=pk)
        serializer=ArticleSerializer(article,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
#Model view set
class ArticleModelviewset(viewsets.ModelViewSet):
    serializer_class=ArticleSerializer
    queryset=Article.objects.all()

class RegisterUser(APIView):
    def post(self,request):
        serializer=Userserialzer(data=request.data)
        if not serializer.is_valid():
            return Response({'status':403,'errors':serializer.errors,'message':'Something went wrong'})
        serializer.save()
        user=User.objects.get(username=serializer.data['username'])
        token_obj,_=Token.objects.get_or_create(user=user)
        return Response({'status':200,'payload':serializer.data,'token':str(token_obj)})



