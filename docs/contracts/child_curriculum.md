# Curriculum API Contract

## Endpoint

`GET /api/child/curriculums`

---

## Authentication

- **Required**: Yes
- **Token Type**: Bearer token
- **Allowed Roles**: child

---

## Request Parameters

| Parameter | Type | Description | Location |
| --------- | ---- | ----------- | -------- |
| None      | -    | -           | -        |

**Note**: Child identification is handled through the authentication token.

---

## Response Format

### Success Response (200)

```json
{
  "curriculums": [
    {
      "curriculum_id": "integer",
      "name": "string",
      "image": "string (URL) | null",
      "description": "string",
      "progress_status": "number (0-100)"
    }
  ]
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

#### 500 Internal Server Error
```json
{
  "error": "Database error occurred"
}
```

---

## Data Requirements

1. **Child Age Group Filtering**

   - Fetch child's age from authenticated child's profile
   - Only return curriculums matching the child's age group

2. **Progress Calculation**  
   Formula:  
   `progress_status = (completed_items / total_items) * 100`  
   Where:
   - `completed_items` =
     - Lessons marked complete
     - Activities with submissions
     - Quizzes with passing scores (≥40%)
   - `total_items` =
     - Total lessons
     - Total activities
     - Total quizzes  
       _(All counts specific to the curriculum)_

3. **Image Field**
   - Currently always returns `null`
   - Planned for future implementation

4. **Authentication**
   - Child identity is derived from the authentication token
   - No additional parameters required in the request
