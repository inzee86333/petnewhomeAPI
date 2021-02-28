from django.db import models

# Create your models here.
class Userex(models.Model):
    USER_TYPE = (
        ('ow', 'owner'),
        ('fi', 'finder'),
    )
    user_id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True, max_length=255)
    password = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone_number = models.CharField(unique=True, max_length=10)
    address = models.CharField(max_length=255, null=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPE, null=True)
    photo_user = models.ImageField(upload_to='images/user/', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"ID: {self.user_id} | {self.email} | {self.created_at}"

class Pets(models.Model):
    pet_id = models.AutoField(primary_key=True)
    owner_id = models.ForeignKey("appAPI.Userex", verbose_name=("owner"), on_delete=models.CASCADE)
    new_owner_id = models.ForeignKey("appAPI.Userex", verbose_name=(
        "new_owner"), on_delete=models.CASCADE, related_name='+', null=True)
    animal_type = models.CharField(max_length=255)
    species = models.CharField(max_length=255, null=True)
    birth_year = models.CharField(max_length=255, null=True)
    sex = models.CharField(max_length=255, null=True)
    disease = models.CharField(max_length=255, null=True)
    status = models.CharField(max_length=255, null=True)
