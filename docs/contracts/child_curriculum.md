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
