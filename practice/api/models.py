from django.db import models

# Create your models here.
class User(models.Model):
    fullname = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    age = models.IntegerField()
    password = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    role = models.CharField(max_length=5, default='USER')
    
    def __str__(self):
        return self.fullname

# {
#     "fullname": "MARCUS SALOPASO",
#     "email": "marcussalopaso1@gmail.com",
#     "age": 19,
#     "password": "asdasdasdas",
#     "role": "ADMIN"
# }
