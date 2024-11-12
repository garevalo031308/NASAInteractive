import shutil

from django.contrib import admin
from django.core.exceptions import ValidationError
from django.db import models

import os
from zipfile import ZipFile
from django.db.models.signals import post_save
from django.dispatch import receiver
from scripts.regsetup import description

from NASAMainPage.static.scripts.mass_insert import mass_insert

def validate_zip_file(value):
    if not value.name.endswith('.zip'):
        raise ValidationError('Only .zip files are allowed.')


def validate_picture_file(value):
    if not value.name.endswith('.jpg'):
        raise ValidationError('Only .jpg, jpeg, or .png files are allowed.')
    elif not value.name.endswith('.jpeg'):
        raise ValidationError('Only .jpg, jpeg, or .png files are allowed.')
    elif not value.name.endswith('.png'):
        raise ValidationError('Only .jpg, jpeg, or .png files are allowed.')

class Dataset(models.Model):
    dataset_name = models.CharField(max_length=200)
    dataset_number_of_images = models.IntegerField(editable=False, null=True)
    dataset_description = models.TextField()
    dataset_zip = models.FileField(upload_to='NASAMainPage/static/temp/', validators=[validate_zip_file], blank=True, null=True)

    def __str__(self):
        return self.dataset_name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.dataset_zip:
            zip_file_path = self.dataset_zip.path
            with ZipFile(zip_file_path, 'r') as zip_ref:
                zip_ref.extractall('NASAMainPage/static/temp/')
            dataset_dir = os.path.join('NASAMainPage', 'static', 'temp', os.path.splitext(os.path.basename(zip_file_path))[0])
            self.process_unzipped_files(dataset_dir)
            self.clean_temp_folder()

    def process_unzipped_files(self, dataset_dir):
        total_images = 0
        for class_name in os.listdir(dataset_dir):
            class_path = os.path.join(dataset_dir, class_name)
            if os.path.isdir(class_path):
                image_count = len([name for name in os.listdir(class_path) if os.path.isfile(os.path.join(class_path, name))])
                total_images += image_count
                class_instance = DatasetClasses.objects.create(dataset=self, dataset_class_name=class_name, class_number_of_images=image_count)
                dest_class_path = os.path.join('NASAMainPage', 'static', 'Datasets', self.dataset_name, class_name)
                os.makedirs(dest_class_path, exist_ok=True)
                for image_name in os.listdir(class_path):
                    image_path = os.path.join(class_path, image_name)
                    if os.path.isfile(image_path):
                        shutil.move(image_path, os.path.join(dest_class_path, image_name))
                        Picture.objects.create(dataset=self, dataset_class=class_instance, image=os.path.join(dest_class_path, image_name), image_name=image_name)
        self.dataset_number_of_images = total_images
        self.dataset_zip = None
        super().save(update_fields=['dataset_number_of_images'])

    @staticmethod
    def clean_temp_folder():
        temp_folder = 'NASAMainPage/static/temp/'
        for filename in os.listdir(temp_folder):
            file_path = os.path.join(temp_folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f'Failed to delete {file_path}. Reason: {e}')

class DatasetClasses(models.Model):
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE)
    dataset_class_name = models.CharField(max_length=200)
    class_number_of_images = models.IntegerField()

    def __str__(self):
        return self.dataset_class_name

class Picture(models.Model):
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE)
    dataset_class = models.ForeignKey(DatasetClasses, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='temp/', validators=[validate_picture_file])  # Temporary path, will be overridden in save method
    image_name = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.image_name

    def save(self, *args, **kwargs):
        # Update the image_name field with the name of the uploaded image file
        if self.image and not self.image_name:
            self.image_name = self.image.name

        # Define the path for the new image
        self.image.field.upload_to = os.path.join('NASAMainPage', 'static', 'Datasets', self.dataset.dataset_name, self.dataset_class.dataset_class_name)
        super().save(*args, **kwargs)

class AIModel(models.Model):
    model_name = models.CharField(max_length=200)
    model_path = models.FileField(upload_to="uploads/", validators=[validate_zip_file])
    model_image = models.ImageField()
    model_dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE)
    model_description = models.TextField()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

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
        new_directory_path = os.path.join('NASAMainPage', 'static', 'Datasets', instance.dataset_name)
        os.makedirs(new_directory_path, exist_ok=True)

@receiver(post_save, sender=DatasetClasses)
def create_classes_directory(sender, instance, created, **kwargs):
    if created:
        # Define the path for the new directory
        dataset_name = instance.dataset.dataset_name
        class_name = instance.dataset_class_name
        new_directory_path = os.path.join('NASAMainPage', 'static', 'Datasets', dataset_name, class_name)

        # Create the new directory
        os.makedirs(new_directory_path, exist_ok=True)
