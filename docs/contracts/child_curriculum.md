# Curriculum API Contract

## Endpoint

`GET /api/child/{child_id}/curriculums`

---

## Request Parameters

| Parameter | Type    | Description                     | Location |
| --------- | ------- | ------------------------------- | -------- |
| child_id  | integer | Unique identifier for the child | Path     |

---

## Response Format

```json
{
  "curriculums": [
    {
      "curriculum_id": "integer",
      "name": "string",
      "image": "string (URL)",
      "description": "string",
      "progress_status": "number (0-100)"
    }
  ]
}
```

---

## Data Requirements

1. **Child Age Group Filtering**

   - Fetch child's age from `child_id`
   - Only return curriculums matching the child's age group

2. **Progress Calculation**  
   Formula:  
   `progress_status = (completed_items / total_items) * 100`  
   Where:
   - `completed_items` =
     - Lessons marked complete
     - Activities with submissions
     - Quizzes with passing scores
   - `total_items` =
     - Total lessons
     - Total activities
     - Total quizzes  
       _(All counts specific to the curriculum)_

---

## Example Request

GET /api/child/123/curriculums

---

## Example Response

```json
{
  "curriculums": [
    {
      "curriculum_id": 1,
      "name": "Critical Thinking",
      "image": "/files/critical_thinking.jpeg",
      "description": "Develop critical thinking skills",
      "progress_status": 60
    },
    {
      "curriculum_id": 2,
      "name": "Communication Skills",
      "image": "/files/communication_skill.jpeg",
      "description": "Enhance communication skills",
      "progress_status": 40
    }
  ]
}
```

---

## Implementation Notes

### 1. Age Group Handling

graph TD
A[Get child by ID] --> B[Determine age group]
B --> C[Filter curriculums by age group]

### 2. Error Handling

- `404 Not Found` if child_id doesn't exist
- `400 Bad Request` for invalid child_id format
- `204 No Content` if no curriculums match age group

---

## Security Requirements

- Validate child belongs to authenticated user

---

## Key Features

### Age-Appropriate Filtering

- Only returns curriculums matching the child's developmental stage

### Accurate Progress Tracking

- Comprehensive calculation including:
  - ✅ Completed lessons
  - ✅ Submitted activities
  - ✅ Passed quizzes

### Child-Centric Design

- Progress tailored to individual child
- Age-appropriate content filtering
- Secure access controls

### Clear Response Structure

- Standardized JSON format with all required curriculum data
