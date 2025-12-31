from django.contrib import admin
from .models import Quiz, Question, Choice, QuizAttempt, UserAnswer


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 4


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ['title', 'duration', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    inlines = [QuestionInline]


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['text', 'quiz', 'order']
    list_filter = ['quiz']
    inlines = [ChoiceInline]


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ['text', 'question', 'is_correct']
    list_filter = ['is_correct', 'question__quiz']


@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ['user', 'quiz', 'score', 'total_questions', 'is_completed', 'started_at']
    list_filter = ['is_completed', 'quiz', 'started_at']
    readonly_fields = ['started_at', 'completed_at']


@admin.register(UserAnswer)
class UserAnswerAdmin(admin.ModelAdmin):
    list_display = ['attempt', 'question', 'selected_choice', 'is_correct']
    list_filter = ['is_correct', 'attempt__quiz']
