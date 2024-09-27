from django.contrib import admin
from fitApp.models import *
# Register your models here.


class WorkoutAdmin(admin.ModelAdmin):
    pass

admin.site.register(Workout, WorkoutAdmin)