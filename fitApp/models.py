from django.db import models
from django.contrib.auth.models import User

class BaseModel(models.Model):
    STATUS_CHOICES = (
        ("Active", 'active'),
        ("In-Active", 'inactive'),
    )
    
    id = models.AutoField(primary_key=True, db_index=True)
    status = models.CharField(choices=STATUS_CHOICES, default="Active", max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class ExerciseModel(BaseModel):
    exercise_name = models.CharField(max_length=500, verbose_name="Exercise Name")
    exercise_code = models.CharField(max_length=500, verbose_name="Exercise Code")

    def __str__(self):
        return self.exercise_name

class Workout(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_workouts')
    exercises = models.ManyToManyField(ExerciseModel, related_name='workouts')  # Changed to ManyToManyField
    date = models.DateField()
    comments = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Workout on {self.date} by {self.user.username}"
 