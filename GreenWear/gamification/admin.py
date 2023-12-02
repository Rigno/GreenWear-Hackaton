from django.contrib import admin
import nested_admin

from .models import Quiz, Question, Answer


class AnswerInline(nested_admin.NestedStackedInline):
    model = Answer
    max_num = 4

class QuestionInline(nested_admin.NestedStackedInline):
    model = Question
    inlines = [AnswerInline]
    max_num = 5

@admin.register(Quiz)
class QuizAdmin(nested_admin.NestedModelAdmin):
    inlines = [QuestionInline]
