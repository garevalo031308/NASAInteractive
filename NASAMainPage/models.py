import shutil
from tkinter.constants import CASCADE

from django.contrib import admin
from django.core.exceptions import ValidationError
from django.db import models

import os
from zipfile import ZipFile
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from NASAMainPage.static.scripts.mass_insert import mass_insert

def validate_zip_file(value):
    if not value.name.endswith('.zip'):
        raise ValidationError('Only .zip files are allowed.')

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
            clean_temp_folder()

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
    model_path = models.FileField(upload_to="NASAMainPage/static/temp", validators=[validate_zip_file], blank=True, null=True)
    model_image = models.ImageField(upload_to=f"NASAMainPage/static/images/models/{model_name}")
    model_dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE)
    model_description = models.TextField()
    model_batch_size = models.IntegerField()
    model_epoch = models.IntegerField()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.model_path:
            zip_file_path = self.model_path.path
            with ZipFile(zip_file_path, 'r') as zip_ref:
                zip_ref.extractall('NASAMainPage/static/temp/')
            model_dir = os.path.join('NASAMainPage', 'static', 'temp',
                                     os.path.splitext(os.path.basename(zip_file_path))[0])
            self.process_unzipped_files(model_dir)
        # if self.model_image:
        #     dest_image_path = os.path.join("NASAMainPage", 'static', 'images', 'models', self.model_name,
        #                                    self.model_dataset.dataset_name)
        #     os.makedirs(dest_image_path, exist_ok=True)
        #     image_name = os.path.basename(self.model_image.path)
        #     dest_image_full_path = os.path.join(dest_image_path, image_name)
        #     shutil.move(self.model_image.path, dest_image_full_path)
        #     self.model_image = dest_image_full_path
        clean_temp_folder()


    def process_unzipped_files(self, model_dir):
        dest_model_path = os.path.join("NASAMainPage", "static", "models", f"{self.model_name}-{self.model_dataset}")
        os.makedirs(dest_model_path, exist_ok=True)
        for item in os.listdir(model_dir):
            item_path = os.path.join(model_dir, item)
            if os.path.isfile(item_path):
                shutil.move(item_path, dest_model_path)
        self.model_path = os.path.join(dest_model_path, "model.json")
        super().save(update_fields=["model_path"])

    def __str__(self):
        return self.model_name

class UserSections(models.Model):
    model = models.ForeignKey(AIModel, on_delete=models.CASCADE)
    section_name = models.CharField(max_length=200)
    section_info = models.TextField()
    section_image = models.ImageField(blank=True)

    def __str__(self):
        return self.section_name

class Fold(models.Model):
    fold_name = models.CharField(max_length=200, editable=False)  # Make the field non-editable
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE)
    AI_model = models.ForeignKey(AIModel, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.fold_name = f"{self.AI_model.model_name}-{self.dataset.dataset_name}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.fold_name

class FoldInfo(models.Model):
    fold = models.ForeignKey(Fold, on_delete=models.CASCADE)  # Add this line
    fold_number = models.IntegerField() # 0 for overall
    confusion_matrix = models.ImageField(upload_to="NASAMainPage/static/images/models")
    accuracy = models.FloatField()

class FoldClassInfo(models.Model):
    foldinfo = models.ForeignKey(FoldInfo, on_delete=models.CASCADE)
    dataset_class_id = models.ForeignKey(DatasetClasses, on_delete=models.CASCADE)
    precision = models.FloatField()
    recall = models.FloatField()
    f1score = models.FloatField()
    support = models.FloatField()

class Leaderboard(models.Model):
    username = models.CharField(max_length=200)
    score = models.FloatField()
    game_mode = models.CharField(max_length=200)

class Definition(models.Model):
    term = models.CharField(max_length=200)
    definition = models.CharField(max_length=200)

class Game(models.Model):
    gamemode = models.CharField(max_length=200)
    difficulty = models.CharField(max_length=200)
    ai_model = models.ForeignKey(AIModel, on_delete=models.CASCADE)
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE)
    username = models.CharField(max_length=200)
    total_score = models.IntegerField()
    number_of_rounds = models.IntegerField()
    number_correct = models.IntegerField()
    number_incorrect = models.IntegerField()
    active_game = models.BooleanField()
    current_round = models.IntegerField(default=1)

class Round(models.Model):
    gameID = models.ForeignKey(Game, on_delete=models.CASCADE)
    round_number = models.IntegerField()
    score = models.IntegerField()
    correct = models.BooleanField()
    image = models.ForeignKey(Picture, on_delete=models.CASCADE)

class Scoreboard(models.Model):
    name = models.CharField(max_length=200)
    score = models.FloatField()
    gameID = models.ForeignKey(Game, on_delete=models.CASCADE)



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

@receiver(post_delete, sender=AIModel)
def delete_model_files(sender, instance, **kwargs):
    model_dir = os.path.join("NASAMainPage", "static", "models", instance.model_name)
    if os.path.exists(model_dir):
        shutil.rmtree(model_dir)

@receiver(post_delete, sender=Dataset)
def delete_picture_files(sender, instance, **kwargs):
    dataset_dir = os.path.join("NASAMainPage", "static", "models", instance.dataset_name)
    if os.path.exists(dataset_dir):
        shutil.rmtree(dataset_dir)
