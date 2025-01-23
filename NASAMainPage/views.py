# NASAMainPage/views.py
import os
import random
from pathlib import Path
from PIL import Image

from django.conf import settings
from django.shortcuts import render, get_object_or_404

from .models import Dataset, DatasetClasses, Picture, AIModel, Fold, FoldInfo, UserSections


def index(request):
    return render(request, "index.html")


def home(request):
    return render(request, 'home.html')


def test_model(request, model_name):
    model = get_object_or_404(AIModel, model_name=model_name)
    dataset = get_object_or_404(Dataset, dataset_name=model.model_dataset.dataset_name)
    dataset_classes = DatasetClasses.objects.filter(dataset=dataset)
    total_number_of_images = dataset.dataset_number_of_images

    images = {
        cls.dataset_class_name: [
            {image.image_name: os.path.relpath(image.image.path, 'NASAMainPage/static/')}
            for image in Picture.objects.filter(dataset=dataset, dataset_class=cls)
        ]
        for cls in dataset_classes
    }

    cls_info = {
        cls.dataset_class_name: {cls.class_number_of_images: f"{cls.class_number_of_images / total_number_of_images:.1%}"}
        for cls in dataset_classes
    }

    return render(request, 'models/test_model.html', {
        'model_name': model_name,
        'dataset': dataset,
        'cls_info': cls_info,
        'total_images': total_number_of_images,
        'images': images,
    })


def models(request):
    models = AIModel.objects.all()
    return render(request, "models/models.html", {"models": list(models)})


def datasets(request):
    datasets = Dataset.objects.all()
    datasets_with_classes = {
        dataset.dataset_name: {
            'classes': [
                {
                    'class_name': cls.dataset_class_name,
                    'number_of_images': cls.class_number_of_images,
                    'random_image': os.path.relpath(random.choice(Picture.objects.filter(dataset_class=cls)).image.path, 'NASAMainPage/static/') if Picture.objects.filter(dataset_class=cls).exists() else None
                }
                for cls in DatasetClasses.objects.filter(dataset=dataset)
            ],
            'number_of_images': sum(cls.class_number_of_images for cls in DatasetClasses.objects.filter(dataset=dataset))
        }
        for dataset in datasets
    }
    return render(request, 'datasets/datasets.html', {'datasets_with_classes': datasets_with_classes})


def model_detail(request, model_name):
    model = get_object_or_404(AIModel, model_name=model_name)
    model_dataset = model.model_dataset
    user_sections = UserSections.objects.filter(model=model).all()

    fold = Fold.objects.filter(dataset=model_dataset.id, AI_model=model).select_related('dataset', 'AI_model').get()
    foldinfo = FoldInfo.objects.filter(fold=fold.id).prefetch_related('foldclassinfo_set__dataset_class_id').all()

    fold_info_dict = {
        "Overall" if info.fold_number == 0 else f"Fold {info.fold_number}": {
            "ConfusionMatrix": os.path.join('/images/models', os.path.basename(info.confusion_matrix.path)),
            "Accuracy": info.accuracy,
            "Classes": {
                classinfo.dataset_class_id.dataset_class_name: {
                    "Precision": classinfo.precision,
                    "Recall": classinfo.recall,
                    "F1Score": classinfo.f1score,
                    "Support": classinfo.support,
                }
                for classinfo in info.foldclassinfo_set.all()
            }
        }
        for info in foldinfo
    }

    file_path = Path(settings.BASE_DIR) / 'NASAMainPage' / 'static' / 'models' / f"{model.model_name}-{model.model_dataset.dataset_name}" / 'model.json'
    active = file_path.exists()

    return render(request, 'models/model.html', {"model": model, "fold": fold_info_dict, "sections": user_sections, "active": active})


def dataset_detail(request, dataset_name):
    dataset = get_object_or_404(Dataset, dataset_name=dataset_name)
    dataset_classes = DatasetClasses.objects.filter(dataset=dataset)
    total_number_of_images = dataset.dataset_number_of_images

    images = {
        cls.dataset_class_name: [
            {image.image_name: os.path.relpath(image.image.path, 'NASAMainPage/static/')}
            for image in Picture.objects.filter(dataset=dataset, dataset_class=cls)
        ]
        for cls in dataset_classes
    }

    cls_info = {
        cls.dataset_class_name: {cls.class_number_of_images: f"{cls.class_number_of_images / total_number_of_images:.1%}"}
        for cls in dataset_classes
    }

    return render(request, 'datasets/dataset.html', {
        'dataset': dataset,
        'cls_info': cls_info,
        'total_images': total_number_of_images,
        'images': images
    })


