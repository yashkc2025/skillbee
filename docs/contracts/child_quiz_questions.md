# Quiz Attempt API Contract

## 1. Get Questions

`GET /api/child/{child_id}/curriculum/{curriculum_id}/lesson/{lesson_id}/quiz/{quiz_id}`
**Description**: Returns about curriculum, lesson, quizzes and questions with their options

### Request Parameters

| Parameter       | Type    | Description   | Location |
| --------------- | ------- | ------------- | -------- |
| `child_id`      | integer | Child ID      | Path     |
| `curriculum_id` | integer | Curriculum ID | Path     |
| `lesson_id`     | integer | Lesson ID     | Path     |
| `quiz_id`       | integer | Lesson ID     | Path     |

### Response (200 OK)

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
    "time_duration": "string (e.g., '5 mins')"
  },
  "questions": [
    {
      "question_index": "integer",
      "question": "string",
      "options": "list",
      "marks": "integer"
    }
  ]
}
```

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
