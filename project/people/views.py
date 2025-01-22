
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, action, permission_classes, authentication_classes
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample,extend_schema_view
from people.models import Person
from people.serializer import PersonSerializer, Rigesterserializer, Loginserializer
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import TokenAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView

class CustomPagination(PageNumberPagination):
    page_size = 10  # Default page size
    page_size_query_param = 'page_size'  # Allow clients to override page size
    max_page_size = 100  # Maximum page size

class RegisterAPI(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        request=Rigesterserializer,
        responses={201: Rigesterserializer},
        description="Endpoint to register a new user."
    )
    def post(self, request):
        _data = request.data
        serializer = Rigesterserializer(data=_data)
        if not serializer.is_valid():
            return Response({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save()
        return Response({'message': 'User Created'}, status=status.HTTP_201_CREATED)

class LoginAPI(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        request=Loginserializer,
        responses={200: {'token': 'string'}},
        description="Endpoint to log in a user."
    )
    def post(self, request):
        _data = request.data
        serializer = Loginserializer(data=_data)
        if not serializer.is_valid():
            return Response({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
        validated_data = serializer.validated_data
        user = authenticate(username=validated_data['username'], password=validated_data['password'])
        
        if not user:
             return Response({'message': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
        
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'message': 'Login Successful', 'token': str(token)}, status=status.HTTP_200_OK)

class ClassPerson(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    @extend_schema(
        responses={200: PersonSerializer(many=True)},
        description="Endpoint to get all persons."
    )
    def get(self, request):
        obj_person = Person.objects.all()
        serializer = PersonSerializer(obj_person, many=True)
        return Response(serializer.data)

    @extend_schema(
        request=PersonSerializer,
        responses={201: PersonSerializer},
        description="Endpoint for POST method using APIView."
    )
    def post(self, request):
        serializer = PersonSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        request=PersonSerializer,
        responses={200: PersonSerializer},
        description="Endpoint for PUT method using APIView."
    )
    def put(self, request):
        data = request.data
        obj = Person.objects.get(id=data['id'])
        serializer = PersonSerializer(obj, data=data, partial=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        request=PersonSerializer,
        responses={200: PersonSerializer},
        description="Endpoint for PATCH method using APIView."
    )
    def patch(self, request):
        data = request.data
        obj = Person.objects.get(id=data['id'])
        serializer = PersonSerializer(obj, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        responses={200: PersonSerializer},
        description="Endpoint for DELETE method using APIView."
    )
    def delete(self, request):
        data = request.data
        obj = Person.objects.get(id=data['id'])
        obj.delete()
        return Response({'message': 'Person deleted'}, status=status.HTTP_200_OK)



@extend_schema_view(
    get=extend_schema(
        responses={200: PersonSerializer(many=True)},
        description="Retrieve all persons."
    ),
    post=extend_schema(
        request=PersonSerializer,
        responses={201: PersonSerializer},
        description="Create a new person."
    ),
    put=extend_schema(
        request=PersonSerializer,
        responses={200: PersonSerializer},
        description="Update a person by ID."
    ),
    patch=extend_schema(
        request=PersonSerializer,
        responses={200: PersonSerializer},
        description="Partially update a person by ID."
    ),
    delete=extend_schema(
        request=None,
        responses={200: {"message": "Person deleted"}},
        description="Delete a person by ID."
    )
)
@api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def person(request, id = None):
    if request.method == 'GET':
        queryset = Person.objects.all()
        serializer = PersonSerializer(queryset, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = PersonSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PUT':
        data = request.data
        obj = Person.objects.get(id=data['id'])
        serializer = PersonSerializer(obj, data=data, partial=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PATCH':
        data = request.data
        obj = Person.objects.get(id=data['id'])
        serializer = PersonSerializer(obj, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        obj = Person.objects.get(id = id)
        obj.delete()
        return Response({'message': 'Person deleted'}, status=status.HTTP_200_OK)


class PersonViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = PersonSerializer
    queryset = Person.objects.all()
    pagination_class = CustomPagination

    @extend_schema(
        parameters=[
            OpenApiParameter(name='search', description='Filter by name', required=False, type=str),
        ],
        responses={200: PersonSerializer(many=True)},
        description="List all persons with optional search and pagination."
    )
    def list(self, request):
        search = request.GET.get('search')
        queryset = self.queryset
        if search:
            queryset = queryset.filter(name__startswith=search)
        paginator = CustomPagination()
        result_page = paginator.paginate_queryset(queryset, request)
        serializer = PersonSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

# Define the index view if needed
@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def index(request):
    if request.method == "GET":
        a = {
            "Name": 'shihab',
            "age": 23,
            "place": "kochi"
        }
        return Response(a)