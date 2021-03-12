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
    pet_id = models.AutoField(primary_key=True)
    owner_id = models.ForeignKey("appAPI.Userex", verbose_name=("owner"), related_name='petdata', on_delete=models.CASCADE)
    new_owner_id = models.ForeignKey("appAPI.Userex", verbose_name=(
        "new_owner"), on_delete=models.CASCADE, related_name='+', null=True)
    animal_type = models.CharField(max_length=255)
    species = models.CharField(max_length=255, null=True)
    birth_year = models.CharField(max_length=255, null=True)
    sex = models.CharField(max_length=255, null=True)
    disease = models.CharField(max_length=255, null=True)
    province = models.CharField(max_length=255)
    district = models.CharField(max_length=255)
    status = models.CharField(max_length=255, null=True)

    def __str__(self):
        return f"PetID: {self.pet_id} | {self.owner_id}"

class PetImage(models.Model):
    pet_image_id = models.AutoField(primary_key=True)
    pet_id = models.ForeignKey("appAPI.Pet", verbose_name=("pet"), related_name='petImages', on_delete=models.CASCADE)
    pet_image = models.ImageField(upload_to='images/pets/')

    def __str__(self):
        return f"PetImageID: {self.pet_image_id} | {self.pet_id}"

class Report(models.Model):
    report_id = models.AutoField(primary_key=True)
    reporter = models.ForeignKey("Userex", verbose_name="reporter", on_delete=models.CASCADE, related_name='reporter')
    report_to = models.ForeignKey("Userex", verbose_name="report_to", on_delete=models.CASCADE, related_name='report_to')
    pet_id = models.ForeignKey("Pet", verbose_name="pet", on_delete=models.CASCADE,)
    message = models.CharField(max_length=255)