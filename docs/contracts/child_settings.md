# Child Profile API Contract

## 1. Get Child Profile

**Endpoint**: `GET /api/child/setting`  
**Description**: Fetch the authenticated child's profile details including profile image, name, date of birth, email, and school  
**Authentication**: Required (Child token)

**Note**: Child identification is handled through the authentication token.

### Response Format (200 OK)

```json
{
  "profile_image_url": "string",
  "name": "string", 
  "dob": "string | null",
  "email": "string | null",
  "school": "string | null"
}
```

### Field Descriptions

- `profile_image_url`: URL or binary data for profile image (empty string if no image)
- `name`: Child's full name
- `dob`: Date of birth in ISO format (null if not set)
- `email`: Child's email address (null if not set)
- `school`: Child's school name (null if not set)

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
  "error": "Child not found"
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
curl -X GET "https://api.example.com/api/child/setting" \
  -H "Authorization: Bearer your_token_here"
```

### Example Response
```json
{
  "profile_image_url": "",
  "name": "John Doe",
  "dob": "2010-05-15",
  "email": "john.doe@example.com",
  "school": "Elementary School"
}
```

---

## 2. Update Child Profile Details

**Endpoint**: `PUT /api/child/update_profile`  
**Description**: Update the authenticated child's name, date of birth, email, or school  
**Authentication**: Required (Child token)

**Note**: Child identification is handled through the authentication token.

### Request Body

```json
{
  "name": "string",
  "email": "string",
  "dob": "string", 
  "school": "string"
}
```

### Request Body Rules

- All fields are optional but **at least one must be present**
- `name`: Cannot be empty if provided
- `email`: Must be unique across all children if provided (can be null)
- `dob`: Must be in YYYY-MM-DD format, child must be 8-14 years old
- `school`: Can be empty/null

### Response Format (200 OK)

```json
{
  "status": "success",
  "message": "Profile details updated"
}
```

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
  "error": "At least one field must be provided"
}
```
or
```json
{
  "error": "Name cannot be empty"
}
```
or
```json
{
  "error": "Invalid date format. Use YYYY-MM-DD"
}
```
or
```json
{
  "error": "Child must be between 8 and 14 years old"
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
  "error": "Child not found"
}
```

#### 409 Conflict
```json
{
  "error": "Email already registered by another child"
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
curl -X PUT "https://api.example.com/api/child/update_profile" \
  -H "Authorization: Bearer your_token_here" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Smith",
    "email": "john.smith@example.com",
    "school": "New Elementary School"
  }'
```

---

## 3. Change Password

**Endpoint**: `PUT /api/child/change_password`  
**Description**: Change the authenticated child's password by providing current and new passwords  
**Authentication**: Required (Child token)

**Note**: Child identification is handled through the authentication token.

### Request Body

```json
{
  "current_password": "string",
  "new_password": "string", 
  "confirm_password": "string"
}
```

### Request Body Rules

- All fields are **required**
- `current_password`: Must match child's current password
- `new_password`: Must be at least 4 characters long and different from current password
- `confirm_password`: Must match `new_password`

### Response Format (200 OK)

```json
{
  "status": "success",
  "message": "Password changed successfully"
}
```

### Error Responses

#### 400 Bad Request
```json
{
  "status": "error",
  "message": "No data provided"
}
```
or
```json
{
  "status": "error", 
  "message": "Current password, new password, and confirm password are required"
}
```
or
```json
{
  "status": "error",
  "message": "Current password is incorrect"
}
```
or
```json
{
  "status": "error",
  "message": "New password and confirm password do not match"
}
```
or
```json
{
  "status": "error",
  "message": "New password must be at least 4 characters long"
}
```
or
```json
{
  "status": "error",
  "message": "New password must be different from current password"
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
  "status": "error",
  "message": "Child not found"
}
```

#### 500 Internal Server Error
```json
{
  "status": "error",
  "message": "Database error occurred"
}
```

### Example Request
```bash
curl -X PUT "https://api.example.com/api/child/change_password" \
  -H "Authorization: Bearer your_token_here" \
  -H "Content-Type: application/json" \
  -d '{
    "current_password": "oldpass123",
    "new_password": "newpass456",
    "confirm_password": "newpass456"
  }'
```

---

## 4. Update Profile Image

**Endpoint**: `GET/POST /api/child/profile_image`  
**Description**: Retrieve or upload/update the authenticated child's profile image  
**Authentication**: Required (Child token)

**Note**: Child identification is handled through the authentication token.

### GET Method - Retrieve Profile Image

#### Response Format (200 OK)
```json
{
  "profile_image": "string | null"
}
```

#### Field Descriptions
- `profile_image`: Profile image data (empty string if no image set, null if none)

### POST Method - Upload Profile Image

#### Request Body
```json
{
  "profile_image": "string"
}
```

#### Request Body Fields
- `profile_image`: Image data (empty string to clear image, or image data to set)

#### Response Format (200 OK)
```json
{
  "status": "success",
  "message": "Profile image updated successfully"
}
```

### Error Responses

#### 400 Bad Request
```json
{
  "status": "error",
  "message": "No data provided"
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
  "status": "error",
  "message": "Child not found"
}
```

#### 500 Internal Server Error
```json
{
  "status": "error",
  "message": "Database error occurred"
}
```

### Example Requests

**GET Profile Image:**
```bash
curl -X GET "https://api.example.com/api/child/profile_image" \
  -H "Authorization: Bearer your_token_here"
```

**POST Profile Image:**
```bash
curl -X POST "https://api.example.com/api/child/profile_image" \
  -H "Authorization: Bearer your_token_here" \
  -H "Content-Type: application/json" \
  -d '{"profile_image": "base64_encoded_image_data"}'
```

### Example Responses

**GET Response:**
```json
{
  "profile_image": ""
}
```

**Clear Image (POST with empty string):**
```bash
curl -X POST "https://api.example.com/api/child/profile_image" \
  -H "Authorization: Bearer your_token_here" \
  -H "Content-Type: application/json" \
  -d '{"profile_image": ""}'
```

### Implementation Notes
- The controller stores image data directly in the `profile_image` field of the Child model
- Empty string sets the field to null (clears the image)
- GET method always returns 200 OK with the current image data
- POST method now returns proper JSON responses with status and message
- Controller includes proper child validation and error handling
- All database operations are wrapped in try-catch blocks with rollback on errors
