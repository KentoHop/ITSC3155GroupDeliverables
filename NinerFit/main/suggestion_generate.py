import os
from openai import OpenAI
from django.conf import settings

#set open AI API
your_api = '' #insert own api key here
client = OpenAI(api_key=your_api)

def generate_health_suggestion(calories, sleep, water, streak, macros):
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

    try:
        response = client.chat.completions.create(
            model="gpt-4.0-mini",
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

        return suggestions

    except Exception as e:
        return {
            "Calories and Nutrition": "Try to stay on track with your macros today!",
            "Sleep": "Aim for a more consistent sleep schedule.",
            "Hydration": "Keep sipping water throughout the day.",
            "Motivation": "You're doing great — stay consistent!"
        }