# ARCHITECTURE.md

# Agentic RAG Assistant – Architecture Document

## 1. System Overview

This project is a production-style Agentic AI Assistant that evolved from a basic RAG system into a multi-agent orchestration system.

The system supports:

- Retrieval-Augmented Generation
- Tool Calling
- ReAct-style reasoning
- Persistent Memory
- LangGraph-style state management
- Specialist agents
- Supervisor agent orchestration
- Automated evaluation

---

## 2. High-Level Architecture

```text
User
 │
 ▼

Streamlit UI
 │
 ▼

answer_question()
 │
 ▼

create_initial_state()
 │
 ▼

Supervisor Agent
 │
 ├─────────────┬─────────────┬─────────────┐
 ▼             ▼             ▼             ▼

HR Agent   Memory Agent  Utility Agent  RAG Agent
 │             │             │             │
 └─────────────┴─────────────┴─────────────┘
 │
 ▼

Answer Node
 │
 ▼

Final Response
```

---

## 3. Main Components

## app.py

The Streamlit UI layer.

Responsibilities:

- Accept user input
- Call `answer_question()`
- Display agent route
- Display thoughts
- Display observations
- Display final answer
- Display sources
- Display chat history

---

## rag_service.py

The main orchestration layer.

Responsibilities:

- Create initial state
- Run supervisor agent
- Execute specialist agents
- Maintain ReAct loop
- Generate final answer

Main functions:

```python
call_gemini()
react_step()
create_initial_state()
supervisor_agent()
hr_agent()
memory_agent()
utility_agent()
rag_agent()
execute_action_node()
answer_node()
answer_question()
```

---

## tools.py

The tool layer.

Responsibilities:

- Leave balance lookup
- Remaining leave calculation
- Current date retrieval
- Calculator execution

Tools:

```python
calculate_remaining_leave_days()
get_remaining_leave_days()
get_current_date()
calculate()
```

---

## memory_service.py

The persistent memory layer.

Responsibilities:

- Load memory
- Save memory
- Remember facts
- Recall facts

Functions:

```python
load_memory()
save_memory()
remember_fact()
recall_fact()
```

---

## evaluation.py

The evaluation framework.

Responsibilities:

- Run predefined test cases
- Compare expected route with actual route
- Print PASS / FAIL
- Calculate route accuracy

---

## 4. State Management

The project uses a centralized state object.

```python
state = {
    "question": question,
    "results": [],
    "sources": [],
    "actions": [],
    "thoughts": [],
    "observations": [],
    "remaining_leave": None,
    "requested_days": extract_requested_days(question),
    "employee_name": None
}
```

The state object acts as the single source of truth.

Every node receives state, updates state, and returns state.

```text
State
 ↓
Node
 ↓
Updated State
```

Benefits:

- Easier debugging
- Cleaner architecture
- Better extensibility
- LangGraph-style workflow design

---

## 5. Supervisor Agent

The Supervisor Agent is responsible for deciding the next action.

It does not execute business logic.

```python
def supervisor_agent(state):
    action = react_step(
        state["question"],
        state["observations"]
    )

    state["next_action"] = action

    state["thoughts"].append(
        f"Supervisor Agent: I selected {action} as the next action."
    )

    return state
```

Responsibilities:

- Inspect question
- Inspect observations
- Decide next action
- Delegate to specialist agent
- Stop when final answer is ready

---

## 6. Specialist Agents

## HR Agent

Handles leave-related workflows.

Action:

```text
LEAVE_TOOL
```

Responsibilities:

- Extract employee name
- Check leave balance
- Store remaining leave in state
- Add observation

Example:

```text
John has 8 leave days remaining.
```

---

## Memory Agent

Handles memory workflows.

Actions:

```text
MEMORY_READ
MEMORY_WRITE
```

Responsibilities:

- Store user facts
- Retrieve user facts
- Update observations
- Use memory.json as persistent storage

---

## Utility Agent

Handles utility workflows.

Actions:

```text
DATE_TOOL
CALCULATOR_TOOL
```

Responsibilities:

- Get today's date
- Compare leave balance with requested vacation days
- Add calculation observations

---

## RAG Agent

Handles document-based question answering.

Action:

```text
RAG
```

Responsibilities:

- Retrieve relevant chunks from FAISS
- Build context
- Call Gemini
- Generate grounded answer
- Add document sources

---

## 7. ReAct Loop

The agent follows a ReAct-style loop:

```text
Reason
 ↓
Act
 ↓
Observe
 ↓
Reason Again
 ↓
Final Answer
```

Implementation flow:

```text
Supervisor Agent
 ↓
Action
 ↓
Specialist Agent
 ↓
Observation
 ↓
Supervisor Agent
 ↓
Next Action
```

Example:

```text
Question:
Do I have enough leave days to take a 15 day vacation?

Step 1:
Supervisor selects LEAVE_TOOL

Step 2:
HR Agent returns:
Abhi has 12 leave days remaining.

Step 3:
Supervisor selects CALCULATOR_TOOL

Step 4:
Utility Agent returns:
The calculation result is False.

Step 5:
Supervisor selects FINAL

Step 6:
Answer Node generates final response.
```

---

## 8. RAG Pipeline

```text
User Question
 ↓
Embedding Model
 ↓
FAISS Similarity Search
 ↓
Relevant Chunks
 ↓
Gemini
 ↓
Grounded Answer
```

RAG is used for company-document questions.

Example:

```text
How many paid leave days do employees get?
```

The system retrieves the employee handbook chunk and generates an answer using only that context.

---

## 9. Memory Pipeline

## Memory Write

