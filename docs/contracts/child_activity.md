# Activity Management API Contract

## 1. Get Lesson Activities

**Endpoint**: `GET /api/child/lesson/{lesson_id}/activities`  
**Description**: Returns curriculum, lesson, and activities for the authenticated child  
**Authentication**: Required (Child token)

**Behavior Notes**:
- Only returns activities specifically assigned to the authenticated child
- Activities are filtered by both lesson and child
- Progress is calculated based on submission history for this specific child

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
  "activities": [
    {
      "activity_id": "integer",
      "name": "string",
      "description": "string",
      "image": "binary data | null",
      "progress_status": "number (0 or 100)"
    }
  ]
}
```

### Progress Status Logic

- `progress_status` = 100 if any submission exists for the activity
- `progress_status` = 0 if no submission exists

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

## 2. Get Activity Details

**Endpoint**: `GET /api/child/activity/{activity_id}`  
**Description**: Returns detailed information about a specific activity for the authenticated child  
**Authentication**: Required (Child token)

### Request Parameters

| Parameter     | Type    | Description | Location |
| ------------- | ------- | ----------- | -------- |
| `activity_id` | integer | Activity ID | Path     |

**Note**: Child identification is handled through the authentication token. Only activities assigned to the authenticated child can be accessed.

### Response Format (200 OK)

```json
{
  "activity_id": "integer",
  "name": "string", 
  "description": "string",
  "image": "binary data | null",
  "answer_format": "string | null",
  "completed_at": "datetime (ISO format) | null"
}
```

### Field Descriptions

- `activity_id`: Unique identifier for the activity
- `name`: Display name of the activity
- `description`: Detailed description of what the activity involves
- `image`: Binary image data associated with the activity (can be null)
- `answer_format`: Expected format for activity submission (text/image/pdf, can be null)
- `completed_at`: ISO datetime of most recent completion (null if never completed)

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
  "error": "Activity not found"
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

## 3. Submit Activity Work

**Endpoint**: `POST /api/child/activity/{activity_id}/submit`  
**Description**: Submits a file (image or PDF) as an activity solution for the authenticated child  
**Authentication**: Required (Child token)

### Request Parameters

| Parameter     | Type    | Description | Location |
| ------------- | ------- | ----------- | -------- |
| `activity_id` | integer | Activity ID | Path     |

**Note**: Child identification is handled through the authentication token.

### Request Body Options

#### Option 1: Multipart Form Data
```
Content-Type: multipart/form-data
```

| Field  | Type   | Description                          |
| ------ | ------ | ------------------------------------ |
| `file` | binary | JPG, JPEG, PNG, or PDF file (max 10MB) |

#### Option 2: Raw Binary Upload
```
Content-Type: image/jpeg | image/png | application/pdf
```
Raw binary file data in request body (max 10MB)

### File Requirements

- **Supported formats**: JPG, JPEG, PNG, PDF
- **Maximum file size**: 10MB
- **File validation**: Format and size are validated server-side

### Response Format (201 Created)

```json
{
  "activity_history_id": "integer",
  "submitted_at": "datetime (ISO format)"
}
```

### Error Responses

#### 400 Bad Request
```json
{
  "error": "No file selected"
}
```
or
```json
{
  "error": "No file uploaded or unsupported content type"
}
```
or
```json
{
  "error": "No file data received"
}
```
or
```json
{
  "error": "File size too large. Maximum allowed size is 10MB"
}
```
or
```json
{
  "error": "Invalid file format. Only JPG, JPEG, PNG, or PDF allowed"
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
  "error": "Activity not found"
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

## 4. Get Activity History

**Endpoint**: `GET /api/child/activity/{activity_id}/history`  
**Description**: Returns submission history for a specific activity for the authenticated child  
**Authentication**: Required (Child token)

### Request Parameters

| Parameter     | Type    | Description | Location |
| ------------- | ------- | ----------- | -------- |
| `activity_id` | integer | Activity ID | Path     |

**Note**: Child identification is handled through the authentication token. Only activities assigned to the authenticated child can be accessed.

### Response Format (200 OK)

```json
{
  "activities_submission": [
    {
      "activity_history_id": "integer",
      "activity_id": "integer",
      "submitted_at": "datetime (ISO format)",
      "feedback": "string | null"
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

#### 404 Not Found
```json
{
  "error": "Activity not found"
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

## 5. Get Activity Submission

**Endpoint**: `GET /api/child/activity/history/{activity_history_id}`  
**Description**: Returns the submitted file for a specific activity submission for the authenticated child  
**Authentication**: Required (Child token)

### Request Parameters

| Parameter             | Type    | Description       | Location |
| --------------------- | ------- | ----------------- | -------- |
| `activity_history_id` | integer | History record ID | Path     |

**Note**: Child identification is handled through the authentication token. Only submissions belonging to the authenticated child can be accessed.

### Response Format (200 OK)

- File stream with appropriate Content-Type header
- Content-Type will match the original file type (image/jpeg, image/png, application/pdf)
- File is returned as an attachment with descriptive filename

### File Type Detection

The system automatically detects file types using:
1. **Magic number analysis** - Examines file headers for accurate type detection
2. **Activity format fallback** - Uses activity.answer_format if magic numbers don't match
3. **Default handling** - Falls back to application/octet-stream for unknown types

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
  "error": "Submission not found"
}
```
or
```json
{
  "error": "Associated activity not found"
}
```
or
```json
{
  "error": "No file found for this submission"
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
curl -X GET "https://api.example.com/api/child/activity/history/12345" \
  -H "Authorization: Bearer your_token_here" \
  --output submission_file.jpg
```

### Notes
- Returns binary file data, not JSON
- Response includes Content-Disposition header for proper file download
- Only submissions from activities assigned to the authenticated child are accessible
- File type is automatically detected and appropriate Content-Type header is set
