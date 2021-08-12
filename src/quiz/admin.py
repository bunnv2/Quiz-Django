from django.contrib import admin
from django.contrib.auth.models import Group

from .models import Question, Quiz, QuizResults

admin.site.register(QuizResults)
admin.site.unregister(Group)
admin.site.site_header = "Panel Administracyjny Quizz"


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ("title", "time", "required_score_to_pass", "is_published", "author")
    ordering = ("author",)
    search_fields = ("title",)
    list_filter = ("author",)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("question", "quiz", "correct_answer")
    ordering = ("quiz",)
    list_filter = ("quiz",)
