# NASAMainPage/views.py
import datetime
import os
from pathlib import Path

from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
import subprocess, random

from .models import Dataset, DatasetClasses, Picture, AIModel, Fold, FoldInfo, FoldClassInfo, UserSections


def index(request):
    return render(request, "index.html")

def home(request):
    return render(request, 'home.html')

# NASAMainPage/views.py

# NASAMainPage/views.py

def test_model(request, model_name):
    model = get_object_or_404(AIModel, model_name=model_name)
    model_path = os.path.join('models', model_name, 'model.json')  # Correctly construct the path

    dataset = get_object_or_404(Dataset, dataset_name=model.model_dataset.dataset_name)
    dataset_classes = DatasetClasses.objects.filter(dataset=dataset)
    total_number_of_images = dataset.dataset_number_of_images
    images = {}
    for cls in dataset_classes:
        paths_list = []
        list_of_images = Picture.objects.filter(dataset=dataset, dataset_class=cls)
        for image in list_of_images:
            paths_list.append({image.image_name: os.path.relpath(image.image.path, 'NASAMainPage/static/')})
        images[cls.dataset_class_name] = paths_list

    cls_info = {}
    for cls in dataset_classes:
        class_name = cls.dataset_class_name
        number_of_images = cls.class_number_of_images
        percentage = f"{number_of_images / total_number_of_images:.1%}"
        cls_info[class_name] = {number_of_images: percentage}

    return render(request, 'models/test_model.html', {
        'model_name': model_name,
        'dataset': dataset,
        'cls_info': cls_info,
        'total_images': total_number_of_images,
        'images': images,
    })

def models(request):
    """
        This view contains the different models that the user has inputed into the DB
    """
    models = AIModel.objects.all()
    list_models = [model for model in models]
    return render(request, "models/models.html", {"models":list_models})

def datasets(request):
    datasets = Dataset.objects.all()
    datasets_with_classes = {}
    for dataset in datasets:
        classes = DatasetClasses.objects.filter(dataset=dataset)
        class_data = []
        for cls in classes:
            pictures = Picture.objects.filter(dataset_class=cls)
            random_picture = random.choice(pictures) if pictures else None
            if random_picture:
                relative_image_path = os.path.relpath(random_picture.image.path, 'NASAMainPage/static/')
                image_url = f"{relative_image_path}"
            else:
                image_url = None
            class_data.append({
                'class_name': cls.dataset_class_name,
                'number_of_images': cls.class_number_of_images,
                'random_image': image_url
            })
        datasets_with_classes[dataset.dataset_name] = {
            'classes': class_data,
            'number_of_images': sum(cls.class_number_of_images for cls in classes)
        }
    return render(request, 'datasets/datasets.html', {'datasets_with_classes': datasets_with_classes})

def model_detail(request, model_name):
    model = get_object_or_404(AIModel, model_name=model_name)
    model_dataset = model.model_dataset

    user_sections = UserSections.objects.filter(model=model).all()

    fold = Fold.objects.filter(dataset=model_dataset.id, AI_model=model).select_related('dataset', 'AI_model').get()
    foldinfo = FoldInfo.objects.filter(fold=fold.id).prefetch_related('foldclassinfo_set__dataset_class_id').all()

    fold_info_dict = {}
    for info in foldinfo:
        foldclassinfo = info.foldclassinfo_set.all()
        fold_number = "Overall" if info.fold_number == 0 else f"Fold {info.fold_number}"
        fold_info_dict[fold_number] = {
            "ConfusionMatrix": os.path.join('/images/models', os.path.basename(info.confusion_matrix.path)),
            "Accuracy": info.accuracy,
            "Classes": {}
        }
        for classinfo in foldclassinfo:
            fold_info_dict[fold_number]["Classes"][classinfo.dataset_class_id.dataset_class_name] = {
                "Precision": classinfo.precision,
                "Recall": classinfo.recall,
                "F1Score": classinfo.f1score,
                "Support": classinfo.support,
            }

    file_path = Path(settings.BASE_DIR) / 'NASAMainPage' / 'static' / 'models' / model.model_name / 'model.json'
    if file_path.exists():
        active = True
    else:
        active = False

    return render(request, 'models/model.html', {"model": model, "fold": fold_info_dict, "sections": user_sections, "active" : active})

def dataset_detail(request, dataset_name):
    dataset = get_object_or_404(Dataset, dataset_name=dataset_name)
    dataset_classes = DatasetClasses.objects.filter(dataset=dataset)
    total_number_of_images = dataset.dataset_number_of_images
    images = {}
    for cls in dataset_classes:
        paths_list = []
        list_of_images = Picture.objects.filter(dataset=dataset, dataset_class=cls)
        for image in list_of_images:
            paths_list.append({image.image_name : os.path.relpath(image.image.path,'NASAMainPage/static/')})
        images[cls.dataset_class_name] = paths_list

    cls_info = {}
    for cls in dataset_classes:
        class_name = cls.dataset_class_name
        number_of_images = cls.class_number_of_images
        percentage = f"{number_of_images / total_number_of_images:.1%}"
        cls_info[class_name] = {number_of_images : percentage}
    return render(request, 'datasets/dataset.html', {
        'dataset': dataset,
        'cls_info': cls_info,
        'total_images': total_number_of_images,
        'images' : images
    })

def game(request):
    models = AIModel.objects.all()
    # list_models = [model for model in models]
    list_models = []
    for model in models:
        file_path = Path(settings.BASE_DIR) / 'NASAMainPage' / 'static' / 'models' / model.model_name / 'model.json'
        if file_path.exists():
            list_models.append(model)
        else:
            continue

    return render(request, "game/main_game_screen.html", {"models" : list_models})

def leaderboard(request):
    return render(request, "game/leaderboard.html")

def about_us(request):
    return render(request, "about_us.html")



def run_script(request):
    if request.method == "POST":
        user_input = request.POST.get('user_input')
        result = subprocess.run(['python', 'NASAMainPage/static/scripts/your_script.py', user_input], capture_output=True, text=True)
        return HttpResponse(f"Script output: {result.stdout}")
    return HttpResponse("Invalid Request")