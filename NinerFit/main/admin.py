from django.contrib import admin
from .models import DailyEntry, FoodLog

admin.site.register(DailyEntry)
admin.site.register(FoodLog)
