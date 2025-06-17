from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.db.models import Case, When, Value, IntegerField

from .models import TodoModel
from .serializers import RegisterSerializer,TodoSerializer

from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from rest_framework_simplejwt.tokens import RefreshToken

from django.core.mail import send_mail
from django.conf import settings



@api_view(["POST"])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username,password=password)
    email = user.email
    
    if user is not None:
        refresh_token = RefreshToken.for_user(user)
        access_token = refresh_token.access_token
        send_mail(
        subject='Welcome!',
        message='Thank you for signing up.',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email],
        fail_silently=False,  # Set True to avoid crashing on error
    )
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
    
    
@api_view(['GET'])
def search(request):
    query = request.query_params.get('q')
    search_results = TodoModel.objects.filter( title__icontains = query ).annotate(starts_with=Case(
        When(title__istartswith=query, then=Value(0)),
        default=Value(1),
        output_field=IntegerField()
    )).order_by('starts_with','title')
    print(search_results)
    serializer = TodoSerializer(search_results,many=True)
    return Response(serializer.data,status=status.HTTP_200_OK)
    # return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
           

    
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
    

@api_view(['POST'])
def logout(request):
    try:
        print("Raw body:", request.body)
        print("Parsed data:", request.data)
        
        refresh_token = request.data.get("refresh")  # safer
        if not refresh_token:
            return Response({"detail": "Refresh token not provided"}, status=status.HTTP_400_BAD_REQUEST)

        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response(status=status.HTTP_205_RESET_CONTENT)

    except Exception as e:
        print("Exception:", e)
        return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    
    



    