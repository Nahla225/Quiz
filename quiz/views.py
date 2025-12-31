from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from .models import Quiz, Question, Choice, QuizAttempt, UserAnswer


def home(request):
    return render(request, 'quiz/home.html')


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if password != password2:
            messages.error(request, 'Passwords do not match!')
            return render(request, 'quiz/register.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists!')
            return render(request, 'quiz/register.html')

        user = User.objects.create_user(username=username, email=email, password=password)
        messages.success(request, 'Registration successful! Please login.')
        return redirect('login')

    return render(request, 'quiz/register.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('quiz_list')
        else:
            messages.error(request, 'Invalid username or password!')
    return render(request, 'quiz/login.html')


def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully!')
    return redirect('home')


@login_required
def quiz_list(request):
    quizzes = Quiz.objects.filter(is_active=True)
    return render(request, 'quiz/quiz_list.html', {'quizzes': quizzes})


@login_required
def take_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id, is_active=True)
    
    # Check if user already has an active attempt
    active_attempt = QuizAttempt.objects.filter(
        user=request.user,
        quiz=quiz,
        is_completed=False
    ).first()

    if active_attempt:
        # Check if time has expired
        time_elapsed = timezone.now() - active_attempt.started_at
        if time_elapsed > timedelta(minutes=quiz.duration):
            active_attempt.is_completed = True
            active_attempt.completed_at = timezone.now()
            active_attempt.save()
            return redirect('quiz_result', attempt_id=active_attempt.id)
        attempt = active_attempt
    else:
        # Create new attempt
        attempt = QuizAttempt.objects.create(
            user=request.user,
            quiz=quiz,
            total_questions=quiz.questions.count()
        )

    if request.method == 'POST':
        # Reset score and save answers
        attempt.score = 0
        for question in quiz.questions.all():
            choice_id = request.POST.get(f'question_{question.id}')
            if choice_id:
                selected_choice = Choice.objects.get(id=choice_id)
                is_correct = selected_choice.is_correct
                
                UserAnswer.objects.update_or_create(
                    attempt=attempt,
                    question=question,
                    defaults={
                        'selected_choice': selected_choice,
                        'is_correct': is_correct
                    }
                )
                
                if is_correct:
                    attempt.score += 1

        attempt.is_completed = True
        attempt.completed_at = timezone.now()
        attempt.save()
        return redirect('quiz_result', attempt_id=attempt.id)

    # Get questions with choices
    questions = quiz.questions.all().order_by('order')
    question_data = []
    for question in questions:
        choices = question.choices.all()
        # Check if user already answered this question
        user_answer = UserAnswer.objects.filter(attempt=attempt, question=question).first()
        question_data.append({
            'question': question,
            'choices': choices,
            'user_answer': user_answer
        })

    # Calculate remaining time
    time_elapsed = timezone.now() - attempt.started_at
    remaining_seconds = (quiz.duration * 60) - int(time_elapsed.total_seconds())
    if remaining_seconds < 0:
        remaining_seconds = 0

    return render(request, 'quiz/take_quiz.html', {
        'quiz': quiz,
        'attempt': attempt,
        'question_data': question_data,
        'remaining_seconds': remaining_seconds
    })


@login_required
def quiz_result(request, attempt_id):
    attempt = get_object_or_404(QuizAttempt, id=attempt_id, user=request.user)
    
    if not attempt.is_completed:
        return redirect('take_quiz', quiz_id=attempt.quiz.id)

    # Get all answers
    user_answers = UserAnswer.objects.filter(attempt=attempt)
    answer_data = []
    for user_answer in user_answers:
        correct_choice = user_answer.question.choices.filter(is_correct=True).first()
        answer_data.append({
            'question': user_answer.question,
            'user_choice': user_answer.selected_choice,
            'correct_choice': correct_choice,
            'is_correct': user_answer.is_correct
        })

    return render(request, 'quiz/quiz_result.html', {
        'attempt': attempt,
        'answer_data': answer_data
    })


