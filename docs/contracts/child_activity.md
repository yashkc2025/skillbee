# Activity Management API Contract

## 1. Get Lesson Activities

`GET /api/child/{child_id}/curriculum/{curriculum_id}/lesson/{lesson_id}/activities`  
**Description**: Returns curriculum, lesson, and activities which are created by admin and parent to their child

### Request Parameters

| Parameter       | Type    | Description   | Location |
| --------------- | ------- | ------------- | -------- |
| `child_id`      | integer | Child ID      | Path     |
| `curriculum_id` | integer | Curriculum ID | Path     |
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
  "activities": [
    {
      "activity_id": "integer",
      "name": "string",
      "description": "string",
      "image": "string (URL)",
      "difficulty": "string (Easy/Medium/Hard)",
      "progress_status": "number (0-100)"
    }
  ]
}
```

### Notes:

- Includes activities from both admin and parents
- `progress_status` = 100 if any submission exists
- `progress_status` = 0 if not any submission exists

---

## 2. Get Activity Details

`GET /api/activity/{activity_id}`  
**Description**: Returns activity details

### Request Parameters

| Parameter     | Type    | Description | Location |
| ------------- | ------- | ----------- | -------- |
| `activity_id` | integer | Activity ID | Path     |

### Response (200 OK)

```json
{
  "selected_activity": {
    "activity_id": "integer",
    "name": "string",
    "description": "string",
    "instruction": "string",
    "difficulty": "string",
    "progress_status": "number (0-100)"
  }
}
```

---

## 3. Submit Activity Work

`POST /api/child/{child_id}/activity/{activity_id}/submit`  
**Description**: Stores activity submission

### Request Parameters

| Parameter     | Type    | Description | Location |
| ------------- | ------- | ----------- | -------- |
| `child_id`    | integer | Child ID    | Path     |
| `activity_id` | integer | Activity ID | Path     |

### Request Body (multipart/form-data)

| Field  | Type   | Description            |
| ------ | ------ | ---------------------- |
| `file` | binary | JPG, JPEG, PNG, or PDF |

### Response (201 Created)

```json
{
  "activity_history_id": "integer",
  "completed_at": "datetime (ISO format)"
}
```

---

## 4. Get Activity History

`GET /api/child/{child_id}/activity/{activity_id}/history`  
**Description**: Returns submission history

### Request Parameters

| Parameter     | Type    | Description | Location |
| ------------- | ------- | ----------- | -------- |
| `child_id`    | integer | Child ID    | Path     |
| `activity_id` | integer | Activity ID | Path     |

### Response (200 OK)

```json
{
  "activity_id": "integer",
  "submissions": [
    {
      "activity_history_id": "integer",
      "completed_at": "datetime (ISO format)",
      "feedback": {
        "admin": "string",
        "parent": "string"
      }
    }
  ]
}
```

---

## 5. Get Activity Submission

`GET /api/activity/history/{activity_history_id}`  
**Description**: Returns submission file

### Request Parameters

| Parameter             | Type    | Description       | Location |
| --------------------- | ------- | ----------------- | -------- |
| `activity_history_id` | integer | History record ID | Path     |

### Response (200 OK)

- File stream with appropriate Content-Type header
