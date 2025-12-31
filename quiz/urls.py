from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('quizzes/', views.quiz_list, name='quiz_list'),
    path('quiz/<int:quiz_id>/', views.take_quiz, name='take_quiz'),
    path('result/<int:attempt_id>/', views.quiz_result, name='quiz_result'),
    path('profile/', views.profile, name='profile'),
    # Admin URLs
    path('manage/quizzes/', views.admin_quiz_list, name='admin_quiz_list'),
    path('manage/quiz/create/', views.admin_create_quiz, name='admin_create_quiz'),
    path('manage/quiz/<int:quiz_id>/edit/', views.admin_edit_quiz, name='admin_edit_quiz'),
    path('manage/quiz/<int:quiz_id>/delete/', views.admin_delete_quiz, name='admin_delete_quiz'),
    path('manage/quiz/<int:quiz_id>/questions/', views.admin_add_questions, name='admin_add_questions'),
    path('manage/quiz/<int:quiz_id>/submissions/', views.admin_quiz_submissions, name='admin_quiz_submissions'),
    path('manage/question/<int:question_id>/edit/', views.admin_edit_question, name='admin_edit_question'),
    path('manage/question/<int:question_id>/delete/', views.admin_delete_question, name='admin_delete_question'),
    path('manage/attempt/<int:attempt_id>/', views.admin_attempt_detail, name='admin_attempt_detail'),
]

