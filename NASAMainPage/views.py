# NASAMainPage/views.py
import datetime
import os

from django.shortcuts import render
from django.http import HttpResponse
import subprocess, random

from .models import Dataset,DatasetClasses, Picture

def current_datetime(request):
    now = datetime.datetime.now()
    html = '<html lang="en"<body>It is now %s.</body></html>' % now
    return HttpResponse(html)

def home(request):
    return render(request, 'home.html')

# NASAMainPage/views.py

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
    return render(request, 'datasets.html', {'datasets_with_classes': datasets_with_classes})

def game(request):
    return render(request, "game.html")

def models(request):
    return render(request, "models.html")

def about_us(request):
    return render(request, "about_us.html")



def run_script(request):
    if request.method == "POST":
        user_input = request.POST.get('user_input')
        result = subprocess.run(['python', 'NASAMainPage/static/scripts/your_script.py', user_input], capture_output=True, text=True)
        return HttpResponse(f"Script output: {result.stdout}")
    return HttpResponse("Invalid Request")