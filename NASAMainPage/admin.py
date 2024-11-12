from django.contrib import admin

from .models import Dataset
from .models import Picture, AIModel, DatasetClasses, Fold


class DatasetAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Dataset Fields", {"fields": ["dataset_name", "dataset_number_of_images", "dataset_description", "dataset_zip"]})
    ]
    readonly_fields = ["dataset_number_of_images"]  # Make the field read-only

class PictureAdmin(admin.ModelAdmin):
    list_display = ["dataset", "dataset_class", "image_name"]
    list_filter = ["dataset", "dataset_class"]

admin.site.register(Dataset, DatasetAdmin)
admin.site.register(Picture, PictureAdmin)
admin.site.register(AIModel)
admin.site.register(DatasetClasses)
admin.site.register(Fold)