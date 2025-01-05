from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializer import UserSerializer

@api_view(['GET'])
def user_list(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def user_create(request):
    data = request.data
    serializer = UserSerializer(data=data) # Create a new instance of UserSerializer
    if serializer.is_valid(): # Check if the data is valid
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED) # 201: Created
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) # 400: Bad Request


@api_view(['PUT'])
def user_update(request, pk):
    try:
        user = User.objects.get(pk=pk)  # Retrieve the user by primary key
    except User.DoesNotExist:
        return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

    serializer = UserSerializer(user, data=request.data)  # Pass the user instance and the updated data
    if serializer.is_valid():  # Check if the data is valid
        serializer.save()  # Save the updated user data
        return Response(serializer.data, status=status.HTTP_200_OK)  # 200: OK
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # 400: Bad Request