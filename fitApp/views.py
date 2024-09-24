from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from .serializers import RegisterSerializer

@api_view(['POST'])
@permission_classes([AllowAny])
def sign_up(request):
    if request.method == 'POST':
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def forgot_password(request):
    if request.method == 'POST':
        # print(request.data)
        req_username = request.data.get("username") 
        req_email = request.data.get("email")

        if req_username:
            user_obj = User.objects.filter(username = req_username,is_active=True)
        elif req_email:
            user_obj = User.objects.filter(email = req_email,is_active=True)

        # print("4567890",user_obj)
        if user_obj:
            email = user_obj.first().email
            # print('email--------',email)
            if email:
                # send_email(email)
                pass
                return Response({"message":"OTP sent to mail Successfully."},status=status.HTTP_200_OK)
            return Response({"message":"No mail is set with given username. Kindly contact administrator."},status=status.HTTP_400_BAD_REQUEST)
        return Response({"message":"User not found for given email/username."},status=status.HTTP_401_UNAUTHORIZED)



@api_view(['GET','POST','PUT','DELETE'])
@permission_classes([IsAuthenticated])
def workouts(request):
    if request.method == 'GET':
        pass
    elif request.method == 'POST':
        pass
    elif request.method == 'PUT':
        pass
    elif request.method == 'DELETE':
        pass