import random
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from datetime import date, timedelta
from .models import DailyEntry, FoodLog
import math
from django.conf import settings
import requests
from django.db.models import Sum

def start_page(request):
    return render(request, 'start.html')

@login_required
def home(request):
    return render(request, 'home.html')

@login_required
def health_score_view(request):
    user = request.user
    today = date.today()
    entry, created = DailyEntry.objects.get_or_create(user=user, date=today)

    if request.method == 'POST':
        if 'water' in request.POST:
            water = int(request.POST.get('water', 0))
            entry.water += water
        if 'sleep' in request.POST:
            sleep = int(request.POST.get('sleep', 0))
            entry.sleep = sleep
        entry.save()

    total_calories = FoodLog.objects.filter(user=user, date=today).aggregate(Sum('calories'))['calories__sum'] or 0

    goal_calories = 2000
    goal_water = 8
    goal_sleep = 8
    calorie_percent = round(min(total_calories / goal_calories, 1) * 100, 2) if goal_calories > 0 else 0
    water_percent = round(min(entry.water / goal_water, 1) * 100, 2) if goal_water > 0 else 0
    sleep_percent = round(min(entry.sleep / goal_sleep, 1) * 100, 2) if goal_sleep > 0 else 0
    health_score = int((calorie_percent + water_percent) / 2)

    radius = 50
    circumference = 2 * math.pi * radius
    big_circle_circumference = 2 * math.pi * (radius + 30)
    calorie_offset = round(circumference * (1 - (calorie_percent / 100)), 2)
    water_offset = round(circumference * (1 - (water_percent / 100)), 2)
    sleep_offset = round(circumference * (1 - (sleep_percent / 100)), 2)
    score_offset = round(big_circle_circumference * (1 - (health_score / 100)), 2)

    if health_score >= 100:
        score_label = "Perfect"
    elif health_score >= 80:
        score_label = "Excellent"
    elif health_score >= 60:
        score_label = "Good"
    elif health_score >= 40:
        score_label = "Fair"
    else:
        score_label = "Poor"

    context = {
        'calories': entry.calories,
        'water': entry.water,
        'goal_calories': goal_calories,
        'goal_water': goal_water,
        'calorie_percent': calorie_percent,
        'water_percent': water_percent,
        'sleep_percent': sleep_percent,
        'health_score': health_score,
        'calorie_offset': calorie_offset,
        'water_offset': water_offset,
        'score_offset': score_offset,
        'sleep_offset': sleep_offset,
        'score_label': score_label,
        'circumference': round(circumference, 2),
        'big_circle_circumference': round(big_circle_circumference, 2),
    }

    return render(request, 'health_score.html', context)

