# Agentic RAG Assistant

Production-style Agentic AI Assistant built with:

- RAG
- FAISS
- Gemini
- ReAct
- Persistent Memory
- Supervisor Agent
- Specialist Agents
- Evaluation Framework

## Quick Links

- Architecture → ARCHITECTURE.md
- Interview Guide → INTERVIEW_GUIDE.md
- Project Log → PROJECT_LOG.md
- Project Structure → PROJECT_STRUCTURE.md
- Git Workflow → GIT_WORKFLOW.md

## Architecture

![Architecture](screenshots/architecture.png)

# End-to-End Execution Example

This section demonstrates exactly what happens internally when a user asks a question.

---

## Example Question

```text
Do I have enough leave days to take a 15 day vacation?
```

---

## Step 1: User Enters Question

```text
User
↓
Streamlit UI (app.py)
```

The question is captured from the Streamlit interface and passed to:

```python
answer_question(question)
```

---

## Step 2: Create Initial State

The system creates a centralized state object.

```python
state = {
    "question": "Do I have enough leave days to take a 15 day vacation?",
    "results": [],
    "sources": [],
    "actions": [],
    "thoughts": [],
    "observations": [],
    "remaining_leave": None,
    "requested_days": 15,
    "employee_name": None
}
```

---

## Step 3: Supervisor Agent

The Supervisor Agent examines:

```text
Question
Current State
Previous Observations
```

and decides:

```text
LEAVE_TOOL
```

The decision is recorded:

```text
Supervisor Agent:
I selected LEAVE_TOOL as the next action.
```

---

## Step 4: HR Agent

The request is delegated to:

```text
HR Agent
```

The HR Agent:

```text
Extracts employee name
Checks leave balance
Stores result
```

Example:

```text
Abhi has 12 leave days remaining.
```

State Update:

```python
state["remaining_leave"] = 12
```

Observation:

```text
Abhi has 12 leave days remaining.
```

---

## Step 5: Supervisor Agent Re-Evaluates

The Supervisor Agent now sees:

```text
Remaining leave balance available
Requested vacation = 15 days
```

It decides:

```text
CALCULATOR_TOOL
```

Recorded thought:

```text
Supervisor Agent:
I selected CALCULATOR_TOOL as the next action.
```

---

## Step 6: Utility Agent

The Utility Agent performs:

```text
12 >= 15
```

Result:

```text
False
```

Observation:

```text
The calculation result is False.
```

---

## Step 7: Supervisor Agent Re-Evaluates Again

Current observations:

```text
Abhi has 12 leave days remaining.
The calculation result is False.
```

The workflow is complete.

Supervisor decides:

```text
FINAL
```

---

## Step 8: Answer Node

The Answer Node converts observations into a business-friendly response.

Instead of:

```text
False
```

the user receives:

```text
Abhi has 12 leave days remaining.

Since your requested vacation is 15 days,
you do not have enough leave available.
```

---

## Step 9: Streamlit Displays Results

The UI shows:

### Route

```text
LEAVE_TOOL
CALCULATOR_TOOL
FINAL
```

### Scratchpad

```text
Supervisor Agent:
I selected LEAVE_TOOL as the next action.

HR Agent:
I need to check the employee's remaining leave balance.

Supervisor Agent:
I selected CALCULATOR_TOOL as the next action.

Utility Agent:
I need to compare the remaining leave days with the requested vacation days.

Supervisor Agent:
I selected FINAL as the next action.
```

### Observations

```text
Abhi has 12 leave days remaining.
The calculation result is False.
```

### Final Answer

```text
Abhi has 12 leave days remaining.

Since your requested vacation is 15 days,
you do not have enough leave available.
```

---

## Complete Flow Diagram

```text
User Question
      │
      ▼

 Streamlit UI
      │
      ▼

 create_initial_state()
      │
      ▼

 Supervisor Agent
      │
      ▼

 HR Agent
      │
      ▼

 Observation:
 12 leave days
      │
      ▼

 Supervisor Agent
      │
      ▼

 Utility Agent
      │
      ▼

 Observation:
 False
      │
      ▼

 Supervisor Agent
      │
      ▼

 Answer Node
      │
      ▼

 Final Answer
      │
      ▼

 Streamlit UI
```

---

## Why This Architecture Matters

This project separates:

```text
Decision Making
```

from

```text
Task Execution
```

The Supervisor Agent decides:

```text
What should happen next?
```

The Specialist Agents execute:

```text
HR Agent
Memory Agent
Utility Agent
RAG Agent
```