@login_required
def profile(request):
    attempts = QuizAttempt.objects.filter(user=request.user, is_completed=True).order_by('-completed_at')
    return render(request, 'quiz/profile.html', {'attempts': attempts})


# Admin Views
@login_required
def admin_quiz_list(request):
    if not request.user.is_staff:
        messages.error(request, 'Access denied. Admin only.')
        return redirect('home')
    
    quizzes = Quiz.objects.all().order_by('-created_at')
    return render(request, 'quiz/admin_quiz_list.html', {'quizzes': quizzes})


@login_required
def admin_create_quiz(request):
    if not request.user.is_staff:
        messages.error(request, 'Access denied. Admin only.')
        return redirect('home')
    
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description', '')
        duration = request.POST.get('duration')
        is_active = request.POST.get('is_active') == 'on'
        
        if title and duration:
            quiz = Quiz.objects.create(
                title=title,
                description=description,
                duration=int(duration),
                is_active=is_active
            )
            messages.success(request, f'Quiz "{title}" created successfully!')
            return redirect('admin_add_questions', quiz_id=quiz.id)
        else:
            messages.error(request, 'Please fill all required fields!')
    
    return render(request, 'quiz/admin_create_quiz.html')


@login_required
def admin_edit_quiz(request, quiz_id):
    if not request.user.is_staff:
        messages.error(request, 'Access denied. Admin only.')
        return redirect('home')
    
    quiz = get_object_or_404(Quiz, id=quiz_id)
    
    if request.method == 'POST':
        quiz.title = request.POST.get('title')
        quiz.description = request.POST.get('description', '')
        quiz.duration = int(request.POST.get('duration'))
        quiz.is_active = request.POST.get('is_active') == 'on'
        quiz.save()
        messages.success(request, 'Quiz updated successfully!')
        return redirect('admin_quiz_list')
    
    return render(request, 'quiz/admin_edit_quiz.html', {'quiz': quiz})


@login_required
def admin_delete_quiz(request, quiz_id):
    if not request.user.is_staff:
        messages.error(request, 'Access denied. Admin only.')
        return redirect('home')
    
    quiz = get_object_or_404(Quiz, id=quiz_id)
    if request.method == 'POST':
        quiz.delete()
        messages.success(request, 'Quiz deleted successfully!')
        return redirect('admin_quiz_list')
    
    return render(request, 'quiz/admin_delete_quiz.html', {'quiz': quiz})


@login_required
def admin_add_questions(request, quiz_id):
    if not request.user.is_staff:
        messages.error(request, 'Access denied. Admin only.')
        return redirect('home')
    
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.questions.all().order_by('order')
    
    if request.method == 'POST':
        question_text = request.POST.get('question_text')
        order = request.POST.get('order', 0)
        
        if question_text:
            question = Question.objects.create(
                quiz=quiz,
                text=question_text,
                order=int(order) if order else 0
            )
            
            # Add choices
            for i in range(1, 5):  # 4 choices
                choice_text = request.POST.get(f'choice_{i}')
                is_correct = request.POST.get(f'correct_choice') == str(i)
                
                if choice_text:
                    Choice.objects.create(
                        question=question,
                        text=choice_text,
                        is_correct=is_correct
                    )
            
            messages.success(request, 'Question added successfully!')
            return redirect('admin_add_questions', quiz_id=quiz.id)
        else:
            messages.error(request, 'Please enter question text!')
    
    return render(request, 'quiz/admin_add_questions.html', {
        'quiz': quiz,
        'questions': questions
    })


