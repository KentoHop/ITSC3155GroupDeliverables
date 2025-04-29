from django.db import models
from django.contrib.auth.models import User
from datetime import date
from django.utils import timezone

class DailyEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(default=date.today)
    calories = models.IntegerField(default=0)
    water = models.IntegerField(default=0)
    sleep = models.IntegerField(default=0)

    class Meta:
        unique_together = ['user', 'date']

    def __str__(self):
        return f"{self.user.username} - {self.date}"
    

class FoodLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    food = models.CharField(max_length=100)
    calories = models.PositiveIntegerField()
    meal = models.CharField(max_length=20, choices=[
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('dinner', 'Dinner'),
        ('snack', 'Snack'),
    ])
    timestamp = models.DateTimeField(auto_now_add=True)

    protein = models.FloatField(default=0)
    carbs = models.FloatField(default=0)
    fat = models.FloatField(default=0)
    sugar = models.FloatField(default=0)
    fiber = models.FloatField(default=0)

    def __str__(self):
        return f"{self.food} - {self.calories} kcal"
    
class DailyLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    calories = models.PositiveIntegerField()
    water_cups = models.PositiveIntegerField()
    sleep_hours = models.DecimalField(max_digits=4, decimal_places=1)

    def __str__(self):
        return f"{self.user.username} - {self.date}"