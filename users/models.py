from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# Custom user model
class FoodUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profilePics/', default='default.jpg')
    biography = models.CharField(max_length=300)

    def __str__(self):
        return str(self.user.username)