def main_game_screen(request):
    return render(request, "game/main_game_screen.html")


def game_selection(request):
    # TODO active_models no longer works properly since we need to loop over all the datasets first before getting active_model
    models = AIModel.objects.all()
    datasets = Dataset.objects.all()

    active_models = [model for model in models if (Path(settings.BASE_DIR) / 'NASAMainPage' / 'static' / 'models' / f'{model.model_name}-HiRiSE' / 'model.json').exists()]
    active_datasets = [model.model_dataset for model in active_models if model.model_dataset in datasets]

    dataset_to_models = {}
    for model in active_models:
        dataset_name = model.model_dataset.dataset_name
        if dataset_name not in dataset_to_models:
            dataset_to_models[dataset_name] = []
        dataset_to_models[dataset_name].append(model.model_name)

    datasets_with_classes = {
        dataset.dataset_name: {
            'classes': [
                {
                    'class_name': cls.dataset_class_name.replace('_', ' ').title(),
                    'number_of_images': cls.class_number_of_images,
                    'random_image': os.path.relpath(random.choice(Picture.objects.filter(dataset_class=cls)).image.path, 'NASAMainPage/static/') if Picture.objects.filter(dataset_class=cls).exists() else None
                }
                for cls in DatasetClasses.objects.filter(dataset=dataset)
            ],
            'number_of_images': sum(cls.class_number_of_images for cls in DatasetClasses.objects.filter(dataset=dataset)),
            'description': dataset.dataset_description,
        }
        for dataset in active_datasets
    }

    print(datasets_with_classes)

    return render(request, "game/game_selection.html", {"active": active_models, "datasets": datasets_with_classes, "dataset_to_models": dataset_to_models})

import base64
from io import BytesIO

def model_prepping(request):
    mode = request.GET.get('mode')
    gamemode = request.GET.get('gamemode')
    dataset = request.GET.get('dataset')
    difficulty = request.GET.get('difficulty')
    model = request.GET.get('model')
    username = request.GET.get('username')

    chosen_dataset = get_object_or_404(Dataset, dataset_name=dataset)
    dataset_classes = DatasetClasses.objects.filter(dataset=chosen_dataset.id)
    all_images = []
    for cls in dataset_classes:
        class_pictures = Picture.objects.filter(dataset=chosen_dataset, dataset_class=cls)
        for image in class_pictures:
            all_images.append({cls.dataset_class_name: os.path.relpath(image.image.path, "NASAMainPage/static/")})

    random.shuffle(all_images)
    random_image_list = random.choices(all_images, k=5)
    round_images = []

    for data in random_image_list:
        for cls in data:
            image_path = data[cls]
            img = Image.open(f"NASAMainPage/static/{image_path}")

            if difficulty == "Medium":
                img = img.rotate(random.randrange(0, 360))
            elif difficulty == "Hard":
                img = img.rotate(random.randrange(0, 360))
                img = img.resize((img.width // 2, img.height // 2))
            elif difficulty == 'Mixed':
                img = img.rotate(random.randrange(0, 360))
                img = img.resize((img.width // 2, img.height // 2))
                # img = img.transpose(Image.FLIP_LEFT_RIGHT)

            buffered = BytesIO()
            img.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
            round_images.append({cls: f"data:image/png;base64,{img_str}"})

    context = {
        'mode': mode,
        'gamemode': gamemode,
        'dataset': dataset,
        'difficulty': difficulty,
        'model': model,
        'username': username,
        'images': round_images
    }
    return render(request, "game/model_prepping.html", context)

def game(request):
    # TODO get round_images classes, then get the class names and pass them to the template
    mode = request.GET.get('mode')
    gamemode = request.GET.get('gamemode')
    dataset = request.GET.get('dataset')
    difficulty = request.GET.get('difficulty')
    model = request.GET.get('model')
    username = request.GET.get('username')
    round_images = request.GET.get('round_images')

    chosen_dataset = get_object_or_404(Dataset, dataset_name=dataset)
    dataset_classes = DatasetClasses.objects.filter(dataset=chosen_dataset.id)
    all_classes = [cls for cls in dataset_classes]

    print(dataset_classes)

    context = {
        'mode': mode,
        'gamemode': gamemode,
        'dataset': dataset,
        'difficulty': difficulty,
        'model': model,
        'username' : username,
        'class_choices': all_classes
    }

    print(mode, gamemode, dataset, difficulty, model, username)

    return render(request, "game/gameplay.html", context)

def leaderboard(request):
    return render(request, "game/leaderboard.html")


def about_us(request):
    return render(request, "about_us.html")