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

        response_data = {
            "message": "User added successfully",
            "status": status.HTTP_201_CREATED,
            'user': serializer.data
        }
        return Response(response_data, status=status.HTTP_201_CREATED) # 201: Created
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) # 400: Bad Request

@api_view(['PUT', 'DELETE'])
def user_details(request, pk):
    try:
        user = User.objects.get(pk=pk)  # Corrected from User.object to User.objects
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)  # It's better to return a 404 if the user doesn't exist
    
    if request.method == 'DELETE':
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    elif request.method == 'PUT':
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


