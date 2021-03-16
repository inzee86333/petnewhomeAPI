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
    user_image = models.ImageField(upload_to='images/user/', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"UserexID: {self.user_id} | {self.email}"


class Pet(models.Model):
    PET_STATUS = (
        ('nonAdopt', 'nonAdopt'),
        ('adopted', 'adopted'),
    )
    pet_id = models.AutoField(primary_key=True)
    owner_id = models.ForeignKey("appAPI.Userex", verbose_name="owner", on_delete=models.CASCADE)
    new_owner_id = models.ForeignKey("appAPI.Userex", verbose_name=(
        "new_owner"), on_delete=models.CASCADE, related_name='+', null=True)
    animal_type = models.CharField(max_length=255)
    species = models.CharField(max_length=255, null=True)
    birth_year = models.CharField(max_length=255, null=True)
    sex = models.CharField(max_length=255, null=True)
    disease = models.CharField(max_length=255, null=True)
    province_code = models.CharField(max_length=255)
    amphoe_code = models.CharField(max_length=255)
    status = models.CharField(max_length=255, choices=PET_STATUS, default='nonAdopt')

    def __str__(self):
        return f"PetID: {self.pet_id} | {self.owner_id}"


class PetImage(models.Model):
    pet_image_id = models.AutoField(primary_key=True)
    pet_id = models.ForeignKey("appAPI.Pet", verbose_name=("pet"), on_delete=models.CASCADE)
    pet_image = models.ImageField(upload_to='images/pets/')

    def __str__(self):
        return f"PetImageID: {self.pet_image_id} | {self.pet_id}"


class Chat(models.Model):
    chat_id = models.AutoField(primary_key=True)
    owner_id = models.ForeignKey("appAPI.Userex", verbose_name="owner", on_delete=models.CASCADE)
    finder_id = models.ForeignKey("appAPI.Userex", verbose_name="finder", on_delete=models.CASCADE, related_name='+')
    pet_id = models.ForeignKey("appAPI.Pet", verbose_name="pet", on_delete=models.CASCADE)


class Message(models.Model):
    message_id = models.AutoField(primary_key=True)
    chat_id = models.ForeignKey("appAPI.Chat", verbose_name="chat", on_delete=models.CASCADE)
    sender = models.ForeignKey("appAPI.Userex", verbose_name="sender", on_delete=models.CASCADE)
    receiver = models.ForeignKey("appAPI.Userex", verbose_name="receiver", on_delete=models.CASCADE, related_name='+')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
