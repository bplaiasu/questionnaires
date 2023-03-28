from django.db import models
from django.contrib.auth.models import User
import uuid
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    simulation_exam_a = models.BooleanField(default=False)
    sim_ex_a_questions = models.IntegerField(default=1, blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Categories"


class Question(models.Model):
    text = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created = models.DateField(auto_now_add=True)
    photo = models.ImageField(upload_to='photos/%Y/%m/', blank=True)

    def __str__(self):
        return self.text

    def get_answers(self):
        return self.answer_set.all()

    def get_next(self):
        next = Question.objects.filter(id__gt=self.id).order_by('id').first()
        if next:
            return next

    def get_prev(self):
        prev = Question.objects.filter(id__lt=self.id).order_by('-id').first()
        if prev:
            return prev


class Answer(models.Model):
    text = models.CharField(max_length=255)
    correct = models.BooleanField(default=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Question: {self.question.text} | Answer: {self.text} | Correct: {self.correct}"


# User = get_user_model()
class UserDashboard(models.Model):
    correct_answers = models.IntegerField()     # save in db number of correct answers
    incorrect_answers = models.IntegerField()   # save in db number of incorrect answers
    # surveys = models.IntegerField(default=0)    # save in db number of surveys that user responds
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    survey = models.UUIDField(blank=False, default=uuid.uuid4)  # generate new hash on every save
    survey_date = models.DateTimeField(default=timezone.now)


class UserDashboardDetails(models.Model):
    survey = models.ForeignKey(UserDashboard, on_delete=models.DO_NOTHING)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    correct_answer = models.IntegerField()
    user_selected_answer = models.IntegerField()
    inserted = models.DateTimeField(default=timezone.now)
