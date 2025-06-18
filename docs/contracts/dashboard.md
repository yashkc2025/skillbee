## **GET /get\_user\_details**

**Description:** Retrieve details of the currently authenticated user.

### Response

```json
{
  "name": "string",
  "email": "string",
  "id": "string | number",
  "user_type": "string"
}
```

### Field Types

| Field      | Type                 | Description                            |
| ---------- | -------------------- | -------------------------------------- |
| name       | `string`             | Full name of the user                  |
| email      | `string`             | Email address                          |
| id         | `string` or `number` | Unique user identifier                 |
| user\_type | `string`             | Type of user (e.g., "parent", "child") |

---

## **GET /child\_dashboard\_stats**

**Description:** Retrieve dashboard statistics for a child user.

### Response

```json
{
  "lessons_completed": "number",
  "skills_completed": "number",
  "streak": "number",
  "badges_earned": "number",
  "leaderboard_rank": "number",
  "heatmap": [
    {
      "date": "YYYY-MM-DD",
      "status": 1
    }
  ]
}
```

### Field Types

| Field              | Type                | Description                                      |
| ------------------ | ------------------- | ------------------------------------------------ |
| lessons\_completed | `number`            | Total number of lessons completed                |
| skills\_completed  | `number`            | Total number of skills completed                 |
| streak             | `number`            | Current streak in days                           |
| badges\_earned     | `number`            | Total number of badges earned                    |
| leaderboard\_rank  | `number`            | Current leaderboard rank                         |
| heatmap            | `array of objects`  | Activity by date (only present if status exists) |
| └─ date            | `string`            | Date of activity                                 |
| └─ status          | `1`                   | Activity status (e.g., 1 = completed)            |

---

## **GET /skill\_categories**

**Description:** Get skill category and progress for the user.

### Response

```json
[
  {
    "name": "string",
    "link": "string (URL)",
    "percentage_completed": "number"
  }
]
```

### Field Types

| Field                 | Type     | Description                      |
| --------------------- | -------- | -------------------------------- |
| name                  | `string` | Name of the skill category       |
| link                  | `string` | URL to access the skill category |
| percentage\_completed | `number` | Progress in percentage (0–100)   |

---

## **GET /user\_badges**

**Description:** Retrieve all badges earned by the user.

### Response

```json
[
  {
    "name": "string",
    "image": "string (URL)"
  }
]
```

### Field Types

| Field | Type     | Description            |
| ----- | -------- | ---------------------- |
| name  | `string` | Name of the badge      |
| image | `string` | URL to the badge image |
