from django.db import models

# Create your models here.
class Picture(models.Model):
    image_classifier = models.CharField(max_length=200)
    image = models.ImageField(width_field=227, height_field=227)
    image_name = models.CharField(max_length=200)
    dataset_name = models.CharField(max_length=200)

class AIModel(models.Model):
    model_name = models.CharField(max_length=200)
    model_path = models.FileField(upload_to="uploads/")