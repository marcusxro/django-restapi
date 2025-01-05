from django.urls import path, include
from .views import user_list, user_create, user_details


urlpatterns = [
    path('users/', user_list, name='user_list'),
    path('users/create/', user_create, name='user_create'), 
    # path('users/update/', user_update, name='user_update')

    
    path('users/<int:pk>', user_details, name="user_details")
]