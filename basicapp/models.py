from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

# class UserProfil(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     # Add other fields for the user's profile if needed
#     # For example: profile_picture = models.ImageField(upload_to='profile_pics/', blank=True)

#     def __str__(self):
#         return self.user.username

    
class client(models.Model):
    
    user = models.ForeignKey(User, on_delete= models.CASCADE,null=True)
    Client_id = models.CharField(max_length=100, default='')
    Secret_key = models.CharField(max_length=100, default='')
    fy_id = models.CharField(max_length=100, default='')
    app_id_type = models.CharField(max_length=100, default='')
    totp_key = models.CharField(max_length=100, default='')
    pin = models.CharField(max_length=100, default='')
    app_id = models.CharField(max_length=100, default='')
    redirect_uri = models.CharField(max_length=100, default='')
    app_type = models.CharField(max_length=100, default='')
    app_id_hash = models.CharField(max_length=100, default='')

    

    def __str__(self):
        return self.Client_id

