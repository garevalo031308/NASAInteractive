import os
import shutil

from django.contrib import admin

from .models import Picture, AIModel, Dataset, DatasetClasses, Fold, InsertDatasetZip
from django.contrib import admin
from django.shortcuts import render, redirect
from django.urls import path
from .models import Dataset, InsertDatasetZip
from .forms import UploadZipForm
from NASAMainPage.static.scripts.mass_insert import mass_insert

# Register your models here.
class DatasetAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Dataset Fields", {"fields" : ["dataset_name", "dataset_number_of_images"]})
    ]

class InsertDatasetAdmin(admin.ModelAdmin):
    change_list_template = "admin/insert_dataset_changelist.html"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('upload-zip/', self.admin_site.admin_view(self.upload_zip), name='upload-zip'),
        ]
        return custom_urls + urls

    def upload_zip(self, request):
        if request.method == 'POST':
            form = UploadZipForm(request.POST, request.FILES)
            if form.is_valid():
                dataset_zip = request.FILES['dataset_zip']
                original_name = dataset_zip.name
                temp_dir = os.path.join('NASAMainPage', 'static', 'temp')
                temp_path = os.path.join(temp_dir, original_name)

                # Save the uploaded file to the temp directory
                with open(temp_path, 'wb+') as destination:
                    for chunk in dataset_zip.chunks():
                        destination.write(chunk)

                # Execute the mass_insert script with the new path
                mass_insert(temp_path)
                self.message_user(request, "Dataset uploaded and processed successfully.")
                return redirect('..')
        else:
            form = UploadZipForm()
        return render(request, 'admin/upload_zip.html', {'form': form})

admin.site.register(InsertDatasetZip, InsertDatasetAdmin)
# admin.site.register(Dataset, DatasetAdmin)
# admin.site.register(Picture)
admin.site.register(AIModel)
# admin.site.register(DatasetClasses)
# admin.site.register(Fold)