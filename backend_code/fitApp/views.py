from fitApp.serializers import WorkoutSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
import traceback
from fitApp.models import Workout
from .serializers import RegisterSerializer
import logging

logger = logging.getLogger(__name__)
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
def workouts(request,id=None):
    try:

        # get workout endpoint
        if request.method == 'GET':
            
            req_user = request.user
            workout_objects = Workout.objects.filter(status=1,user=req_user).all()
            if len(workout_objects)==0:
                return Response({"message":"Workout created successfully.","data":WorkoutSerializer(workout_objects,many=True).data}, status=status.HTTP_200_OK)
            return Response({"message":"Data successfully.","data":WorkoutSerializer(workout_objects,many=True).data}, status=status.HTTP_200_OK)
        
        # create workout endpoint
        elif request.method == 'POST':
            request.data['user'] = request.user.id  
            create_data = request.data
            srl_obj = WorkoutSerializer(data=create_data)
            if srl_obj.is_valid(raise_exception=False):
                srl_obj.save()
                return Response({"message":"Workout created successfully.","data":srl_obj.data}, status=status.HTTP_201_CREATED)
            return Response({"message":"Error while creating the workout.","data":srl_obj.errors},status=status.HTTP_400_BAD_REQUEST)
        
        # update workout endpoint
        elif request.method == 'PUT':
            try:
                workout = Workout.objects.get(id=id)  
            except Workout.DoesNotExist:
                return Response({"message": "Workout not found.","data":""}, status=status.HTTP_404_NOT_FOUND)

            # Ensure the user is authorized to update this workout (optional)
            if workout.user != request.user:
                return Response({"message": "You do not have permission to update this workout.","data":""}, status=status.HTTP_403_FORBIDDEN)

            srl_obj = WorkoutSerializer(workout, data=request.data, partial=True)  # Allow partial updates
            if srl_obj.is_valid(raise_exception=False):
                srl_obj.save()
                return Response({"message": "Workout updated successfully.", "data": srl_obj.data}, status=status.HTTP_200_OK)
            return Response({"message": "Error while updating the workout.", "data": srl_obj.errors}, status=status.HTTP_400_BAD_REQUEST)
        
        # delete workout endpoint
        elif request.method == 'DELETE':
            try:
                workout_obj = Workout.objects.get(id=id)
            except Workout.DoesNotExist:
                return  Response({"message": "Workout not found.", "data": ""}, status=status.HTTP_404_NOT_FOUND)
            workout_obj.delete()
            return  Response({"message": "Workout deleted successfully.", "data": WorkoutSerializer(workout_obj).data}, status=status.HTTP_200_OK)

    except Exception as ex:
        logger.error(traceback.format_exc())