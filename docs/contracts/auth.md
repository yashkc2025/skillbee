# 📘 **API Contract: Authentication API**

## Parent Endpoints

### **1. Parent Register**

- **Endpoint:** `POST /auth/parent_register`
- **Description:** Registers a parent account.

#### Request Body (JSON):

```json
{
  "name": "string",
  "email": "string",
  "password": "string",
  "profile_image": "string (base64, optional)"
}
```

#### Success Response: `201 Created`

```json
{
  "session": {
    "token": "string",
    ...
  },
  "user": {
    "id": "string"
  }
}
```

#### Error Responses:

- `400 Bad Request` – Missing or malformed fields.
- `409 Conflict` – Email already registered.

---

### **2. Parent Login**

- **Endpoint:** `POST /auth/parent_login`
- **Description:** Authenticates an existing parent account.

#### Request Body (JSON):

```json
{
  "email": "string",
  "password": "string"
}
```

#### Success Response: `200 OK`

```json
{
  "session": {
    "token": "string",
    ...
  },
  "user": {
    "id": "string"
  }
}
```

#### Error Responses:

- `400 Bad Request` – Missing required fields.
- `401 Unauthorized` – Invalid email or password.

---

## Children Endpoints

### **3. Child Register**

- **Endpoint:** `POST /auth/children_register`
- **Description:** Registers a new child account.

#### Request Body (JSON):

```json
{
  "email": "string",
  "password": "string",
  "username": "string",
  "dob": "YYYY-MM-DD",
  "school": "string",
  "profile_image": "string (base64, optional)"
}
```

#### Success Response: `201 Created`

```json
{
  "session": {
    "token": "string",
    ...
},
  "user": {
    "id": "string"
  }
}
```

#### Error Responses:

- `400 Bad Request` – Invalid/missing fields.
- `409 Conflict` – Email or username already in use.

---

### **4. Child Login**

- **Endpoint:** `POST /auth/children_login`
- **Description:** Authenticates a child account via username or email.

#### Request Body (JSON):

```json
{
  "email_or_username": "string",
  "password": "string"
}
```

#### Success Response: `200 OK`

```json
{
  "session": {
    "token": "string",
    ...
  },
  "user": {
    "id": "string"
  }
}
```

#### Error Responses:

- `400 Bad Request` – Missing or malformed input.
- `401 Unauthorized` – Invalid credentials.
- `404 Not Found` – User does not exist.

## Shared Endpoint

### **5. Get Authenticated User**

**GET** `/auth/get_user`

Fetches the currently authenticated user's profile using a Bearer token.

#### Headers:

```
Authorization: Bearer <session_token>
```

#### Success: `200 OK`

```json
{
  "user": {
    "id": "string",
    "role": "parent" | "child",
    "name": "string (if parent)",
    "username": "string (if child)",
    "email": "string",
    "dob": "YYYY-MM-DD (if child)",
    "school": "string (if child)",
    "profile_image": "string (base64 or null)"
  }
}
```

#### Error Responses:

- `401 Unauthorized` – Invalid credentials.
- `403 Bad Request` – Missing or malformed token
