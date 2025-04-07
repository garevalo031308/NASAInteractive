# NASAMainPage/views.py
import json
import os
import random
from pathlib import Path
from PIL import Image

from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from .models import Dataset, DatasetClasses, Picture, AIModel, Fold, FoldInfo, UserSections, Game, Round, Leaderboard


def calculate_score(correct, time_taken, beat_ai_time):
    if not correct:
        return 0

    scoring = {
        "base_score_correct": 1000,
        "time_bonus_max": 1000,
        "time_penalty_per_millisecond": 0.03,
        "ai_bonus": {
            "beat_time": 200,
            "beat_accuracy": 300,
        },
        "max_time": 30,  # seconds
    }

    base = scoring["base_score_correct"]
    time_bonus = max(0, scoring["time_bonus_max"] - int(time_taken* scoring["time_penalty_per_millisecond"]))

    ai_bonus = 0
    if beat_ai_time:
        ai_bonus += scoring["ai_bonus"]["beat_time"]

    total_score = base + time_bonus + ai_bonus
    return total_score

def calculate_ai_score(correct, time_taken):
    scoring = SCORING_CONFIG = {
        "base_score_correct": 1000,
        "time_bonus_max": 1000,
        "time_penalty_per_millisecond": 0.03,
        "ai_bonus": {
            "beat_time": 200,
            "beat_accuracy": 300,
        },
        "max_time": 30,
    }
    if not correct: return 0
    base = scoring["base_score_correct"]
    time_bonus = max(0, scoring["time_bonus_max"] - int(time_taken * scoring["time_penalty_per_millisecond"]))

    total_score = base + time_bonus
    return total_score

def index(request):
    return render(request, "index.html")


def home(request):
    return render(request, 'home.html')


def test_model(request, id):
    model = get_object_or_404(AIModel, id=id)
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
        'model_name': model.model_name,
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
                    'random_image': os.path.relpath(random.choice(Picture.objects.filter(dataset_class=cls)).image.path,
                                                    'NASAMainPage/static/') if Picture.objects.filter(dataset_class=cls).exists() else None
                }
                for cls in DatasetClasses.objects.filter(dataset=dataset)
            ],
            'number_of_images': sum(cls.class_number_of_images for cls in DatasetClasses.objects.filter(dataset=dataset))
        }
        for dataset in datasets
    }
    return render(request, 'datasets/datasets.html', {'datasets_with_classes': datasets_with_classes})


def model_detail(request, id):
    model = get_object_or_404(AIModel, id=id)
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

def model_prepping(request):
    mode = request.GET.get('mode')
    gamemode = request.GET.get('gamemode')
    dataset = request.GET.get('dataset')
    difficulty = request.GET.get('difficulty')
    model = request.GET.get('model')
    username = request.GET.get('username')
    number_of_rounds = 5

    chosen_dataset = get_object_or_404(Dataset, dataset_name=dataset)
    dataset_classes = DatasetClasses.objects.filter(dataset=chosen_dataset.id)
    classes = [cls.dataset_class_name for cls in dataset_classes]
    all_images = []
    for cls in dataset_classes:
        class_pictures = Picture.objects.filter(dataset=chosen_dataset, dataset_class=cls)
        for image in class_pictures:
            all_images.append({cls.dataset_class_name: os.path.relpath(image.image.path, "NASAMainPage/static/")})

    random.shuffle(all_images)
    random_image_list = random.choices(all_images, k=5)
    round_images = []
    image_paths = []

    ai_model = get_object_or_404(AIModel, model_name=model, model_dataset=chosen_dataset)

    upload_game = Game(gamemode=gamemode, dataset=chosen_dataset, difficulty=difficulty, ai_model=ai_model,
                       username=username, total_score=0, number_of_rounds=number_of_rounds,
                       number_correct=0, number_incorrect=0, active_game=True, ai_total_score=0,
                       ai_number_correct=0, ai_number_incorrect=0)
    upload_game.save()

    game_id = upload_game.id

    for i in range(number_of_rounds):
        current_round_image = random_image_list[i]
        current_round_cls = list(current_round_image.keys())[0]
        image_path = current_round_image[current_round_cls]
        picture_instance = get_object_or_404(Picture, image=os.path.join("NASAMainPage\\static\\", image_path))
        new_round = Round(gameID=upload_game, round_number=i+1, score=0,
                          correct=False, image=picture_instance, ai_score=0,
                          player_time=0, player_answer="", ai_time=0, ai_answer="",
                          ai_correct = False
                          )
        new_round.save()
        round_images.append({current_round_cls: image_path})
        image_paths.append(image_path)

    print(round_images)
    print(image_paths)
    print(classes)

    context = {
        'mode': mode,
        'gamemode': gamemode,
        'dataset': dataset,
        'difficulty': difficulty,
        'model': model,
        'username': username,
        'images': round_images,
        'game_id': game_id,
        'image_paths': image_paths,
        'class_choices': classes,
    }
    return render(request, "game/model_prepping.html", context)

