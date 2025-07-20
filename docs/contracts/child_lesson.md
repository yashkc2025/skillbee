# Lesson Management API Contract

## 1. Get Curriculum Lessons

**Endpoint**: `GET /api/child/curriculum/{curriculum_id}/lessons`  
**Description**: Returns curriculum details and lessons with progress status

### Request Parameters

| Parameter       | Type    | Description                     | Location |
| --------------- | ------- | ------------------------------- | -------- |
| `curriculum_id` | integer | Curriculum ID to filter lessons | Path     |

### Response Format (200 OK)

```json
{
  "curriculum": {
    "curriculum_id": "integer",
    "name": "string"
  },
  "lessons": [
    {
      "lesson_id": "integer",
      "title": "string",
      "image": "string (URL)",
      "description": "string",
      "progress_status": "number (0-100)"
    }
  ]
}
```

### Progress Calculation

progress_status = (completed_activities + completed_quizzes) / (total_activities + total_quizzes) \* 100

- Only includes activities/quizzes for this lesson
- `completed_activities`: Activities with submissions
- `completed_quizzes`: Quizzes with submissions

---

## 2. Get Lesson Details

**Endpoint**: `GET /api/lesson/{lesson_id}`  
**Description**: Returns lesson content and completed_at  
**Authentication**: Required (Child token)

### Request Parameters

| Parameter   | Type    | Description | Location |
| ----------- | ------- | ----------- | -------- |
| `lesson_id` | integer | Lesson ID   | Path     |

### Response Format (200 OK)

```json
{
  "lesson_id": "integer",
  "title": "string",
  "content": {
    "text": "string"
  },
  "image": "string (URL) | null",
  "completed_at": "datetime (ISO format) | null"
}
```

---

## 3. Mark Lesson as Read

**Endpoint**: `POST /api/child/lesson/{lesson_id}/mark-read`  
**Description**: Records lesson completion timestamp

### Request Parameters

| Parameter   | Type    | Description | Location |
| ----------- | ------- | ----------- | -------- |
| `child_id`  | integer | Child ID    | Path     |
| `lesson_id` | integer | Lesson ID   | Path     |

### Request Body

```json
{
  "completed_at": "datetime (ISO format - optional)"
}
```

- If `completed_at` not provided, uses current server time

### Response (201 Created)

```json
{
  "status": "success",
  "completed_at": "2025-06-30T23:31:45.000Z"
}
```