@login_required
def admin_edit_question(request, question_id):
    if not request.user.is_staff:
        messages.error(request, 'Access denied. Admin only.')
        return redirect('home')
    
    question = get_object_or_404(Question, id=question_id)
    choices = list(question.choices.all())
    
    if request.method == 'POST':
        question.text = request.POST.get('question_text')
        question.order = int(request.POST.get('order', 0))
        question.save()
        
        # Update or create choices
        for i in range(1, 5):
            choice_text = request.POST.get(f'choice_{i}')
            is_correct = request.POST.get(f'correct_choice') == str(i)
            
            if i <= len(choices):
                # Update existing choice
                choice = choices[i-1]
                choice.text = choice_text
                choice.is_correct = is_correct
                choice.save()
            else:
                # Create new choice
                if choice_text:
                    Choice.objects.create(
                        question=question,
                        text=choice_text,
                        is_correct=is_correct
                    )
        
        messages.success(request, 'Question updated successfully!')
        return redirect('admin_add_questions', quiz_id=question.quiz.id)
    
    # Pad choices to 4 if less
    while len(choices) < 4:
        new_choice = Choice.objects.create(question=question, text='', is_correct=False)
        choices.append(new_choice)
    
    return render(request, 'quiz/admin_edit_question.html', {
        'question': question,
        'choices': choices
    })


@login_required
def admin_delete_question(request, question_id):
    if not request.user.is_staff:
        messages.error(request, 'Access denied. Admin only.')
        return redirect('home')
    
    question = get_object_or_404(Question, id=question_id)
    quiz_id = question.quiz.id
    
    if request.method == 'POST':
        question.delete()
        messages.success(request, 'Question deleted successfully!')
        return redirect('admin_add_questions', quiz_id=quiz_id)
    
    return render(request, 'quiz/admin_delete_question.html', {'question': question})


@login_required
def admin_quiz_submissions(request, quiz_id):
    if not request.user.is_staff:
        messages.error(request, 'Access denied. Admin only.')
        return redirect('home')
    
    quiz = get_object_or_404(Quiz, id=quiz_id)
    attempts = QuizAttempt.objects.filter(quiz=quiz, is_completed=True).order_by('-completed_at')
    
    # Calculate statistics
    total_attempts = attempts.count()
    if total_attempts > 0:
        avg_score = sum(attempt.score for attempt in attempts) / total_attempts
        avg_percentage = sum(attempt.get_percentage() for attempt in attempts) / total_attempts
        highest_score = max(attempt.score for attempt in attempts)
        lowest_score = min(attempt.score for attempt in attempts)
    else:
        avg_score = 0
        avg_percentage = 0
        highest_score = 0
        lowest_score = 0
    
    # Calculate time taken for each attempt
    attempt_data = []
    for attempt in attempts:
        time_taken = None
        if attempt.completed_at and attempt.started_at:
            time_taken = (attempt.completed_at - attempt.started_at).total_seconds()
        attempt_data.append({
            'attempt': attempt,
            'time_taken': int(time_taken) if time_taken else None
        })
    
    return render(request, 'quiz/admin_quiz_submissions.html', {
        'quiz': quiz,
        'attempt_data': attempt_data,
        'total_attempts': total_attempts,
        'avg_score': round(avg_score, 2),
        'avg_percentage': round(avg_percentage, 2),
        'highest_score': highest_score,
        'lowest_score': lowest_score,
    })


@login_required
def admin_attempt_detail(request, attempt_id):
    if not request.user.is_staff:
        messages.error(request, 'Access denied. Admin only.')
        return redirect('home')
    
    attempt = get_object_or_404(QuizAttempt, id=attempt_id)
    
    # Calculate time taken
    time_taken_seconds = None
    time_taken_minutes = None
    if attempt.completed_at and attempt.started_at:
        time_taken_seconds = int((attempt.completed_at - attempt.started_at).total_seconds())
        time_taken_minutes = round(time_taken_seconds / 60, 1)
    
    # Get all answers
    user_answers = UserAnswer.objects.filter(attempt=attempt).order_by('question__order')
    answer_data = []
    for user_answer in user_answers:
        correct_choice = user_answer.question.choices.filter(is_correct=True).first()
        answer_data.append({
            'question': user_answer.question,
            'user_choice': user_answer.selected_choice,
            'correct_choice': correct_choice,
            'is_correct': user_answer.is_correct
        })
    
    return render(request, 'quiz/admin_attempt_detail.html', {
        'attempt': attempt,
        'answer_data': answer_data,
        'time_taken_seconds': time_taken_seconds,
        'time_taken_minutes': time_taken_minutes
    })
