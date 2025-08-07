## 🔐 Access Levels

- `@only admin` → Admin-only access
- `@only admin or parent` → Both Parent and Admin
- `@only parent` → Parent-only access

## 📚 Endpoints

### 🔹 Get Children

**GET** `/children`
**Access:** `@only parent and admin`

> Only allow parent to access thier children

#### ✅ Response

```ts
{
  id: number;
  name: string;
  email: string;
  age: number;
  school_name: string;
  last_login: string; // ISO timestamp or formatted string
}[]
```

### 🔹 Get Parents

**GET** `/parents`
**Access:** `@only admin`

#### ✅ Response

```ts
{
  id: number;
  name: string;
  email: string;
  blocked: boolean;
}[]
```

### 🔹 Get Lessons

**GET** `/lessons`
**Access:** `@only parent and admin`

#### ✅ Response

```ts
{
  id: number;
  title: string;
  curriculum: string;
}[]
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
  id: number;
  title: string;
  lesson: string;
  curriculum: string;
}[]
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
  id: number;
  title: string;
  lesson: string;
  curriculum: string;
}[]
```

### 🔹 Get Badges

**GET** `/badges`
**Access:** `@only parent and admin`

#### ✅ Response

```ts
{
  id: number;
  label: string;
  image: string; // Base64
  points: number;
}[]
```

### 🔹 Get Children Profile

**GET** `/children/profile`
**Access:** `@only parent and admin`

> If parent, only allowed for their own children.

#### 🧾 Params

```ts
{
  id: number;
}
```

#### ✅ Response

```ts
{
  info: {
    child_id: string
    full_name: string
    age: number
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
    lesson_started_count : number
    lesson_completed_count : number
    quiz_attempted_count : number
  }>
  point_earned: Array <{
    point : number
    date: string // YYYY-MM-DD  
  }>
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

### 🔹 Get Active Users Charts

**GET** `/admin/active_users_chart`
**Access:** `@only admin`

> Only for last 15-20 days

#### 🧾 Params

```ts
{
  dates : string[]; //  YYYY-MM-DD
  active_children : number[];
  active_parents : number[];
  new_children_signups : number[];
  new_parent_signups : number[];
  total_active_users : number[]
}
```

### 🔹 Get Skill Engagements Charts

**GET** `/admin/skill_engagment_chart`
**Access:** `@only admin`

#### 🧾 Params

```ts
{
  age_8_10 : number;
  age_10_12 : number;
  age_12_14 : number
}
```

### 🔹 Get Badges by Age Group Charts

**GET** `/admin/badge_by_age_group_chart`
**Access:** `@only admin`

#### 🧾 Params

```ts
{
  badge_name : string;
  age_8_10 : number;
  age_10_12 : number;
  age_12_14 : number
}[]
```

### 🔹 Get Learning Funnel

**GET** `/admin/learning_funnel_chart`
**Access:** `@only admin`

#### 🧾 Params

```ts
{
  user_started_skill : number;
  lessons_completed : number;
  quizzes_attempted : number;
  badges_earned : number
}[]
```

### 🔹 Get Age Group Distribution Chart

**GET** `/admin/age_group_distribution_chart`
**Access:** `@only admin`

#### 🧾 Params

```ts
{
    skill_id: string
    skill_name: string
    lesson_started_count : number
    lesson_completed_count : number
    quiz_attempted_count : number
}[]
```

## Creation (POST)

### 🔹 Create New Activity

**POST** `/admin/activity`
**Access:** `@only admin`

#### 🧾 Query Params

```ts
{
  lesson_id?: number
}
```

#### 🧾 Body

```ts
{
  image: string; // Base64
  title: string;
  description: string;
  instructions: string;
  difficulty: string;
  point: number;
  answer_format: text, image or pdf;
}
```

### 🔹 Create New Lesson

**POST** `/admin/lesson`
**Access:** `@only admin`


#### 🧾 Query Params


#### 🧾 Body

```ts
{ skill_id: number
  title: string;
  content: JSON;
  description: string;
  image: string; // Base64
}
```

### 🔹 Create New Badge

**POST** `/admin/badge`
**Access:** `@only admin`

#### 🧾 Body

```ts
{
  title: string;
  description: string;
  image: string; // Base64
  points: number;
}
```

### 🔹 Create New Quiz

**POST** `/admin/quiz`
**Access:** `@only admin`


#### 🧾 Query Params


#### 🧾 Body

```ts
{ lesson_id : number
  image: string; // Base64
  title: string;
  description: string;
  difficulty: string;
  point: number;
  time_duration: number; // in seconds
  questions: {
    question: string;
    options: {
      text: string;
      isCorrect: boolean;
    }
    [];
  }
}
```

## Mutation (PUT)

### 🔹 Update Email

**PUT** `/admin/update_email`
**Access:** `@only admin`

#### 🧾 Body

```ts
{
    email : string
}
```

### 🔹 Update Password

**PUT** `/admin/update_password`
**Access:** `@only admin`

#### 🧾 Body

```ts
{
    oldPassword : string;
    newPassword : string
    confirmPassword : string
}
```

### 🔹 Block Children

**PUT** `/admin/block_children`
**Access:** `@only admin`

#### 🧾 Body

```ts
{
  id : number
}
```

### 🔹 Unblock Children

**PUT** `/admin/unblock_children`
**Access:** `@only admin`

#### 🧾 Body

```ts
{
  id : number
}
```

### 🔹 Block Parent

**PUT** `/admin/block_parent`
**Access:** `@only admin`

#### 🧾 Body

```ts
{
  id : number
}
```

### 🔹 Unblock Children

**PUT** `/admin/unblock_parent`
**Access:** `@only admin`

#### 🧾 Body

```ts
{
  id : number
}
```

### 🔹 Update Activity

**PUT** `/admin/activity`
**Access:** `@only admin`

#### 🧾 Body

```ts
{
  id : number;
  lesson: string | null; // Optional
  image: string | null; // Base64
  title: string | null;
  description: string | null;
  instructions: string | null;
  difficulty: string | null;
  point: number | null;
}
```

### 🔹 Update Quiz

**PUT** `/admin/quiz`
**Access:** `@only admin`

#### 🧾 Body

```ts
{
  id : number
  lesson: string | null;
  image: string | null; // Base64
  title: string | null;
  description: string | null;
  difficulty: string | null;
  point: number | null;
  questions: {
    question: string;
    options: {
      text: string;
      isCorrect: boolean;
    }[];
  }
}

```

### 🔹 Update Lesson

**PUT** `/admin/lesson`
**Access:** `@only admin`

#### 🧾 Body

```ts
{
  id : number;
  title: string | null;
  content: JSON | null;
  image: string | null; // Base64
  description: string | null;
  curriculum_id: number | null;
}
```

## Delete (DELETE)

### 🔹 Delete Badge

**DELETE** `/admin/badge`
**Access:** `@only admin`

#### 🧾 Body

```ts
{
    id : string
}
```

### 🔹 Delete Activity

**DELETE** `/admin/activity`
**Access:** `@only admin`

#### 🧾 Body

```ts
{
    id : string
}
```

### 🔹 Delete Quiz

**DELETE** `/admin/quiz`
**Access:** `@only admin`

#### 🧾 Body

```ts
{
    id : string
}
```

### 🔹 Delete Lesson

**DELETE** `/admin/lesson`
**Access:** `@only admin`

#### 🧾 Body

```ts
{
    id : string
}
```
