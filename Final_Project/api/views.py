import random
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from Final_Project.settings import get_static_file
from pickle import load
from tensorflow.keras.models import load_model
from .forms import *
from .utils import extract_features, generate_desc


max_length = 34

# load the tokenizer
tokenizer = get_static_file('api', 'tokenizer/tokenizer.pkl')
tokenizer = load(open(tokenizer, 'rb'))

# load the model
model = get_static_file('api', 'model/model.h5')
model = load_model(model)


def predictor(img):
    photo = extract_features(img)
    description = generate_desc(model, tokenizer, photo, max_length)
    return description


def get_name():
    while True:
        name = ''.join(random.choice('abcdefghijklmnopqrstuvwxyz0123456789')
                    for _ in range(50))
        if not ApiImage.objects.filter(name=name):
            return name


def return_error():
    response = JsonResponse({"status": "error"})
    response.status_code = "400"
    return response


@csrf_exempt
def predict(request):
    try:
        if request.method == 'POST':
            name = get_name()
            date = {
                'Main_Img': request.POST.get('image'),
                'name': name
            }
            files = {
                'Main_Img': request.FILES.get('image')
            }
            form = ApiImageForm(date, files)

            if form.is_valid():
                form.save()

                image = ApiImage.objects.filter(name=name).first()
                image = image.Main_Img
                image = image.path

                result = predictor(image)

                return JsonResponse({"status": "success", "result": result})
            else:
                return return_error()

        else:
            return return_error()
    except:
        return return_error()
