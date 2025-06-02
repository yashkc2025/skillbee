# 🛠️ Software Engineering Project – May 2025

The below will be how to set up the git repo and everything but i am adding how to run the controllers and do api calls to check if everything is working in backend properly.I have added an extra file db.py because the previous structure was causing a loop between the files.Everything else is the same as Yathin had updated before for the database except for the changes i made in routes.py and the new file controllers.py for the logic.

How to run?
open integrated terminal in directory of backend 
then python run.py
after that we install extension of Rapid API client and follow below instructions:

For context i will be using Rapid API client as an extension in VS code for this.

for parent registration i have the route: ​http://127.0.0.1:5000/auth/parent_register so i will paste this on to the sapce given in the extension then select the required method(post) and send a json body.

the body i used:

{"name":"ub",
"email_id":"ub@gmail.com",
"password":"abc",
"profile_image":""}

and then evaluate whether the correct status code and message are being displayed or not. 

for children registration the route used: http://127.0.0.1:5000/auth/children_register

the body used:
{
  "name":"ubb",
  "email_id": "ub123@gmail.com",
  "password": "abcdef",
  "username": "ubbbbbbb",
  "dob": "2009-09-09",
  "school": "sphs",
  "profile_image": ""
}


please try not to change most things as it will mess up the working code 
I will apply the tokens and all in accordance to frontend team.

Urjaswi Banerjee



Interactive platform for students, parents, and admins with progress tracking, gamified rewards, child account management, and full content control.

## 🚀 Getting Started

Clone the repository and set up your environment:

```bash
# Clone the repo
git clone https://github.com/yashkc2025/soft-engg-project-may-2025-se-May-9.git
cd soft-engg-project-may-2025-se-May-9

# Pull the latest main
git checkout main
git pull origin main
```

## 🧭 Git Workflow & Collaboration Etiquette

Please follow these rules strictly to ensure clean collaboration and project health.

### ✅ Branching Rules

- **Always create a new branch** for features, fixes, or enhancements.

- **Branch naming convention:**

  ```
  yourname-feature-name
  yourname-feature-name-YYYYMMDD (optional date)
  ```

- **Examples:**

  - `yash-login-module`
  - `arpit-dashboard-ui-20250601`

> ✅ Use `git checkout -b branch-name` to create and switch.

### 📤 Never Force Push

- **Never use `git push --force`.**
- Always use:

```bash
git push origin your-branch-name
```

### 🔄 Staying Synced with Main

Before starting or while working on a branch:

```bash
git checkout main
git pull origin main
git checkout your-feature-branch
git rebase origin/main  # or use merge if preferred
```

### 📥 Pull Request (PR) Guidelines

- **Never push directly to `main`**
- All changes must go through a **Pull Request (PR)**
- **Open a Draft PR early** to share progress and gather feedback
- Keep PRs **focused** and **small**
- Reference related issues using keywords like:
  `Closes #issue-number`

### 💬 Review Process

- Use inline comments for suggestions or questions
- Be respectful and constructive
- Never push to someone else's branch without consent

## 🧪 Code Quality Standards

### 🧹 Linting & Formatting

- Run linters and formatters before committing code
- Use stack-specific tools (e.g., ESLint, Prettier, Black)
- Example:

```bash
npm run lint
npm run format
```

### ✅ Testing

- Add tests for new functionality when possible
- Run tests locally before opening a PR:

## ✍️ Commit Message Convention

Use clear, structured commit messages:

```
type: short description
```

**Types:**

- `feat` – New feature
- `fix` – Bug fix
- `docs` – Documentation
- `style` – Formatting
- `refactor` – Code refactor
- `test` – Test-related
- `chore` – Misc tasks

**Examples:**

```
feat: implement login with JWT
fix: fix alignment issue on mobile
```

## 📁 Project Structure

```plaintext
/docs
  *.md
/backend
  ...
/frontend
  ...
```

### Production / CI

- Deployment handled via GitHub Actions (CI/CD)
- Store secrets and keys in `.env` (never commit them)

## Tech Stack

![image](https://github.com/user-attachments/assets/c90b0112-56ef-4b81-9960-1c99ecbddca9)

