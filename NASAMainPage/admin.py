from django.contrib import admin

from .models import Picture, AIModel, Dataset, DatasetClasses, Fold

# Register your models here.
class DatasetAdmin(admin.ModelAdmin):
    fields = ["dataset_name", "dataset_number_of_images"]


admin.site.register(Dataset, DatasetAdmin)
admin.site.register(Picture)
admin.site.register(AIModel)
admin.site.register(DatasetClasses)
admin.site.register(Fold)