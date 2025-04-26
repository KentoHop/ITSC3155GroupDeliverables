import random
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from datetime import date, timedelta
from HealthScore.models import TodoItem
from .models import DailyEntry, FoodLog
import math
from django.conf import settings
import requests
from django.db.models import Sum

import os

# Create or import suggestion_generate module
try:
    from suggestion_generate import generate_health_suggestion
except ImportError:
    # Fallback implementation if module doesn't exist
    def generate_health_suggestion(calories=None, sleep=None, water=None, streak=None, macros=None):
        suggestions = []
        if calories is not None:
            if calories < 1200:
                suggestions.append("Try to increase your calorie intake with nutritious foods.")
            elif calories > 2200:
                suggestions.append("Consider reducing your calorie intake slightly.")
        if sleep is not None:
            if sleep < 7:
                suggestions.append("Aim for 7-9 hours of sleep for optimal health.")
            else:
                suggestions.append("Great job maintaining a healthy sleep schedule!")
        if water is not None:
            if water < 8:
                suggestions.append(f"Try to drink {8-water} more glasses of water today.")
            else:
                suggestions.append("You're doing great with hydration!")
        if streak is not None and streak > 3:
            suggestions.append(f"Amazing! You've maintained your goals for {streak} days.")
        if macros is not None and all(v is not None for v in macros):
            protein, carbs, fat, sugar, fiber = macros
            if protein < 50:
                suggestions.append("Consider adding more protein to your diet.")
            if fiber < 25:
                suggestions.append("Try to include more fiber-rich foods in your meals.")
        return suggestions




def start_page(request):
    return render(request, 'start.html')

@login_required
def home(request):
    todos = TodoItem.objects.filter(user=request.user)
    health_data = calculate_health_data(request.user)
    
    return render(request, 'home.html', {
        'todos': todos,
        'health_score': health_data['health_score'],
        'big_circle_circumference': health_data['big_circle_circumference'],
        'score_offset': health_data['score_offset'],
        'calorie_percent': health_data['calorie_percent'],
        'water_percent': health_data['water_percent'],
        'sleep_percent': health_data['sleep_percent'],
        'calorie_offset': health_data['calorie_offset'],
        'water_offset': health_data['water_offset'],
        'sleep_offset': health_data['sleep_offset'],
        'score_label': health_data['score_label'],
        'circumference': health_data['circumference'],
    })

# modified
def health_score_view(request):
    if request.method == 'POST':
        user = request.user
        today = date.today()
        entry, created = DailyEntry.objects.get_or_create(user=user, date=today)

        if 'water' in request.POST:
            water = int(request.POST.get('water', 0))
            entry.water += water
        if 'sleep' in request.POST:
            sleep = int(request.POST.get('sleep', 0))
            entry.sleep = sleep
        entry.save()

    health_data = calculate_health_data(request.user)
    return render(request, 'health_score.html', health_data)
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

    # Store in session for suggestions
    request.session['suggestion_calories'] = total_calories

    goal_calories = 2000
    goal_water = 8
    goal_sleep = 8
    calorie_percent = round(min(total_calories / goal_calories, 1) * 100, 2) if goal_calories > 0 else 0
    water_percent = round(min(entry.water / goal_water, 1) * 100, 2) if goal_water > 0 else 0
    sleep_percent = round(min(entry.sleep / goal_sleep, 1) * 100, 2) if goal_sleep > 0 else 0
    health_score = int((calorie_percent + water_percent + sleep_percent) / 3)  # Added sleep to calculation

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
        'total_calories': total_calories,
        'water': entry.water,
        'sleep': entry.sleep,
        'goal_calories': goal_calories,
        'goal_water': goal_water,
        'goal_sleep': goal_sleep,
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

