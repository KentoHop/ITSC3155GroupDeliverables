import os
from openai import OpenAI
from django.conf import settings

#set open AI API
your_api = '' #insert own api key here
client = OpenAI(api_key=your_api)

def generate_health_suggestion(calories, sleep, water, streak, macros):
    try:
        prompt = (
            f"""
                You are a helpful fitness assistant. Based on the following user health data, generate FOUR very specific suggestions — each in one sentence — categorized as:

                1. Calories and Nutrition
                2. Sleep
                3. Hydration
                4. Motivation

                Health Data:
                - Calories: {calories}
                - Sleep: {sleep} hours
                - Water: {water} cups
                - Streak: {streak} days of hitting calorie goal
                - Macros (in grams): Protein: {macros[0]}, Carbs: {macros[1]}, Fat: {macros[2]}, Sugar: {macros[3]}, Fiber: {macros[4]}

                Each suggestion should be personalized and helpful — do not repeat the numbers, but give actionable feedback. Return the output as a list like:

                Calories and Nutrition: ...
                Sleep: ...
                Hydration: ...
                Motivation: ...
                """
        )
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300,
            temperature=0.8,
        )
        suggestions_raw = response.choices[0].message.content.strip()
        suggestions = {}

        for line in suggestions_raw.split("\n"):
            if ":" in line:
                key, value = line.split(":", 1)
                suggestions[key.strip()] = value.strip()
    except Exception as e:
        suggestions = {}
        if calories is not None:
            if calories < 1200:
                suggestions.update({"Calories and Nutrition": "Try to increase your calorie intake with nutritious foods."})
            elif calories > 2200:
                suggestions.update({"Calories and Nutrition": "Consider reducing your calorie intake slightly."})
        if sleep is not None:
            if sleep < 7:
                suggestions.update({"Sleep": "Aim for 7-9 hours of sleep for optimal health."})
            else:
                suggestions.update({"Sleep": "Great job maintaining a healthy sleep schedule!"})
        if water is not None:
            if water < 8:
                suggestions.update({"Hydration": f"Try to drink {8-water} more glasses of water today."})
            else:
                suggestions.update({"Hydration": "You're doing great with hydration!"})
        if streak is not None and streak > 3:
            suggestions.update({"Motivation": f"Amazing! You've maintained your goals for {streak} days."})
        if macros is not None and all(v is not None for v in macros):
            protein, carbs, fat, sugar, fiber = macros
            if protein < 50:
                suggestions.update({"Calories and Nutrition": "Consider adding more protein to your diet."})
            if fiber < 25:
                suggestions.update({"Calories and Nutrition": "Try to include more fiber-rich foods in your meals."})
    
    return suggestions