from django.db import models

# Create your models here.
from django.db import models

class Codeform(models.Model):
    room_code = models.CharField(max_length=50)  # To store room code
    username = models.CharField(max_length=100)  # To store username

    def __str__(self):
        return f"Room: {self.room_code}, User: {self.username}"
