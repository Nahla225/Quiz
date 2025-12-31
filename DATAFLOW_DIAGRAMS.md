# Online Quiz System - Dataflow Diagrams

## User Dataflow Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         USER DATAFLOW                                    │
└─────────────────────────────────────────────────────────────────────────┘

┌──────────────┐
│   Home Page  │
│   (/)        │
└──────┬───────┘
       │
       ├─────────────────┐
       │                 │
       ▼                 ▼
┌──────────────┐  ┌──────────────┐
│   Register   │  │    Login     │
│  (/register) │  │   (/login)   │
└──────┬───────┘  └──────┬───────┘
       │                 │
       │                 │
       └────────┬────────┘
                │
                ▼
        ┌───────────────┐
        │ Authenticated │
        │    User       │
        └───────┬───────┘
                │
                ▼
        ┌───────────────┐
        │  Quiz List    │
        │  (/quizzes)   │
        └───────┬───────┘
                │
                ▼
        ┌───────────────┐
        │  Select Quiz  │
        │  (Click Quiz) │
        └───────┬───────┘
                │
                ▼
        ┌───────────────┐
        │  Take Quiz    │
        │(/quiz/<id>/)  │
        │               │
        │  - Timer      │
        │  - Questions  │
        │  - Choices    │
        └───────┬───────┘
                │
                │ Submit Answers
                ▼
        ┌───────────────┐
        │ Save Answers  │
        │               │
        │  - UserAnswer │
        │  - Calculate │
        │    Score      │
        │  - Mark as    │
        │    Completed  │
        └───────┬───────┘
                │
                ▼
        ┌───────────────┐
        │ Quiz Result   │
        │(/result/<id>) │
        │               │
        │  - Score      │
        │  - Percentage │
        │  - Review     │
        │    Answers    │
        └───────┬───────┘
                │
                ▼
        ┌───────────────┐
        │   Profile     │
        │  (/profile)   │
        │               │
        │  - Quiz       │
        │    History    │
        │  - All Scores │
        └───────────────┘
```

### User Data Flow Steps:

1. **Registration/Login**
   - User enters credentials
   - System creates/authenticates user
   - User session created

2. **Quiz Selection**
   - User views available quizzes
   - System displays active quizzes
   - User selects a quiz

3. **Taking Quiz**
   - System creates QuizAttempt record
   - Timer starts
   - User answers questions
   - System saves answers as UserAnswer records

4. **Result Processing**
   - System calculates score
   - Compares answers with correct choices
   - Updates QuizAttempt with score
   - Marks attempt as completed

5. **Viewing Results**
   - System displays score and percentage
   - Shows correct/incorrect answers
   - Saves to user's profile history

---

## Admin Dataflow Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        ADMIN DATAFLOW                                   │
└─────────────────────────────────────────────────────────────────────────┘

┌──────────────┐
│   Home Page  │
│   (/)        │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│    Login     │
│   (/login)   │
└──────┬───────┘
       │
       │ (Staff User)
       ▼
┌──────────────┐
│ Admin Panel  │
│(/manage/     │
│ quizzes/)    │
└──────┬───────┘
       │
       ├──────────────────┬──────────────────┬──────────────────┐
       │                  │                  │                  │
       ▼                  ▼                  ▼                  ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│ Create Quiz  │  │  Edit Quiz   │  │ Delete Quiz  │  │ View Quiz    │
│(/manage/quiz │  │(/manage/quiz │  │(/manage/quiz │  │ Submissions  │
│ /create/)    │  │/<id>/edit/) │  │/<id>/delete)│  │(/manage/quiz │
└──────┬───────┘  └──────────────┘  └──────────────┘  │/<id>/       │
       │                                               │submissions/)│
       │                                               └──────┬───────┘
       │                                                      │
       ▼                                                      │
┌──────────────┐                                             │
│ Quiz Created │                                             │
│              │                                             │
│ - Title      │                                             │
│ - Duration   │                                             │
│ - Status     │                                             │
└──────┬───────┘                                             │
       │                                                      │
       ▼                                                      │
┌──────────────┐                                             │
│ Add Questions│                                             │
│(/manage/quiz │                                             │
│/<id>/        │                                             │
│questions/)   │                                             │
└──────┬───────┘                                             │
       │                                                      │
       ├──────────────────┬──────────────────┐              │
       │                  │                  │              │
       ▼                  ▼                  ▼              │
┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│ Add Question │  │ Edit Question│  │Delete Question│       │
│              │  │(/manage/     │  │(/manage/     │       │
│ - Text       │  │question/    │  │question/     │       │
│ - Order      │  │<id>/edit/)  │  │<id>/delete/) │       │
│ - 4 Choices  │  └──────────────┘  └──────────────┘       │
│ - Mark       │                                            │
│   Correct    │                                            │
└──────┬───────┘                                            │
       │                                                     │
       ▼                                                     │
┌──────────────┐                                            │
│ Question      │                                            │
│ Saved        │                                            │
│              │                                            │
│ - Question   │                                            │
│   Record     │                                            │
│ - Choice     │                                            │
│   Records    │                                            │
└──────────────┘                                            │
                                                             │
                                                             ▼
                                                    ┌──────────────┐
                                                    │ View All     │
                                                    │ Submissions  │
                                                    │              │
                                                    │ - Statistics │
                                                    │ - Student    │
                                                    │   List       │
                                                    │ - Scores     │
                                                    └──────┬───────┘
                                                           │
                                                           ▼
                                                  ┌──────────────┐
                                                  │ View Attempt │
                                                  │ Details      │
                                                  │(/manage/     │
                                                  │attempt/<id>/)│
                                                  │              │
                                                  │ - Student    │
                                                  │   Info       │
                                                  │ - Score      │
                                                  │ - All Answers│
                                                  │ - Correct/   │
                                                  │   Incorrect  │
                                                  └──────────────┘
```

