from rest_framework.decorators import api_view,permission_classes,authentication_classes
from rest_framework.response import Response
from people.models import Person
from people.serializer import Personserializer,Rigesterserializer,loginserializer
from rest_framework.views import APIView
from rest_framework import viewsets,status
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.authentication import TokenAuthentication


class registerapi(APIView):
    permission_classes = [AllowAny]
    def post(self,request):
        _data=request.data
        serializer=Rigesterserializer(data=_data)

        if not serializer.is_valid():
            return Response({'message':serializer.errors},status=status.HTTP_404_NOT_FOUND)
        
        serializer.save()
        return Response({'message':'User Created'},status=status.HTTP_201_CREATED)

class loginapi(APIView):
    permission_classes = [AllowAny]
    def post(self,request):
        _data=request.data
        serializer=loginserializer(data=_data)
        if not serializer.is_valid():
            return Response({'message':serializer.errors},status=status.HTTP_404_NOT_FOUND)
        
        validated_data = serializer.validated_data
        user=authenticate(username=validated_data['username'],password=validated_data['password'])
        
        if not user:
             return Response({'message':'Invalid'},status=status.HTTP_404_NOT_FOUND)
        
        token,_=Token.objects.get_or_create(user=user)
        return Response({'message':'Login Sucessfull','token':str(token)},status=status.HTTP_200_OK)



class classperson(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes=[TokenAuthentication]
    def get(self,request):
        objperson=Person.objects.all()
        serializer=Personserializer(objperson,many=True)
        return Response(serializer.data)
    def post(self,request):
        return Response("this is post method using apiview")
    def put(self,request):
        return Response("this is put method using apiview")
    def patch(self,request):
        return Response("this is patch method using apiview")
    def delete(self,request):
        return Response("this is delete method using apiview")



@api_view(['GET','POST','PUT'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def index(request):
    if request.method =="GET":
        a={
            "Name:":'shihab',
            "age:":23,
            "palce:":"kochi"
        }
        return Response(a)
    elif request.method =="POST":
        return Response('this is post method')
    elif request.method =="PUT":
        return Response('this is put method')
    

@api_view(['GET','PUT','PATCH','DELETE','POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def person(request):
    if request.method=='GET':
        objperson=Person.objects.all()
        serializer=Personserializer(objperson,many=True)
        return Response(serializer.data)
    elif request.method=='POST':
        data=request.data
        serializer=Personserializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    elif request.method=='PUT':
        data=request.data
        obj=Person.objects.get(id=data['id'])
        serializer=Personserializer(obj,data=data,partial=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    elif request.method=='PATCH':
        data=request.data
        obj=Person.objects.get(id=data['id'])
        serializer=Personserializer(obj,data=data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    elif request.method=='DELETE':
        data=request.data
        obj=Person.objects.get(id=data['id'])
        return Response({'message':'person deleted'})

class personviewsets(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes=[TokenAuthentication]
    serializer_class=Personserializer
    queryset=Person.objects.all()

    def list(self,request):
        search=request.GET.get('search')
        queryset=self.queryset

        if search:
            queryset=queryset.filter(name__startswith=search)

        serializer=Personserializer(queryset,many=True)
        return Response({'status':200,'data':serializer.data})