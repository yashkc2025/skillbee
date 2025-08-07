# Quiz Questions API Contract

## 1. Get Quiz Questions

**Endpoint**: `GET /api/child/curriculum/{curriculum_id}/lesson/{lesson_id}/quiz/{quiz_id}`  
**Description**: Returns curriculum, lesson, quiz details and questions with their options for the authenticated child  
**Authentication**: Required (Child token)

### Request Parameters

| Parameter       | Type    | Description   | Location |
| --------------- | ------- | ------------- | -------- |
| `curriculum_id` | integer | Curriculum ID | Path     |
| `lesson_id`     | integer | Lesson ID     | Path     |
| `quiz_id`       | integer | Quiz ID       | Path     |

**Note**: Child identification is handled through the authentication token.

### Response Format (200 OK)

```json
{
  "curriculum": {
    "curriculum_id": "integer",
    "name": "string"
  },
  "lesson": {
    "lesson_id": "integer",
    "title": "string"
  },
  "quizzes": {
    "quiz_id": "integer",
    "name": "string",
    "time_duration": "integer | null"
  },
  "questions": [
    {
      "question_index": "integer",
      "question": "string",
      "options": "array of strings",
      "marks": "integer"
    }
  ]
}
```

### Field Descriptions

- `curriculum`: Information about the curriculum containing this lesson
- `lesson`: Information about the lesson containing this quiz
- `quizzes`: Quiz details including name and duration
- `questions`: Array of quiz questions with their options and scoring
- `time_duration`: Duration in minutes (null if not set)
- `question_index`: 1-based index of the question
- `options`: Array of answer choices for the question
- `marks`: Points awarded for correct answer

### Validation Logic

The endpoint validates:
1. **Curriculum exists** - Returns 404 if curriculum not found
2. **Lesson belongs to curriculum** - Returns 404 if lesson doesn't belong to specified curriculum
3. **Quiz belongs to lesson** - Returns 404 if quiz doesn't belong to specified lesson

### Error Responses

#### 401 Unauthorized
```json
{
  "error": "Token is missing"
}
```

#### 403 Forbidden
```json
{
  "error": "Insufficient permissions"
}
```

#### 404 Not Found
```json
{
  "error": "Curriculum not found"
}
```
or
```json
{
  "error": "Lesson not found or does not belong to the curriculum"
}
```
or
```json
{
  "error": "Quiz not found or does not belong to the lesson"
}
```

#### 500 Internal Server Error
```json
{
  "error": "Database error occurred",
  "details": "string"
}
```

### Example Request
```bash
curl -X GET "https://api.example.com/api/child/curriculum/1/lesson/101/quiz/201" \
  -H "Authorization: Bearer your_token_here"
```

### Example Response
```json
{
  "curriculum": {
    "curriculum_id": 1,
    "name": "Mathematics Basics"
  },
  "lesson": {
    "lesson_id": 101,
    "title": "Introduction to Addition"
  },
  "quizzes": {
    "quiz_id": 201,
    "name": "Basic Addition Quiz",
    "time_duration": 10
  },
  "questions": [
    {
      "question_index": 1,
      "question": "What is 2 + 3?",
      "options": ["4", "5", "6", "7"],
      "marks": 1
    },
    {
      "question_index": 2,
      "question": "What is 10 + 15?",
      "options": ["20", "25", "30", "35"],
      "marks": 2
    }
  ]
}
```

### Notes
- Questions are returned without correct answers for security
- Question indices start from 1, not 0
- Only children with valid authentication tokens can access quiz questions
- All path parameters are validated for proper relationships

## 2. Submit Quiz

`POST /api/child/{child_id}/quizzes/{quiz_id}/submit`
**Description**: Post dictionary of index of question and option which is selected

```json
{
  "answers": {
    "question_index": "option_index"
  }
}
```

### Response (200 OK)

```json
{
  "score": "integer",
  "total_score": "integer"
}
```
