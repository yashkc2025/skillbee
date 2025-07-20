## Creation (POST)

### 🔹 Post Feedback

**POST** `/feedback`
**Access:** `@only parent`

#### 🧾 Body

```ts
{
  skill_type: "Quiz" | "Activity";
  id: number;
  text: string;
}
```

### 🔹 Create New Child

**POST** `/parent/children`
**Access:** `@only parent`

#### 🧾 Body

```ts
{
  name: string;
  username: string;
  password: string;
  confirmPass: string;
  dob: string; // YYYY-MM-DD
  school: string;
}
```

## Mutation (PUT)

### 🔹 Update Personal Details

**PUT** `/parent/update_personal_details`
**Access:** `@only parent`

#### 🧾 Body

```ts
{
    name : string;
    email : string
}
```

### 🔹 Update Password

**PUT** `/parent/update_password`
**Access:** `@only parent`

#### 🧾 Body

```ts
{
    oldPassword : string;
    newPassword : string
    confirmPassword : string
}
```