@login_required
def calorie_detail(request):
    user = request.user
    today = date.today()
    goal_calories = 2000

    if request.method == 'POST':
        if 'reset_calories' in request.POST:
            for i in range(7):
                day = today - timedelta(days=i)
                FoodLog.objects.filter(user=user, date=day).delete()
            return redirect('calorie_detail')
        elif 'generate_calorie_data' in request.POST:
            foods = [
                {"food": "Oatmeal", "meal": "breakfast", "calories": 150, "protein": 5, "carbs": 27, "fat": 3, "sugar": 1, "fiber": 4},
                {"food": "Chicken Salad", "meal": "lunch", "calories": 350, "protein": 30, "carbs": 10, "fat": 15, "sugar": 2, "fiber": 3},
                {"food": "Steak", "meal": "dinner", "calories": 450, "protein": 40, "carbs": 0, "fat": 25, "sugar": 0, "fiber": 0},
                {"food": "Apple", "meal": "snack", "calories": 95, "protein": 0, "carbs": 25, "fat": 0, "sugar": 19, "fiber": 4},
                {"food": "Protein Shake", "meal": "snack", "calories": 200, "protein": 25, "carbs": 5, "fat": 2, "sugar": 1, "fiber": 1},
            ]
            for i in range(7):
                day = today - timedelta(days=i)
                for _ in range(random.randint(2, 4)):
                    food = random.choice(foods)
                    FoodLog.objects.create(
                        user=user,
                        food=food["food"],
                        calories=food["calories"],
                        meal=food["meal"],
                        protein=food["protein"],
                        carbs=food["carbs"],
                        fat=food["fat"],
                        sugar=food["sugar"],
                        fiber=food["fiber"],
                        date=day
                    )
            return redirect('calorie_detail')
        elif request.POST.get('food', ''):
            food = request.POST.get('food')
            cals = int(request.POST.get('calories', 0) or 0)
            meal = request.POST.get('meal', 'other')
            protein = float(request.POST.get('protein', 0) or 0)
            carbs = float(request.POST.get('carbs', 0) or 0)
            fat = float(request.POST.get('fat', 0) or 0)
            sugar = float(request.POST.get('sugar', 0) or 0)
            fiber = float(request.POST.get('fiber', 0) or 0)
            FoodLog.objects.create(
                user=user,
                food=food,
                calories=cals,
                meal=meal,
                protein=protein,
                carbs=carbs,
                fat=fat,
                sugar=sugar,
                fiber=fiber,
                date=today
            )
        return redirect('calorie_detail')

    logs_today = FoodLog.objects.filter(user=user, date=today).order_by('-timestamp')
    total_calories = sum(log.calories for log in logs_today)

    calorie_values = []
    protein_values = []
    carbs_values = []
    fat_values = []
    sugar_values = []
    fiber_values = []
    labels = []

    for i in range(6, -1, -1):
        day = today - timedelta(days=i)
        logs = FoodLog.objects.filter(user=user, date=day)
        labels.append(day.strftime('%a'))
        calorie_values.append(sum(log.calories for log in logs))
        protein_values.append(sum(log.protein for log in logs))
        carbs_values.append(sum(log.carbs for log in logs))
        fat_values.append(sum(log.fat for log in logs))
        sugar_values.append(sum(log.sugar for log in logs))
        fiber_values.append(sum(log.fiber for log in logs))

    streak = 0
    for i in range(30):
        day = today - timedelta(days=i)
        logs = FoodLog.objects.filter(user=user, date=day)
        total = sum(log.calories for log in logs)
        print(f"{day}: {total} kcal")
        if 1800 <= total:
            streak += 1
        else:
            break

    protein_total = sum(log.protein for log in logs_today)
    carbs_total = sum(log.carbs for log in logs_today)
    fat_total = sum(log.fat for log in logs_today)
    sugar_total = sum(log.sugar for log in logs_today)
    fiber_total = sum(log.fiber for log in logs_today)

    macro_values = [protein_total, carbs_total, fat_total, sugar_total, fiber_total]

    if total_calories < 1200:
        suggestion = "You're low today. Add a healthy meal!"
    elif total_calories > 2200:
        suggestion = "You've passed your goal. Go light for dinner?"
    elif 1800 <= total_calories <= 2200:
        suggestion = "Perfect! You're in your goal zone."
    else:
        suggestion = "Keep logging to track progress."

    return render(request, 'calorie_detail.html', {
        'food_logs': logs_today,
        'total_calories': total_calories,
        'goal_calories': goal_calories,
        'calorie_labels': labels,
        'calorie_values': calorie_values,
        'protein_values': protein_values,
        'carbs_values': carbs_values,
        'fat_values': fat_values,
        'sugar_values': sugar_values,
        'fiber_values': fiber_values,
        'macro_values': macro_values,
        'streak': streak,
        'suggestion_message': suggestion,
    })


