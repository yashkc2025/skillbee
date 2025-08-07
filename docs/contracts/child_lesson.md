# Lesson Management API Contract

## 1. Get Curriculum Lessons

**Endpoint**: `GET /api/child/curriculum/{curriculum_id}/lessons`  
**Description**: Returns curriculum details and lessons with progress status  
**Authentication**: Required (Child token)

### Request Parameters

| Parameter       | Type    | Description                     | Location |
| --------------- | ------- | ------------------------------- | -------- |
| `curriculum_id` | integer | Curriculum ID to filter lessons | Path     |

**Note**: Child identification is handled through the authentication token.

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
      "image": "string (URL) | null",
      "description": "string",
      "progress_status": "number (0-100)"
    }
  ]
}
```

### Progress Calculation

progress_status = (attempted_activities + attempted_quizzes) / (total_activities + total_quizzes) \* 100

- Only includes activities/quizzes for this lesson and the authenticated child
- `attempted_activities`: Activities that have been attempted (with submissions in history)
- `attempted_quizzes`: Quizzes that have been attempted (regardless of score)
- If no activities or quizzes exist for a lesson, progress_status defaults to 100%

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
  "error": "Skill not found"
}
```
or
```json
{
  "error": "No lessons found for this skill"
}
```

#### 500 Internal Server Error
```json
{
  "error": "Database error occurred",
  "details": "string"
}
```

---

## 2. Get Lesson Details

**Endpoint**: `GET /api/child/lesson/{lesson_id}`  
**Description**: Returns lesson content and completion status  
**Authentication**: Required (Child token)

### Request Parameters

| Parameter   | Type    | Description | Location |
| ----------- | ------- | ----------- | -------- |
| `lesson_id` | integer | Lesson ID   | Path     |

**Note**: Child identification is handled through the authentication token.

### Response Format (200 OK)

```json
{
  "lesson_id": "integer",
  "title": "string",
  "content": "string",
  "image": "string (URL) | null", 
  "completed_at": "datetime (ISO format) | null"
}
```

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
  "error": "Lesson not found"
}
```

#### 500 Internal Server Error
```json
{
  "error": "Database error occurred",
  "details": "string"
}
```

---

## 3. Mark Lesson as Read

**Endpoint**: `POST /api/child/lesson/{lesson_id}/mark-read`  
**Description**: Records lesson completion timestamp for the authenticated child  
**Authentication**: Required (Child token)

**Behavior Notes**:
- If lesson is already marked as completed by this child, returns 200 (idempotent operation)
- Each child-lesson combination can only have one completion record
- Completion timestamp cannot be modified once set

### Request Parameters

| Parameter   | Type    | Description | Location |
| ----------- | ------- | ----------- | -------- |
| `lesson_id` | integer | Lesson ID   | Path     |

**Note**: Child identification is handled through the authentication token.

### Request Body (Optional)

```json
{
  "completed_at": "datetime (ISO format - optional)"
}
```

**Date Format Details**:
- Accepts ISO 8601 datetime format
- Supports timezone suffixes: 'Z' (UTC) or '+HH:MM'/'-HH:MM'
- Examples: `"2024-12-01T10:30:45.000Z"`, `"2024-12-01T10:30:45+05:30"`
- If `completed_at` not provided, uses current server time

### Success Response (201 Created)

```json
{
  "message": "Lesson marked as completed"
}
```

### Success Response - Already Completed (200 OK)

```json
{
  "message": "Lesson already completed"
}
```

### Error Responses

#### 400 Bad Request
```json
{
  "error": "Invalid date format"
}
```

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
  "error": "Lesson not found"
}
```

#### 500 Internal Server Error
```json
{
  "error": "Database error occurred",
  "details": "string"
}
```
