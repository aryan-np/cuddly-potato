from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from .models import TodoModel
from .serializers import RegisterSerializer,TodoSerializer

from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from rest_framework_simplejwt.tokens import RefreshToken



@api_view(["POST"])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username,password=password)
    
    if user is not None:
        refresh_token = RefreshToken.for_user(user)
        access_token = refresh_token.access_token
        return Response({
            "refresh":str(refresh_token),
            "access": str(access_token)
        },status=status.HTTP_200_OK)
        
    else:
        return Response({
            "error":"Invalid Credentials"
        },status=status.HTTP_404_NOT_FOUND)
        
        
@api_view(['POST'])
def register(request):
    serializer = RegisterSerializer(data = request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({
            "message":"Regestration successful"
        },status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
           
    
    
class TodoViewSet(viewsets.ModelViewSet):
    serializer_class = TodoSerializer
    queryset = TodoModel.objects.all()
    
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)  

    def get_queryset(self):
        queryset = TodoModel.objects.filter(owner=self.request.user)
        status = self.request.query_params.get('status')
        priority = self.request.query_params.get('priority')
        if status is not None:
            queryset = queryset.filter(status=status)
        if priority is not None:
            queryset = queryset.filter(priority=priority)
        return queryset
    
