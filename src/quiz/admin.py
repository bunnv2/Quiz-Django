from django.contrib import admin

from .models import Question, Quiz, QuizResults

admin.site.register(Question)
admin.site.register(Quiz)
admin.site.register(QuizResults)
