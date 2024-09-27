from django.db import models
from django.contrib.auth.models import User

class BaseModel(models.Model):
    STATUS_CHOICES = (
        (1, "Active"),
        (0, "In-Active"),
    )
    
    id = models.AutoField(primary_key=True, db_index=True)
    status = models.CharField(choices=STATUS_CHOICES, default=1, max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class ExerciseModel(BaseModel):
    exercise_name = models.CharField(max_length=500, verbose_name="Exercise Name")
    exercise_code = models.CharField(max_length=500, verbose_name="Exercise Code")

    def __str__(self):
        return self.exercise_name

class Workout(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_workouts')
    exercises = models.ManyToManyField(ExerciseModel, related_name='workouts', blank=True)  
    workout_date = models.DateField(auto_now_add=True)
    comments = models.TextField(blank=True, null=True)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"Workout on {self.workout_date} by {self.user.username}"
 