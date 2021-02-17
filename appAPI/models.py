from django.db import models

# Create your models here.
class Userex(models.Model):
    USER_TYPE = (
        ('ow', 'owner'),
        ('fi', 'finder'),
    )
    user_id = models.AutoField(primary_key=True)
    email = models.CharField(unique=True, max_length=255)
    password = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone_number = models.CharField(unique=True, max_length=10)
    address = models.CharField(max_length=255)
    user_type = models.CharField(max_length=10,choices=USER_TYPE)
    photo_user = models.ImageField(upload_to='images/user/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"ID: {self.user_id} | {self.email} | {self.created_at}"
