from django.db import models

import os
from django.db.models.signals import post_save
from django.dispatch import receiver

class Dataset(models.Model):
    dataset_name = models.CharField(max_length=200)
    dataset_number_of_images = models.IntegerField()

    def __str__(self):
        return self.dataset_name

class DatasetClasses(models.Model):
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE)
    dataset_class_name = models.CharField(max_length=200)
    class_number_of_images = models.IntegerField()

    def __str__(self):
        return self.dataset_class_name

class Picture(models.Model):
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE)
    dataset_class = models.ForeignKey(DatasetClasses, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='temp/')  # Temporary path, will be overridden in save method
    image_name = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.image_name

    def save(self, *args, **kwargs):
        # Update the image_name field with the name of the uploaded image file
        if self.image and not self.image_name:
            self.image_name = self.image.name

        # Define the path for the new image
        self.image.field.upload_to = os.path.join('NASAMainPage', 'Datasets', self.dataset.dataset_name, self.dataset_class.dataset_class_name)
        super().save(*args, **kwargs)


class AIModel(models.Model):
    model_name = models.CharField(max_length=200)
    model_path = models.FileField(upload_to="uploads/")
    model_image = models.ImageField()

    def __str__(self):
        return self.model_name

class Fold(models.Model):
    fold_number = models.IntegerField()
    dataset_class = models.ForeignKey(DatasetClasses, on_delete=models.CASCADE)
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE)
    confusion_matrix = models.ImageField()
    precision = models.IntegerField()
    recall = models.IntegerField()
    f1score = models.IntegerField()
    support = models.IntegerField()
    accuracy = models.IntegerField()
    AI_model = models.ForeignKey(AIModel, on_delete=models.CASCADE)


@receiver(post_save, sender=Dataset)
def create_dataset_directory(sender, instance, created, **kwargs):
    if created:
        # Define the path for the new directory
        new_directory_path = os.path.join('NASAMainPage', 'Datasets', instance.dataset_name)

        # Create the new directory
        os.makedirs(new_directory_path, exist_ok=True)

@receiver(post_save, sender=DatasetClasses)
def create_classes_directory(sender, instance, created, **kwargs):
    if created:
        # Define the path for the new directory
        dataset_name = instance.dataset.dataset_name
        class_name = instance.dataset_class_name
        new_directory_path = os.path.join('NASAMainPage', 'Datasets', dataset_name, class_name)

        # Create the new directory
        os.makedirs(new_directory_path, exist_ok=True)
