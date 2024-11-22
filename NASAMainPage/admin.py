from django.contrib import admin

from .models import Dataset, FoldInfo, UserSections
from .models import Picture, FoldClassInfo, AIModel, DatasetClasses, Fold
from django import forms

import nested_admin


class DatasetAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Dataset Fields", {"fields": ["dataset_name", "dataset_number_of_images", "dataset_description", "dataset_zip"]})
    ]
    readonly_fields = ["dataset_number_of_images"]  # Make the field read-only

class PictureAdmin(admin.ModelAdmin):
    list_display = ["dataset", "dataset_class", "image_name"]
    list_filter = ["dataset", "dataset_class"]

class FoldClassInfoInline(nested_admin.NestedTabularInline):
    model = FoldClassInfo
    extra = 1

class FoldInfoInline(nested_admin.NestedStackedInline):
    model = FoldInfo
    extra = 1
    inlines = [FoldClassInfoInline]

class FoldAdmin(nested_admin.NestedModelAdmin):
    fieldsets = [
        (None, {"fields": ["dataset", "AI_model"]})
    ]
    inlines = [FoldInfoInline]

class UserSectionsInline(admin.StackedInline):
    model = UserSections

class AIAdmin(admin.ModelAdmin):
    inlines = [UserSectionsInline]

admin.site.register(UserSections)
admin.site.register(Fold, FoldAdmin)
admin.site.register(Dataset, DatasetAdmin)
admin.site.register(Picture, PictureAdmin)
admin.site.register(AIModel, AIAdmin)
admin.site.register(DatasetClasses)