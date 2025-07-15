# Child Profile API Contract

## 1. Get Child Profile

**Endpoint**

`GET /api/child/{child_id}/setting`

**Description**  
Fetch the child's profile details including profile image, name, date of birth, email, and school.

**Path Parameters**

| Name     | Type | Description            |
| -------- | ---- | ---------------------- |
| child_id | int  | Unique ID of the child |

### Response (200 OK)

```json
{
  "profile_image_url": "string",
  "name": "string",
  "dob": "string",
  "email": "string",
  "school": "string"
}
```

---

## 2. Update Child Profile Details

**Endpoint**

`PUT /api/child/{child_id}/update/profile`

**Description**  
Update the child's name, date of birth, email, or school.

**Path Parameters**

| Name     | Type | Description            |
| -------- | ---- | ---------------------- |
| child_id | int  | Unique ID of the child |

**Request Body** (`application/json`)

```json
{
  "name": "string",
  "email": "string",
  "dob": "string",
  "school": "string"
}
```

- All fields are optional but at least one must be present.

**Response** (`application/json`)

```json
{
  "status": "success",
  "message": "Profile details updated"
}
```

---

## 3. Change Password

**Endpoint**

`PUT /api/child/{child_id}/change/password`

**Description**  
Change the child's password by providing the current password and the new password.

**Path Parameters**

| Name     | Type | Description            |
| -------- | ---- | ---------------------- |
| child_id | int  | Unique ID of the child |

**Request Body** (`application/json`)

```json
{
  "current_password": "string",
  "new_password": "string",
  "confirm_password": "string"
}
```

**Response** (`application/json`)

- On Success:

```json
{
  "status": "success",
  "message": "Password changed successfully"
}
```

- On Failure (e.g. current password incorrect):

```json
{
  "status": "error",
  "message": "Current password is incorrect"
}
```

---

## 4. Update Profile Image

**Endpoint**

`POST /api/child/{child_id}/profile/image`

**Description**  
Upload and update the child's profile image.

**Path Parameters**

| Name     | Type | Description            |
| -------- | ---- | ---------------------- |
| child_id | int  | Unique ID of the child |

**Request Body** (`multipart/form-data`)

| Field | Type | Description                       |
| ----- | ---- | --------------------------------- |
| image | file | The new profile image (JPEG, PNG) |

**Response** (`application/json`)

```json
{
  "status": "success",
  "message": "Profile image updated",
  "profile_image_url": "/files/new-profile.jpg"
}
```
