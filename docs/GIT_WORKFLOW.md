# Git Workflow Documentation

## Purpose

This document records the Git and GitHub workflow used to version-control and publish the Agentic RAG Assistant project.

---

## Step 1: Initialize Git Repository

```bash
git init
```

This created a local Git repository inside the project folder.

---

## Step 2: Check Repository Status

```bash
git status
```

Initially, Git showed all project files as untracked.

---

## Step 3: Add .gitignore

Created `.gitignore` to avoid committing local or sensitive files.

Ignored files/folders:

```text
venv/
.env
__pycache__/
*.pyc
.streamlit/
.vscode/
.idea/
memory.json
installed_packages.txt
```

Purpose:

- Prevent API keys from being uploaded
- Prevent virtual environment files from being committed
- Prevent runtime memory data from being committed
- Keep repository clean

---

## Step 4: Stage Project Files

```bash
git add .
```

This staged all allowed project files for commit.

---

## Step 5: Verify Staged Files

```bash
git status
```

Confirmed that important files were staged:

```text
README.md
ARCHITECTURE.md
INTERVIEW_GUIDE.md
PROJECT_LOG.md
PROJECT_STRUCTURE.md
app.py
rag_service.py
tools.py
memory_service.py
evaluation.py
requirements.txt
data/
vector_store/
screenshots/
```

Confirmed sensitive files were not staged:

```text
.env
venv/
memory.json
```

---

## Step 6: Create First Commit

```bash
git commit -m "Complete Agentic RAG Assistant project"
```

This created the first Git commit containing the completed project.

---

## Step 7: Create GitHub Repository

Created a GitHub repository named:

```text
agentic-rag-assistant
```

Repository description:

```text
Production-style Agentic AI Assistant built with RAG, FAISS, Gemini, ReAct reasoning, persistent memory, supervisor-specialist agents, and automated evaluation.
```

---

## Step 8: Add GitHub Remote

```bash
git remote add origin https://github.com/Abhinav150526/agentic-rag-assistant.git
```

If Git shows:

```text
error: remote origin already exists
```

that means the remote was already configured.

Verify with:

```bash
git remote -v
```

Expected:

```text
origin  https://github.com/Abhinav150526/agentic-rag-assistant.git (fetch)
origin  https://github.com/Abhinav150526/agentic-rag-assistant.git (push)
```

---

## Step 9: Rename Branch to main

```bash
git branch -M main
```

Verify:

```bash
git branch
```

Expected:

```text
* main
```

---

## Step 10: Push to GitHub

```bash
git push -u origin main
```

During this step, GitHub authentication may open in the browser.

After successful authentication, the local repository is pushed to GitHub.

---

## Step 11: Verify GitHub Repository

Opened GitHub repository and confirmed that all files were visible.

Repository:

```text
https://github.com/Abhinav150526/agentic-rag-assistant
```

---

# Common Git Commands Used

## Check Status

```bash
git status
```

Shows current file changes.

---

## Stage Changes

```bash
git add .
```

Stages all allowed files.

---

## Commit Changes

```bash
git commit -m "message"
```

Creates a snapshot of the project.

---

## Check Remote

```bash
git remote -v
```

Shows connected GitHub repository.

---

## Push Changes

```bash
git push
```

Uploads committed changes to GitHub.

---

# Future Workflow

For future code changes:

```bash
git status
git add .
git commit -m "Describe the change"
git push
```

Example:

```bash
git add .
git commit -m "Add Streamlit deployment configuration"
git push
```

---

# Key Learning

Git is used for local version control.

GitHub is used for remote hosting and sharing.

`.gitignore` protects secrets, local files, and runtime data from being committed.

The final project is now version-controlled, documented, and publicly shareable.