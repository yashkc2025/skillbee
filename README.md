# 🛠️ Software Engineering Project – May 2025

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
type(scope): short description
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
