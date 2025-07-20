# Quiz Management API Contract

## 1. Get Lesson Quizzes

`GET /api/child/curriculum/{curriculum_id}/lesson/{lesson_id}/quizzes`  
**Description**: Returns curriculum, lesson, and quizzes

### Request Parameters

| Parameter       | Type    | Description   | Location |
| --------------- | ------- | ------------- | -------- |
| `lesson_id`     | integer | Lesson ID     | Path     |

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
  "quizzes": [
    {
      "quiz_id": "integer",
      "name": "string",
      "description": "string",
      "time_duration": "string (e.g., '5 mins')",
      "difficulty": "string (Easy/Medium/Hard)",
      "progress_status": "number (0 or 100)",
      "image": "string (URL)"
    }
  ]
}
```

### Progress Status Calculation

- `progress_status = 100` if child has attempted quiz at least once
- `progress_status = 0` if no attempts exist

---

## 2. Get Quiz History

`GET /api/child/quiz/{quiz_id}/history`  
**Description**: Returns quiz attempt history

### Request Parameters

| Parameter  | Type    | Description | Location |
| ---------- | ------- | ----------- | -------- |
| `quiz_id`  | integer | Quiz ID     | Path     |

### Response (200 OK)

```json
{
  "quizzes_history": [
    {
      "quiz_history_id": "integer",
      "quiz_id": "integer",
      "attempted_at": "datetime (ISO format)",
      "score": "number",
      "feedback": "string"
    }
  ]
}
```