# Separate function to calculate health data
def calculate_health_data(user):
    today = date.today()
    entry, created = DailyEntry.objects.get_or_create(user=user, date=today)

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

    return {
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


@login_required
def calorie_detail(request):
    user = request.user
    today = date.today()
    goal_calories = 2000

    if request.method == 'POST':
        if 'reset_calories' in request.POST:
            # Use bulk delete instead of looping
            days = [today - timedelta(days=i) for i in range(7)]
            FoodLog.objects.filter(user=user, date__in=days).delete()
        elif 'generate_calorie_data' in request.POST:
            foods = [
                {"food": "Oatmeal", "meal": "breakfast", "calories": 150, "protein": 5, "carbs": 27, "fat": 3, "sugar": 1, "fiber": 4},
                {"food": "Chicken Salad", "meal": "lunch", "calories": 350, "protein": 30, "carbs": 10, "fat": 15, "sugar": 2, "fiber": 3},
                {"food": "Steak", "meal": "dinner", "calories": 450, "protein": 40, "carbs": 0, "fat": 25, "sugar": 0, "fiber": 0},
                {"food": "Apple", "meal": "snack", "calories": 95, "protein": 0, "carbs": 25, "fat": 0, "sugar": 19, "fiber": 4},
                {"food": "Protein Shake", "meal": "snack", "calories": 200, "protein": 25, "carbs": 5, "fat": 2, "sugar": 1, "fiber": 1},
            ]

            # Prepare bulk creation
            new_logs = []
            for i in range(7):
                day = today - timedelta(days=i)
                for _ in range(random.randint(2, 4)):
                    food = random.choice(foods)
                    new_logs.append(FoodLog(
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
                    ))
            # Bulk create
            FoodLog.objects.bulk_create(new_logs)
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

    # Get data for past 7 days in one query
    days = [today - timedelta(days=i) for i in range(7)]
    days_dict = {day: [] for day in days}
    all_logs = FoodLog.objects.filter(user=user, date__in=days)

    for log in all_logs:
        days_dict[log.date].append(log)

    # Process data for chart
    calorie_values = []
    protein_values = []
    carbs_values = []
    fat_values = []
    sugar_values = []
    fiber_values = []
    labels = []

    for i in range(6, -1, -1):
        day = today - timedelta(days=i)
        logs = days_dict[day]
        labels.append(day.strftime('%a'))
        calorie_values.append(sum(log.calories for log in logs))
        protein_values.append(sum(log.protein for log in logs))
        carbs_values.append(sum(log.carbs for log in logs))
        fat_values.append(sum(log.fat for log in logs))
        sugar_values.append(sum(log.sugar for log in logs))
        fiber_values.append(sum(log.fiber for log in logs))

    # Calculate streak
    streak = 0
    for i in range(30):
        day = today - timedelta(days=i)
        if day in days_dict:
            logs = days_dict[day]
        else:
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

    # Store in session for suggestions
    request.session['suggestion_calories'] = total_calories
    request.session['suggestion_macro_values'] = macro_values
    request.session['suggestion_streak'] = streak

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
            # Prepare bulk update
            entries_to_update = []
            for i in range(7):
                day = today - timedelta(days=i)
                entry, _ = DailyEntry.objects.get_or_create(user=request.user, date=day)
                entry.water = random.randint(0, 12)
                entries_to_update.append(entry)

            # Bulk update
            DailyEntry.objects.bulk_update(entries_to_update, ['water'])
            return redirect('water_detail')

        elif 'reset_water_data' in request.POST:
            # Bulk update with zero values
            days = [today - timedelta(days=i) for i in range(7)]
            entries = DailyEntry.objects.filter(user=user, date__in=days)
            for entry in entries:
                entry.water = 0
            DailyEntry.objects.bulk_update(entries, ['water'])
            return redirect('water_detail')

        elif 'reset_water' in request.POST:
            entry.water = 0
        else:
            water = int(request.POST.get('water', 0))
            entry.water += water
        entry.save()

    # Store in session for suggestions
    request.session['suggestion_water'] = entry.water

    # Get water data for past 7 days in one query
    days = [today - timedelta(days=i) for i in range(7)]
    entries = DailyEntry.objects.filter(user=user, date__in=days)
    entries_dict = {entry.date: entry for entry in entries}

    labels = []
    values = []
    for i in range(6, -1, -1):
        day = today - timedelta(days=i)
        labels.append(day.strftime('%a'))
        if day in entries_dict:
            values.append(entries_dict[day].water)
        else:
            values.append(0)

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
            # Prepare bulk update
            entries_to_update = []
            for i in range(7):
                day = today - timedelta(days=i)
                entry, _ = DailyEntry.objects.get_or_create(user=user, date=day)
                entry.sleep = random.randint(4, 10)
                entries_to_update.append(entry)

            # Bulk update
            DailyEntry.objects.bulk_update(entries_to_update, ['sleep'])
            return redirect('sleep_detail')

        elif 'reset_sleep_data' in request.POST:
            # Bulk update with zero values
            days = [today - timedelta(days=i) for i in range(7)]
            entries = DailyEntry.objects.filter(user=user, date__in=days)
            for entry in entries:
                entry.sleep = 0
            DailyEntry.objects.bulk_update(entries, ['sleep'])
            return redirect('sleep_detail')

        else:
            sleep = int(request.POST.get('sleep', 0))
            entry.sleep = sleep
            entry.save()
            return redirect('sleep_detail')

    # Store in session for suggestions
    request.session['suggestion_sleep'] = entry.sleep

    # Get sleep data for past 7 days in one query
    days = [today - timedelta(days=i) for i in range(7)]
    entries = DailyEntry.objects.filter(user=user, date__in=days)
    entries_dict = {entry.date: entry for entry in entries}

    labels = []
    values = []
    for i in range(6, -1, -1):
        day = today - timedelta(days=i)
        labels.append(day.strftime('%a'))
        if day in entries_dict:
            values.append(entries_dict[day].sleep)
        else:
            values.append(0)

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
    if not api_key:
        return JsonResponse({'error': 'API key not configured'}, status=500)

    url = f'https://api.nal.usda.gov/fdc/v1/foods/search'
    params = {
        'api_key': api_key,
        'query': query,
        'pageSize': 5,
    }

    try:
        res = requests.get(url, params=params)
        res.raise_for_status()  # Raises exception for 4XX/5XX responses
        data = res.json()
    except requests.exceptions.RequestException as e:
        return JsonResponse({'error': f'API request failed: {str(e)}'}, status=500)
    except ValueError:  # Handles JSON parsing errors
        return JsonResponse({'error': 'Invalid response from API'}, status=500)

    data = res.json()
    foods = []
    for item in data.get('foods', []):
        # Initialize all variables first
        desc = item.get('description', '')
        cals = protein = carbs = fat = sugar = fiber = 0
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

@login_required
def suggestion(request):
    # Get stored values from session
    ai_suggestions = generate_health_suggestion(
        calories=request.session.get('suggestion_calories'),
        sleep=request.session.get('suggestion_sleep'),
        water=request.session.get('suggestion_water'),
        streak=request.session.get('suggestion_streak'),
        macros=request.session.get('suggestion_macro_values')
    )
    return render(request, 'suggestions.html', {
        'suggestions': ai_suggestions,
    }) 