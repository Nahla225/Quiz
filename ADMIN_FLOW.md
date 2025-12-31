# Admin Flow - Step by Step

## Quiz Creation Flow

```
START
  │
  ▼
┌─────────────────┐
│ Admin Login     │
│ (is_staff=True) │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Admin Panel     │
│ /manage/quizzes │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Click "Create   │
│ New Quiz"        │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Fill Quiz Form: │
│ - Title         │
│ - Description   │
│ - Duration      │
│ - Active Status │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Create Quiz     │
│ (Quiz Model)    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Redirect to     │
│ Add Questions   │
└─────────────────┘
```

## Question Creation Flow

```
START (From Quiz Created)
  │
  ▼
┌─────────────────┐
│ Add Questions   │
│ Page            │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Fill Question:  │
│ - Question Text │
│ - Order Number  │
│ - Choice 1      │
│ - Choice 2      │
│ - Choice 3      │
│ - Choice 4      │
│ - Mark Correct  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Validate:       │
│ - Text required │
│ - 4 choices     │
│ - 1 correct     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Create Question │
│ (Question Model)│
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Create Choices  │
│ (Choice Model)  │
│ - 4 records     │
│ - 1 is_correct  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Display in List │
│ (Can add more)  │
└─────────────────┘
```

## Viewing Submissions Flow

```
START
  │
  ▼
┌─────────────────┐
│ Admin Panel     │
│ Quiz List       │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Click           │
│ "Submissions"   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Query Database: │
│ - QuizAttempt   │
│   .filter(      │
│     quiz=quiz,  │
│     is_completed│
│     =True)      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Calculate Stats:│
│ - Total count   │
│ - Avg score     │
│ - Highest       │
│ - Lowest        │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Display:        │
│ - Statistics    │
│ - Student List  │
│ - Scores        │
│ - Times         │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Click "View     │
│ Details"        │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Query:          │
│ - QuizAttempt   │
│ - UserAnswer    │
│   .filter(      │
│     attempt=    │
│     attempt)    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Display:        │
│ - Student Info  │
│ - Score         │
│ - All Answers   │
│ - Correct/      │
│   Incorrect     │
└─────────────────┘
```

## Data Operations in Admin Flow

```
Admin Action              Database Operation
─────────────────────────────────────────────
Create Quiz          →    Quiz.objects.create()
                        - title, description
                        - duration, is_active

Add Question         →    Question.objects.create()
                        - quiz = current_quiz
                        - text, order
                        
                        Choice.objects.create() x4
                        - question = new_question
                        - text, is_correct

Edit Quiz            →    Quiz.objects.get(id)
                        - Update fields
                        - .save()

Delete Quiz          →    Quiz.objects.get(id)
                        - .delete() (cascades to
                          questions, choices,
                          attempts)

View Submissions     →    QuizAttempt.objects.filter(
                        - quiz = selected_quiz
                        - is_completed = True
                        )
                        - .order_by('-completed_at')

View Attempt Detail  →    QuizAttempt.objects.get(id)
                        UserAnswer.objects.filter(
                        - attempt = selected_attempt
                        )
                        - .order_by('question__order')
```

## Admin Access Control

```
Request → Check is_staff
           │
      ┌────┴────┐
      │         │
      ▼         ▼
   True      False
      │         │
      │         └──> Redirect Home
      │             + Error Message
      │
      ▼
   Allow Access
```