This mirrors how modern agent frameworks such as LangGraph, CrewAI, and enterprise multi-agent systems are designed.


# Memory Lifecycle Example

This section explains exactly how memory works inside the agent.

The project implements persistent memory using:

```text
memory.json
memory_service.py
```

The memory system allows the agent to remember facts across multiple conversations and application restarts.

---

## Example 1: Writing Memory

### User Question

```text
My manager is Priya.
```

---

### Step 1: Streamlit UI

The question is sent to:

```python
answer_question(question)
```

---

### Step 2: Create Initial State

```python
state = {
    "question": "My manager is Priya.",
    ...
}
```

---

### Step 3: Supervisor Agent

The supervisor analyzes:

```text
Question:
My manager is Priya.
```

The ReAct planner determines:

```text
MEMORY_WRITE
```

Recorded thought:

```text
Supervisor Agent:
I selected MEMORY_WRITE as the next action.
```

---

### Step 4: Memory Agent

The Memory Agent executes:

```python
remember_fact(
    "manager",
    "Priya"
)
```

---

### Step 5: memory_service.py

The helper function:

```python
remember_fact(key, value)
```

performs:

```python
memory[key] = value
```

Example:

```python
memory["manager"] = "Priya"
```

---

### Step 6: Save To Disk

The updated memory is written into:

```text
memory.json
```

Example:

```json
{
    "manager": "Priya"
}
```

---

### Step 7: Observation Created

The Memory Agent records:

```text
Stored manager = Priya
```

The observation is added to:

```python
state["observations"]
```

---

### Step 8: Supervisor Agent

The Supervisor sees:

```text
Stored manager = Priya
```

The stopping rule triggers:

```text
FINAL
```

---

### Step 9: Final Response

The user receives:

```text
Okay, I will remember that your manager is Priya.
```

---

## Memory Write Flow

```text
User Question
      │
      ▼

Supervisor Agent
      │
      ▼

MEMORY_WRITE
      │
      ▼

Memory Agent
      │
      ▼

remember_fact()
      │
      ▼

memory.json
      │
      ▼

Observation
      │
      ▼

FINAL
      │
      ▼

User Response
```

---

# Example 2: Reading Memory

### User Question

```text
Who is my manager?
```

---

### Step 1: Supervisor Agent

Planner decides:

```text
MEMORY_READ
```

Recorded thought:

```text
Supervisor Agent:
I selected MEMORY_READ as the next action.
```

---

### Step 2: Memory Agent

Memory Agent executes:

```python
recall_fact("manager")
```

---

### Step 3: memory_service.py

The function:

```python
recall_fact(key)
```

loads:

```text
memory.json
```

Example:

```json
{
    "manager": "Priya"
}
```

and returns:

```text
Priya
```

---

### Step 4: Observation Created

Observation:

```text
Recalled manager = Priya
```

stored inside:

```python
state["observations"]
```

---

### Step 5: Supervisor Agent

Supervisor sees:

```text
Recalled manager = Priya
```

Stopping rule:

```text
FINAL
```

---

### Step 6: Final Response

The user receives:

```text
Your manager is Priya.
```

---

## Memory Read Flow

```text
User Question
      │
      ▼

Supervisor Agent
      │
      ▼

MEMORY_READ
      │
      ▼

Memory Agent
      │
      ▼

recall_fact()
      │
      ▼

memory.json
      │
      ▼

Observation
      │
      ▼

FINAL
      │
      ▼

User Response
```

---

# Why Memory Is Implemented As A Tool

Originally memory was handled with:

```python
if "manager" in question:
    ...
```

This approach does not scale.

Instead, memory became a first-class tool:

```text
MEMORY_READ
MEMORY_WRITE
```

inside the ReAct loop.

This means memory is treated exactly like:

```text
LEAVE_TOOL
DATE_TOOL
CALCULATOR_TOOL
RAG
```

which makes the architecture more modular and closer to production agent frameworks.

---

# Memory Architecture

```text
                 Supervisor Agent
                         │
                         ▼

                 Memory Agent
                         │
            ┌────────────┴────────────┐
            ▼                         ▼

     remember_fact()           recall_fact()
            │                         │
            ▼                         ▼

                  memory.json
```

---

# Key Learning

Memory is not just data storage.

The memory system demonstrates:

```text
Persistent Storage
Tool-Based Memory Access
Agent-Controlled Memory
Observation Generation
State Updates
Multi-Step Reasoning
```

The Supervisor decides when memory should be accessed.

The Memory Agent performs the operation.

The memory service reads/writes data.

The observation is returned to the ReAct loop.

The Supervisor decides what happens next.