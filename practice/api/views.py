from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializer import UserSerializer


@api_view(['GET'])
def user_list(request):
    user_id = request.query_params.get('id')  # Retrieve the 'id' parameter from the query string
    
    # Retrieve all users from the database
    users = User.objects.all()
    total_users = users.count()  # Get the total number of users
    
    if user_id:
        # Convert to integer for comparison
        try:
            user_id = int(user_id)
        except ValueError:
            return Response({
                "message": "Invalid ID. It must be an integer."
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if the user_id exceeds the number of users
        if user_id > total_users:
            return Response({
                "message": f"ID cannot exceed the number of users. There are {total_users} users in the database."
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # If valid, filter by user_id
        users = User.objects.filter(id=user_id)

    # Serialize the data
    serializer = UserSerializer(users, many=True)
    
    # Prepare the response data
    response_data = {
        "message": "User fetched successfully",
        "status": status.HTTP_200_OK,
        "length": total_users,  # Include the total length of users
        "users": serializer.data
    }
    
    return Response(response_data)

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
        return Response({
            "message": "User not found",
            "status": status.HTTP_404_NOT_FOUND
        }, status=status.HTTP_404_NOT_FOUND)  # Return a 404 if the user doesn't exist
    
    if request.method == 'DELETE':
        user.delete()
        return Response({
            "message": "User deleted successfully",
            "status": status.HTTP_204_NO_CONTENT
        }, status=status.HTTP_204_NO_CONTENT)
    
    elif request.method == 'PUT':
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "User updated successfully",
                "status": status.HTTP_200_OK,
                "user": serializer.data
            }, status=status.HTTP_200_OK)
        return Response({
            "message": "Invalid data",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


