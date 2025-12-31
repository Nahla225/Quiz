# Online Quiz System

A web-based Django application for conducting online quizzes with automatic evaluation and performance tracking.

## Features

- User registration and authentication
- Multiple choice quizzes with time limits
- Instant results and feedback
- Performance history tracking
- Admin panel for managing quizzes and questions
- User profiles with quiz history

## Setup Instructions

1. Install dependencies (if using uv):
   ```bash
   uv sync
   ```

2. Create a superuser for admin access:
   ```bash
   python manage.py createsuperuser
   ```

3. Run migrations (if not already done):
   ```bash
   python manage.py migrate
   ```

4. Start the development server:
   ```bash
   python manage.py runserver
   ```

5. Access the application:
   - Home: http://127.0.0.1:8000/
   - Admin: http://127.0.0.1:8000/admin/

## Usage

1. **Register/Login**: Create an account or login with existing credentials
2. **Browse Quizzes**: View available quizzes from the quiz list
3. **Take Quiz**: Start a quiz and answer questions within the time limit
4. **View Results**: See your score and review correct/incorrect answers
5. **Profile**: Check your quiz history and performance

## Admin Panel

Use the admin panel to:
- Create and manage quizzes
- Add questions and choices
- View student attempts and performance
- Activate/deactivate quizzes

## Project Structure

- `quiz/` - Main application
  - `models.py` - Database models (Quiz, Question, Choice, QuizAttempt, UserAnswer)
  - `views.py` - View functions
  - `templates/quiz/` - HTML templates
  - `admin.py` - Admin configuration
- `config/` - Django project settings