### Admin Data Flow Steps:

1. **Quiz Management**
   - Admin creates quiz (Quiz model)
   - Sets title, description, duration, status
   - Quiz saved to database

2. **Question Management**
   - Admin adds questions to quiz (Question model)
   - Creates 4 choices per question (Choice model)
   - Marks one choice as correct
   - Questions linked to quiz via ForeignKey

3. **Viewing Submissions**
   - Admin views all completed QuizAttempt records
   - System calculates statistics:
     - Total submissions
     - Average score
     - Highest/Lowest scores
   - Displays student list with scores

4. **Viewing Attempt Details**
   - Admin selects a specific attempt
   - System retrieves:
     - QuizAttempt record
     - All UserAnswer records for that attempt
     - Compares with correct answers
   - Displays detailed review

---

## Database Models Flow

```
┌─────────────────────────────────────────────────────────────────────────┐
│                      DATABASE MODELS RELATIONSHIP                        │
└─────────────────────────────────────────────────────────────────────────┘

                    ┌──────────┐
                    │   User   │
                    │ (Django) │
                    └────┬─────┘
                         │
                         │ (1:N)
                         │
        ┌────────────────┴────────────────┐
        │                                 │
        ▼                                 ▼
┌───────────────┐              ┌───────────────┐
│  QuizAttempt  │              │     Quiz       │
│               │              │                │
│ - user        │              │ - title        │
│ - quiz        │              │ - duration    │
│ - score       │              │ - is_active    │
│ - started_at  │              └───────┬────────┘
│ - completed_at│                       │
└───────┬───────┘                       │ (1:N)
        │                               │
        │ (1:N)                        ▼
        │                      ┌───────────────┐
        │                      │   Question   │
        │                      │               │
        │                      │ - quiz        │
        │                      │ - text        │
        │                      │ - order      │
        │                      └───────┬───────┘
        │                              │
        │                              │ (1:N)
        │                              │
        │                              ▼
        │                      ┌───────────────┐
        │                      │    Choice    │
        │                      │               │
        │                      │ - question   │
        │                      │ - text        │
        │                      │ - is_correct  │
        │                      └───────┬───────┘
        │                              │
        │                              │
        │                              │
        ▼                              │
┌───────────────┐                      │
│  UserAnswer   │                      │
│               │                      │
│ - attempt     │                      │
│ - question    │                      │
│ - selected_   │                      │
│   choice      │──────────────────────┘
│ - is_correct  │
└───────────────┘
```

### Model Relationships:

1. **User → QuizAttempt** (One-to-Many)
   - One user can have multiple quiz attempts

2. **Quiz → QuizAttempt** (One-to-Many)
   - One quiz can have multiple attempts by different users

3. **Quiz → Question** (One-to-Many)
   - One quiz contains multiple questions

4. **Question → Choice** (One-to-Many)
   - One question has multiple choices (typically 4)

5. **QuizAttempt → UserAnswer** (One-to-Many)
   - One attempt contains multiple user answers

6. **Question → UserAnswer** (One-to-Many)
   - One question can be answered in multiple attempts

7. **Choice → UserAnswer** (One-to-Many)
   - One choice can be selected in multiple answers

---

## Complete System Flow

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         COMPLETE SYSTEM FLOW                            │
└─────────────────────────────────────────────────────────────────────────┘

ADMIN SIDE                          USER SIDE
──────────                          ──────────

1. Create Quiz                      1. Register/Login
   └─> Quiz Model                       └─> User Session

2. Add Questions                     2. View Quiz List
   └─> Question Model                    └─> Filter Active Quizzes
   └─> Choice Model

3. Activate Quiz                     3. Start Quiz
   └─> is_active = True                  └─> Create QuizAttempt
                                          └─> Start Timer

                                      4. Answer Questions
                                         └─> Create UserAnswer
                                         └─> Check is_correct

                                      5. Submit Quiz
                                         └─> Calculate Score
                                         └─> Update QuizAttempt
                                         └─> Mark Completed

                                      6. View Results
                                         └─> Display Score
                                         └─> Show Review

                                      7. View Profile
                                         └─> List All Attempts

4. View Submissions
   └─> Query QuizAttempt
   └─> Calculate Statistics

5. View Attempt Details
   └─> Query UserAnswer
   └─> Compare with Choices
   └─> Display Review
```

---

## Key Data Operations

### User Operations:
- **CREATE**: QuizAttempt, UserAnswer
- **READ**: Quiz (active), QuizAttempt (own), UserAnswer (own)
- **UPDATE**: QuizAttempt (on submit)
- **DELETE**: None (users cannot delete)

### Admin Operations:
- **CREATE**: Quiz, Question, Choice
- **READ**: All models (Quiz, Question, Choice, QuizAttempt, UserAnswer)
- **UPDATE**: Quiz, Question, Choice, QuizAttempt status
- **DELETE**: Quiz, Question, Choice

---

## Data Validation Points

1. **User Registration**: Username uniqueness, password match
2. **Quiz Creation**: Title required, duration > 0
3. **Question Creation**: Text required, at least one correct choice
4. **Quiz Attempt**: Time limit check, one attempt per active session
5. **Answer Submission**: All questions must be answered (or timer expires)

---

## Security & Access Control

- **User Access**: Can only view/edit their own attempts
- **Admin Access**: Requires `is_staff = True`
- **Quiz Visibility**: Only active quizzes shown to users
- **Attempt Protection**: Users cannot modify completed attempts

