# Quiz Management API Contract

## 1. Get Lesson Quizzes

**Endpoint**: `GET /api/child/lesson/{lesson_id}/quizzes`  
**Description**: Returns curriculum, lesson, and quizzes associated with a specific lesson for the authenticated child  
**Authentication**: Required (Child token)

### Request Parameters

| Parameter   | Type    | Description | Location |
| ----------- | ------- | ----------- | -------- |
| `lesson_id` | integer | Lesson ID   | Path     |

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
  "quizzes": [
    {
      "quiz_id": "integer",
      "name": "string",
      "description": "string",
      "time_duration": "integer | null",
      "progress_status": "number (0 or 100)",
      "image": "binary data | null"
    }
  ]
}
```

### Field Descriptions

- `curriculum`: Information about the curriculum containing this lesson
- `lesson`: Information about the lesson containing these quizzes
- `quizzes`: Array of quiz objects with progress information
- `time_duration`: Duration in minutes (null if not set)
- `progress_status`: 100 if child has attempted quiz at least once, 0 otherwise
- `image`: Binary image data associated with the quiz (null if no image)

### Progress Status Calculation

- `progress_status = 100` if child has attempted quiz at least once
- `progress_status = 0` if no attempts exist

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
  "error": "Lesson not found or does not belong to the curriculum"
}
```
or
```json
{
  "error": "Curriculum not found"
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

## 2. Submit Quiz Answers

**Endpoint**: `POST /api/child/quizzes/{quiz_id}/submit`  
**Description**: Submit quiz answers and receive calculated score for the authenticated child  
**Authentication**: Required (Child token)

### Request Parameters

| Parameter | Type    | Description | Location |
| --------- | ------- | ----------- | -------- |
| `quiz_id` | integer | Quiz ID     | Path     |

**Note**: Child identification is handled through the authentication token.

### Request Body

```json
{
  "answers": {
    "question_index": "option_index"
  }
}
```

### Request Body Format

- `answers` (object, required): Dictionary mapping question indices to selected option indices
- `question_index` (string): 1-based index of the question (e.g., "1", "2", "3")
- `option_index` (string): 0-based index of the selected option (e.g., "0", "1", "2", "3")

### Response Format (200 OK)

```json
{
  "score": "integer",
  "total_score": "integer"
}
```

### Field Descriptions

- `score`: Points earned by the child for correct answers
- `total_score`: Maximum possible points for this quiz

### Scoring Logic

- Each question has an associated marks value (default: 1 point)
- Points are awarded only for correct answers
- Selected option text must exactly match the correct answer
- Invalid question/option indices are skipped (no penalty)
- Quiz attempt is saved to history regardless of score

### Validation Rules

1. **Quiz Existence**: Quiz must exist and be accessible
2. **Answer Format**: Must provide valid JSON with "answers" object
3. **Quiz Data**: Quiz must have both questions and answers arrays
4. **Data Consistency**: Questions and answers arrays must have equal length
5. **Index Validation**: Question indices (1-based) and option indices (0-based) must be within valid ranges

### Error Responses

#### 400 Bad Request
```json
{
  "error": "No data provided"
}
```
or
```json
{
  "error": "Invalid answers format. Expected dictionary with question_index: option_index"
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
  "error": "Quiz not found"
}
```

#### 500 Internal Server Error
```json
{
  "error": "Quiz has no questions or answer key"
}
```
or
```json
{
  "error": "Quiz data inconsistency: questions and answers count mismatch"
}
```
or
```json
{
  "error": "Database error occurred",
  "details": "string"
}
```

### Example Request
```bash
curl -X POST "https://api.example.com/api/child/quizzes/201/submit" \
  -H "Authorization: Bearer your_token_here" \
  -H "Content-Type: application/json" \
  -d '{
    "answers": {
      "1": "1",
      "2": "0",
      "3": "2"
    }
  }'
```

### Example Response
```json
{
  "score": 5,
  "total_score": 10
}
```

### Notes
- Quiz attempts are automatically saved to history
- Multiple submissions are allowed (each creates a new history entry)
- Invalid question/option indices are silently skipped
- Questions support both string and object option formats
- Scoring is based on exact text matching for selected options

---

## 3. Get Quiz History

**Endpoint**: `GET /api/child/quiz/{quiz_id}/history`  
**Description**: Returns quiz attempt history for the authenticated child for a specific quiz  
**Authentication**: Required (Child token)

### Request Parameters

| Parameter | Type    | Description | Location |
| --------- | ------- | ----------- | -------- |
| `quiz_id` | integer | Quiz ID     | Path     |

**Note**: Child identification is handled through the authentication token.

### Response Format (200 OK)

```json
{
  "quizzes_history": [
    {
      "quiz_history_id": "integer",
      "quiz_id": "integer", 
      "attempted_at": "string (ISO datetime)",
      "score": "integer",
      "feedback": "string | null"
    }
  ]
}
```

### Field Descriptions

- `quizzes_history`: Array of quiz attempt records
- `quiz_history_id`: Unique identifier for the quiz attempt
- `quiz_id`: ID of the quiz that was attempted
- `attempted_at`: ISO format datetime when the quiz was attempted
- `score`: Points scored in the quiz attempt
- `feedback`: Additional feedback text (null if no feedback provided)

### Sorting

Quiz attempts are returned in **descending order** by attempt date (most recent first).

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
  "error": "Quiz not found"
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
curl -X GET "https://api.example.com/api/child/quiz/201/history" \
  -H "Authorization: Bearer your_token_here"
```

### Example Response
```json
{
  "quizzes_history": [
    {
      "quiz_history_id": 5,
      "quiz_id": 201,
      "attempted_at": "2024-07-20T14:30:00Z",
      "score": 8,
      "feedback": "Great improvement!"
    },
    {
      "quiz_history_id": 3,
      "quiz_id": 201,
      "attempted_at": "2024-07-19T10:00:00Z",
      "score": 5,
      "feedback": null
    }
  ]
}
```

### Notes
- Returns empty array if no attempts found (still 200 OK)
- Quiz validation ensures only existing quizzes return history
- Child can only see their own quiz history
- Attempts are ordered by date (newest first)
