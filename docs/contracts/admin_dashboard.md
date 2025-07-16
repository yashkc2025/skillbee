## 🔐 Access Levels

* `@only admin` → Admin-only access
* `@only parent and admin` → Both Parent and Admin
* `@only parent` → Parent-only access


## 📚 Endpoints


### 🔹 Get Children

**GET** `/children`
**Access:** `@only parent and admin`
> Only allow parent to access thier children

#### ✅ Response

```ts
{
  id: number
  name: string
  email: string
  age: number
  school_name: string
  last_login: string // ISO timestamp or formatted string
}
```


### 🔹 Get Parents

**GET** `/parents`
**Access:** `@only admin`

#### ✅ Response

```ts
{
  id: number
  name: string
  email: string
  blocked: boolean
}
```


### 🔹 Get Lessons

**GET** `/lessons`
**Access:** `@only parent and admin`

#### ✅ Response

```ts
{
  id: number
  title: string
  curriculum: string
}
```


### 🔹 Get Quizzes

**GET** `/quizzes`
**Access:** `@only parent and admin`

#### 🧾 Query Params

```ts
{
  lesson_id?: number
}
```

#### ✅ Response

```ts
{
  id: number
  title: string
  lesson: string
  curriculum: string
}
```


### 🔹 Get Activities

**GET** `/activities`
**Access:** `@only parent and admin`

#### 🧾 Query Params

```ts
{
  lesson_id?: number
}
```

#### ✅ Response

```ts
{
  id: number
  title: string
  lesson: string
  curriculum: string
}
```


### 🔹 Get Badges

**GET** `/badges`
**Access:** `@only parent and admin`

#### ✅ Response

```ts
{
  id: number
  label: string
  image: string // Base64
}
```


### 🔹 Get Children Profile

**GET** `/children/profile`
**Access:** `@only parent and admin`

> If parent, only allowed for their own children.

#### 🧾 Params

```ts
{
  id: number
}
```

#### ✅ Response

```ts
{
  info: {
    child_id: string
    full_name: string
    age: number
    grade: string
    enrollment_date: string // e.g., "2024-09-20"
    status: string
    parent: {
      id: number
      name: string
      email: string
    }
  },
  skills_progress: Array<{
    skill_id: string
    skill_name: string
    progress_percent: number
  }>,
  assessments: Array<{
    id: number
    skill_id: string
    assessment_type: "Quiz" | "Activity"
    title: string
    date: string // ISO or YYYY-MM-DD
    score: number | string // can be number or "Pass"
    max_score: number | string
  }>,
  achievements: {
    badges: Array<{
      badge_id: string
      title: string
      image : string // Base64
      awarded_on: string // ISO or date string
    }>
    streak: number
  },
}
```


## 🟢 Mutations (POST)


### 🔹 Post Feedback

**POST** `/feedback`
**Access:** `@only parent`

#### 🧾 Body

```ts
{
  skill_type: "Quiz" | "Activity"
  id: number
  text: string
}
```


### 🔹 Create New Activity

**POST** `/admin/activity`
**Access:** `@only admin`

#### 🧾 Body

```ts
{
  lesson: string
  image: string // Base64
  title: string
  description: string
  instructions: string
  difficulty: string
  point: number
}
```


### 🔹 Create New Child

**POST** `/parent/children`
**Access:** `@only parent`

#### 🧾 Body

```ts
{
  name: string
  username: string
  password: string
  confirmPass: string
  dob: string // YYYY-MM-DD
  school: string
}
```


### 🔹 Create New Lesson

**POST** `/admin/lesson`
**Access:** `@only admin`

#### 🧾 Body

```ts
{
  title: string
  content: string
  image: string // Base64
  description: string
  badge_id: number
  curriculum_id: number
}
```


### 🔹 Create New Badge

**POST** `/admin/badge`
**Access:** `@only admin`

#### 🧾 Body

```ts
{
  title: string
  image: string // Base64
  points: number
}
```


### 🔹 Create New Quiz

**POST** `/admin/quiz`
**Access:** `@only admin`

#### 🧾 Body

```ts
{
  lesson: string
  image: string // Base64
  title: string
  description: string
  difficulty: string
  point: number
  questions: {
    question : string
    options : {
      text : string
      isCorrect : boolean
    }[]
  }
}
```