def game(request):
    game_id = request.GET.get('gameid')
    game = get_object_or_404(Game, id=game_id)

    current_round_number = game.current_round
    current_round = get_object_or_404(Round, gameID=game_id, round_number=current_round_number)
    round_image = current_round.image
    round_image_class = round_image.dataset_class

    chosen_dataset = get_object_or_404(Dataset, dataset_name=game.dataset.dataset_name)
    dataset_classes = DatasetClasses.objects.filter(dataset=chosen_dataset.id)
    all_classes = [cls for cls in dataset_classes]
    all_classes_names = [cls.dataset_class_name for cls in all_classes]

    # Ensure round_image_class is in the list and get 3 other random classes
    other_classes = [cls.dataset_class_name for cls in all_classes if cls != round_image_class]
    random_classes = random.sample(other_classes, 3)
    class_choices = random_classes + [round_image_class.dataset_class_name]
    random.shuffle(class_choices)

    correct_class = round_image_class.dataset_class_name
    print(game_id)

    context = {
        'model': game.ai_model.model_name,
        'round_image': os.path.relpath(round_image.image.path, "NASAMainPage/static"),
        'round_number': current_round_number,
        'round_image_class': round_image_class,
        'class_choices': class_choices,
        'model_class_choices': all_classes_names,
        'correct_class': correct_class,
        'gameid': game_id
    }

    return render(request, "game/gameplay.html", context)

def round_results(request):
    game_id = request.GET.get('gameid')
    selected_class = request.GET.get('selectedClass')
    time_taken =  request.GET.get('timeTaken')

    game = get_object_or_404(Game, id=game_id)
    current_round = game.current_round
    current_round = get_object_or_404(Round, gameID=game_id, round_number=current_round)

    round_class = current_round.image.dataset_class
    if str(round_class).strip() == str(selected_class).strip():
        correct_answer = True
    else:
        correct_answer = False

    ai_time = current_round.ai_time

    if float(time_taken) < ai_time:
        beat_ai_time = True
    else:
        beat_ai_time = False

    player_score = calculate_score(correct_answer, float(time_taken), beat_ai_time)
    ai_score = calculate_ai_score(correct_answer, ai_time)

    print("Player Score:", player_score)
    print("AI Score:", ai_score)

    print(correct_answer, beat_ai_time)

    print(game_id)
    print(selected_class)
    print(time_taken)
    current_round.score = player_score
    current_round.ai_score = ai_score
    current_round.player_time  = float(time_taken)
    current_round.player_answer = selected_class
    current_round.correct = correct_answer
    current_round.save()

    game.current_round = game.current_round+1
    game.total_score = game.total_score+player_score
    game.ai_total_score = game.ai_total_score+ai_score
    game.save()

    context = {
        'selected_class': selected_class,
        'time_taken': time_taken,
        'correct_answer': current_round.image.dataset_class.dataset_class_name,
        'ai_score': ai_score,
        'player_score': player_score,
        'ai_time': current_round.ai_time,
        'ai_answer': current_round.ai_answer,
        'gameid': game_id,
        'round_number': current_round.round_number,
    }

    return render(request, "game/round_results.html", context)

def game_results(request):
    game_id = request.GET.get('gameid')

    game = get_object_or_404(Game, id=game_id)

    new_leaderboard = Leaderboard(username=game.username, game_id=game, score=game.total_score,
                                  game_mode=game.gamemode, ai_model=game.ai_model, dataset=game.dataset,
                                  ai_score=game.ai_total_score)

    new_leaderboard.save()
    context = {}
    return render(request, "game/end_game.html", context)

@csrf_exempt
def save_predictions(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        results = data.get('results', [])
        game_id = data.get('game_id')

        # Save the results to the session or database
        request.session['prediction_results'] = results
        print(results)
        print(game_id)

        for i in range(5):
            if i < len(results):
                result = results[i]
                predicted_class = result.get('predictedClass')
                time_taken = result.get('timeTaken')
                print(f"Prediction Result {i+1}: Class - {predicted_class}, Time Taken - {time_taken} ms")
                ai_rounds = get_object_or_404(Round, gameID=game_id, round_number=i+1)
                ai_rounds.ai_answer = predicted_class
                ai_rounds.ai_time = float(time_taken)
                ai_rounds.ai_correct = True if ai_rounds.image.dataset_class.dataset_class_name.strip() == predicted_class.strip() else False
                ai_rounds.save()
                print(ai_rounds.ai_answer)

        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'error'}, status=400)

def leaderboard(request):
    return render(request, "game/leaderboard.html")


def about_us(request):
    return render(request, "about_us.html")