@login_required
def water_detail(request):
    today = date.today()
    entry, _ = DailyEntry.objects.get_or_create(user=request.user, date=today)

    if request.method == 'POST':
        if 'generate_water_data' in request.POST:
            for i in range(7):
                day = today - timedelta(days=i)
                dummy_water = random.randint(0, 12)
                entry, _ = DailyEntry.objects.get_or_create(user=request.user, date=day)
                entry.water = dummy_water
                entry.save()
            return redirect('water_detail')

        elif 'reset_water_data' in request.POST:
            for i in range(7):
                day = today - timedelta(days=i)
                entry = DailyEntry.objects.filter(user=request.user, date=day).first()
                if entry:
                    entry.water = 0
                    entry.save()
            return redirect('water_detail')

        elif 'reset_water' in request.POST:
            entry.water = 0
        else:
            water = int(request.POST.get('water', 0))
            entry.water += water
        entry.save()

    labels = []
    values = []
    for i in range(6, -1, -1):
        day = today - timedelta(days=i)
        labels.append(day.strftime('%a'))
        past_entry = DailyEntry.objects.filter(user=request.user, date=day).first()
        values.append(past_entry.water if past_entry else 0)

    return render(request, 'water_detail.html', {
        'entry': entry,
        'water_labels': labels,
        'water_values': values,
        'water_range': range(1, 9),
        })

@login_required
def sleep_detail(request):
    today = date.today()
    entry, _ = DailyEntry.objects.get_or_create(user=request.user, date=today)

    if request.method == 'POST':
        if 'generate_sleep_data' in request.POST:
            for i in range(7):
                day = today - timedelta(days=i)
                dummy_hours = random.randint(4, 10)
                entry, _ = DailyEntry.objects.get_or_create(user=request.user, date=day)
                entry.sleep = dummy_hours
                entry.save()
            return redirect('sleep_detail')

        elif 'reset_sleep_data' in request.POST:
            for i in range(7):
                day = today - timedelta(days=i)
                entry = DailyEntry.objects.filter(user=request.user, date=day).first()
                if entry:
                    entry.sleep = 0
                    entry.save()
            return redirect('sleep_detail')

        else:
            sleep = int(request.POST.get('sleep', 0))
            entry.sleep = sleep
            entry.save()
            return redirect('sleep_detail')

    labels = []
    values = []
    for i in range(6, -1, -1):
        day = today - timedelta(days=i)
        labels.append(day.strftime('%a'))
        past_entry = DailyEntry.objects.filter(user=request.user, date=day).first()
        values.append(past_entry.sleep if past_entry else 0)

    return render(request, 'sleep_detail.html', {
        'entry': entry,
        'sleep_labels': labels,
        'sleep_values': values,
    })

@login_required
def usda_food_search(request):
    query = request.GET.get('query', '')
    if not query:
        return JsonResponse({'error': 'Missing query'}, status=400)

    api_key = settings.USDA_API_KEY
    url = f'https://api.nal.usda.gov/fdc/v1/foods/search'
    params = {
        'api_key': api_key,
        'query': query,
        'pageSize': 5,
    }

    res = requests.get(url, params=params)
    if res.status_code != 200:
        return JsonResponse({'error': 'USDA API error'}, status=500)

    data = res.json()
    foods = []
    for item in data.get('foods', []):
        desc = item.get('description', '')
        cals = 0
        protein = carbs = fat = 0
        for nutrient in item.get('foodNutrients', []):
            name = nutrient.get('nutrientName', '').lower()
            val = nutrient.get('value', 0)
            if 'energy' in name:
                cals = val
            elif 'protein' in name:
                protein = val
            elif 'carbohydrate' in name:
                carbs = val
            elif 'fat' in name:
                fat = val
            elif 'sugar' in name:
                sugar = val
            elif 'fiber' in name:
                fiber = val
        foods.append({
            'name': desc,
            'calories': cals,
            'protein': protein,
            'carbs': carbs,
            'fat': fat,
            'sugar': sugar,
            'fiber': fiber,
        })

    return JsonResponse({'results': foods})