```text
User:
My manager is Priya.

Supervisor Agent
 ↓
MEMORY_WRITE
 ↓
Memory Agent
 ↓
remember_fact("manager", "Priya")
 ↓
memory.json
 ↓
Observation:
Stored manager = Priya
 ↓
FINAL
```

---

## Memory Read

```text
User:
Who is my manager?

Supervisor Agent
 ↓
MEMORY_READ
 ↓
Memory Agent
 ↓
recall_fact("manager")
 ↓
memory.json
 ↓
Observation:
Recalled manager = Priya
 ↓
FINAL
```

---

## 10. Tool Pipeline

Example:

```text
Do I have enough leave days to take a 15 day vacation?
```

Pipeline:

```text
Supervisor Agent
 ↓
LEAVE_TOOL
 ↓
HR Agent
 ↓
Observation:
Abhi has 12 leave days remaining.
 ↓
Supervisor Agent
 ↓
CALCULATOR_TOOL
 ↓
Utility Agent
 ↓
Observation:
The calculation result is False.
 ↓
Answer Node
```

---

## 11. Answer Node

The Answer Node converts state into the final user-facing answer.

Responsibilities:

- Convert raw tool output into natural language
- Use remaining leave and requested days
- Combine results when needed

Example:

```text
Abhi has 12 leave days remaining.

Since your requested vacation is 15 days,
you do not have enough leave available.
```

---

## 12. Error Handling

Gemini calls are centralized in:

```python
call_gemini()
```

It handles:

- API errors
- Quota errors
- Temporary failures
- Retry logic
- Fallback return

Flow:

```text
Call Gemini
 ↓
If success:
Return response
 ↓
If failure:
Retry
 ↓
If still failing:
Return ERROR
```

This prevents Streamlit from crashing.

---

## 13. Duplicate Action Guard

The agent prevents repeated actions.

Problem:

```text
LEAVE_TOOL
LEAVE_TOOL
LEAVE_TOOL
```

Solution:

```python
if action in state["actions"] and action != "FINAL":
    state["observations"].append(
        f"Duplicate action detected: {action}. Stopping agent."
    )
    state["actions"].append("FINAL")
    break
```

This protects the ReAct loop from infinite repetition.

---

## 14. Deterministic Workflow Guard

Some workflows should not rely entirely on LLM reasoning.

Example:

```text
Do I have enough leave days to take a 15 day vacation?
```

Required workflow:

```text
LEAVE_TOOL
 ↓
CALCULATOR_TOOL
 ↓
FINAL
```

Guard:

```python
if "enough leave" in question_lower or "vacation" in question_lower:
    if "leave days remaining" not in observations_text:
        return "LEAVE_TOOL"

    if "calculation result" not in observations_text:
        return "CALCULATOR_TOOL"

    return "FINAL"
```

This guarantees correct workflow execution.

---

## 15. Evaluation Framework

The evaluation framework validates agent behavior.

Test case example:

```python
{
    "question": "Who is my manager?",
    "expected_route": "MEMORY_READ, FINAL"
}
```

Evaluation checks:

```text
Expected Route
vs
Actual Route
```

Metrics:

```text
Passed
Failed
Total
Route Accuracy
```

Example output:

```text
Evaluation Summary
Passed: 1
Failed: 3
Total: 4
Route Accuracy: 25.00%
```

Important finding:

Failures can be caused by:

```text
LLM/API Availability
```

not necessarily:

```text
Agent Logic Failure
```

---

## 16. End-to-End Execution Example

Question:

```text
Do I have enough leave days to take a 15 day vacation?
```

Complete flow:

```text
User Question
      │
      ▼

Streamlit UI
      │
      ▼

answer_question()
      │
      ▼

create_initial_state()
      │
      ▼

Supervisor Agent
      │
      ▼

LEAVE_TOOL
      │
      ▼

HR Agent
      │
      ▼

Observation:
Abhi has 12 leave days remaining.
      │
      ▼

Supervisor Agent
      │
      ▼

CALCULATOR_TOOL
      │
      ▼

Utility Agent
      │
      ▼

Observation:
The calculation result is False.
      │
      ▼

Supervisor Agent
      │
      ▼

FINAL
      │
      ▼

Answer Node
      │
      ▼

Final Response
```

Final response:

```text
Abhi has 12 leave days remaining.

Since your requested vacation is 15 days,
you do not have enough leave available.
```

---

## 17. Scalability Considerations

Current system uses:

```text
JSON memory
Local FAISS index
Streamlit frontend
Gemini API
```

Future scalable version could use:

```text
PostgreSQL
Vector database service
Cloud deployment
Authentication
Monitoring
CI/CD evaluation pipeline
```

---

## 18. Future Improvements

Planned improvements:

```text
1. Deploy application to cloud
2. Replace JSON memory with PostgreSQL
3. Add vector-based memory
4. Add authentication
5. Add monitoring and logging
6. Add CI/CD evaluation pipeline
7. Add human-in-the-loop approval
8. Add real LangGraph implementation
9. Add role-based tools
10. Add production observability
```

---

## 19. Key Architecture Principle

The main design principle is separation of responsibility.

```text
Supervisor Agent
= decision making

Specialist Agents
= task execution

State
= shared memory across nodes

Answer Node
= final response generation
```

This makes the project easier to understand, debug, test, and extend.

---

## 20. Final Summary

This project demonstrates a complete progression from:

```text
Basic RAG
```

to:

```text
Agentic AI Orchestrator
```

using:

```text
RAG
Tool Calling
Memory
ReAct
State Management
Specialist Agents
Supervisor Agent
Evaluation
Reliability Patterns
```

The architecture is designed to be understandable, modular, and interview-ready.