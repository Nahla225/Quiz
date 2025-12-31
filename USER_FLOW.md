# User Flow - Step by Step

## Registration Flow

```
START
  │
  ▼
┌─────────────────┐
│ Visit Home Page │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Click Register  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Fill Form:      │
│ - Username      │
│ - Email         │
│ - Password      │
│ - Confirm Pass  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Validate Input │
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
    ▼         ▼
┌──────┐  ┌──────────┐
│Valid │  │ Invalid  │
└──┬───┘  └────┬─────┘
   │           │
   │           └──> Show Error
   │
   ▼
┌─────────────────┐
│ Create User     │
│ (User Model)    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Redirect Login  │
└─────────────────┘
```

## Quiz Taking Flow

```
START
  │
  ▼
┌─────────────────┐
│ Login           │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ View Quiz List  │
│ (Active Quizzes)│
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Select Quiz     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Check Existing  │
│ Active Attempt  │
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
    ▼         ▼
┌──────┐  ┌──────────┐
│Exists│  │  New     │
└──┬───┘  └────┬─────┘
   │           │
   │           ▼
   │    ┌──────────────┐
   │    │ Create       │
   │    │ QuizAttempt  │
   │    └──────┬───────┘
   │           │
   └───────────┘
         │
         ▼
┌─────────────────┐
│ Display Quiz    │
│ - Questions     │
│ - Choices       │
│ - Timer         │
└────────┬────────┘
         │
         │
    ┌────┴────┐
    │         │
    ▼         ▼
┌──────┐  ┌──────────┐
│Timer │  │ Submit   │
│Expire│  │ Answers  │
└──┬───┘  └────┬─────┘
   │           │
   │           ▼
   │    ┌──────────────┐
   │    │ Save Answers │
   │    │ (UserAnswer) │
   │    └──────┬───────┘
   │           │
   └───────────┘
         │
         ▼
┌─────────────────┐
│ Calculate Score │
│ - Check Answers │
│ - Count Correct │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Update Attempt  │
│ - score         │
│ - completed_at  │
│ - is_completed  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Show Results    │
│ - Score         │
│ - Percentage    │
│ - Review        │
└─────────────────┘
```

## Data Storage During Quiz

```
User Action              Database Operation
─────────────────────────────────────────────
Start Quiz          →    QuizAttempt.created
                        - user = current_user
                        - quiz = selected_quiz
                        - started_at = now()
                        - is_completed = False

Select Answer       →    UserAnswer.created (if new)
                        - attempt = current_attempt
                        - question = current_question
                        - selected_choice = chosen
                        - is_correct = check_choice()

Submit Quiz         →    For each question:
                        - UserAnswer.update_or_create()
                        - Check is_correct
                        - Increment score if correct
                        
                        QuizAttempt.update:
                        - score = calculated_score
                        - completed_at = now()
                        - is_completed = True
```

