# PROJECT LOG - RAG to Agentic AI Journey

## Project Goal

Build a production-style AI Assistant that evolves from:

Basic RAG → Conversational RAG → Tool Calling → Multi-Tool Agent → ReAct Agent

---

# Milestone 1: Basic RAG System

Status: Completed

Objective:
Build a Retrieval-Augmented Generation (RAG) application capable of answering questions from company documents.

Files:

* app.py
* rag_service.py
* vector_store.py
* documents/

Implementation:

* Loaded company documents
* Created embeddings
* Stored vectors in FAISS
* Retrieved relevant chunks
* Sent retrieved context to Gemini
* Generated grounded answers

Architecture:

User Question
↓
FAISS Retrieval
↓
Relevant Chunks
↓
Gemini
↓
Answer

Outcome:
Successfully answered questions from local documents.

---

# Milestone 2: Conversational RAG

Status: Completed

Objective:
Allow follow-up questions to understand previous conversation context.

Files Modified:

* app.py
* rag_service.py

Implementation:

* Added chat history
* Stored conversation using Streamlit session state
* Passed previous messages to Gemini

Example:

Q1: What is FAISS?
Q2: Who created it?

Assistant understands:
"it" = FAISS

Architecture:

Question
↓
Chat History
↓
RAG Retrieval
↓
Gemini
↓
Answer

Outcome:
Assistant became conversational instead of single-turn.

---

# Milestone 3: Environment Variable Management

Status: Completed

Objective:
Remove hardcoded API keys.

Files Modified:

* .env
* rag_service.py

Implementation:

* Created .env file
* Stored Gemini API key securely
* Loaded key using environment variables

Outcome:
Project became deployment-friendly and secure.

---

# Milestone 4: Similarity Score Debugging

Status: Completed

Objective:
Understand retrieval quality.

Files Modified:

* vector_store.py

Implementation:

* Printed FAISS distances
* Printed retrieved chunk indices

Example Output:

Distances:
[[0.68 1.85 1.86]]

Indices:
[[5 11 2]]

Outcome:
Learned how retrieval quality is measured.

---

# Milestone 5: Tool Calling Foundation

Status: Completed

Objective:
Allow assistant to use tools instead of only RAG.

Files Added:

* tools.py

Implementation:

* Created Leave Balance Tool

Tool:

calculate_remaining_leave_days()

Example:

Question:
How many leave days do I have?

Output:
Abhi has 12 leave days remaining.

Outcome:
Assistant can execute tools.

---

# Milestone 6: LLM-Based Routing

Status: Completed

Objective:
Allow Gemini to decide when tools should be used.

Files Modified:

* rag_service.py

Implementation:

* Created should_use_leave_tool()
* Gemini decides YES or NO

Architecture:

Question
↓
Gemini Router
↓
Tool OR RAG

Outcome:
Moved from hardcoded routing to LLM routing.

---

# Milestone 7: Multi-Tool Routing

Status: Completed

Objective:
Allow multiple tools.

Tools Added:

* Leave Tool
* Date Tool

Files Modified:

* tools.py
* rag_service.py

Implementation:

* Added get_current_date()
* Added select_route()

Routes:

* LEAVE_TOOL
* DATE_TOOL
* RAG

Architecture:

Question
↓
Gemini Router
↓
Select Route
↓
Execute Route

Outcome:
Assistant can choose between multiple tools.

---

# Milestone 8: Agent Planning

Status: Completed

Objective:
Allow planner to choose multiple actions.

Files Modified:

* rag_service.py

Implementation:

* Replaced select_route()
* Added select_actions()

Example:

Question:
How many leave days do I have and what is today's date?

Planner Output:

[
"LEAVE_TOOL",
"DATE_TOOL"
]

Outcome:
Planner can generate action lists.

---

# Milestone 9: Agent Execution Loop

Status: Completed

Objective:
Execute multiple actions.

Files Modified:

* rag_service.py

Implementation:

for action in actions:
...

Architecture:

Question
↓
Plan Actions
↓
Execute Action 1
↓
Execute Action 2
↓
Combine Results

Outcome:
Assistant performs multiple actions in one request.

---

# Milestone 10: Calculator Tool

Status: Completed

Files Modified:

* tools.py
* rag_service.py

Implementation:

* Added calculate()

Example:

calculate("12 >= 10")

Output:

True

Outcome:
Agent gained calculation capability.

---

# Milestone 11: Observation Passing

Status: Completed

Objective:
Allow later actions to use previous observations.

Files Modified:

* tools.py
* rag_service.py

Implementation:

* Added get_remaining_leave_days()
* Stored remaining_leave variable
* Passed observation to calculator

Example:

Leave Tool:
12

Calculator:
12 >= 15

Result:
False

Outcome:
Agent actions now depend on previous tool outputs.

---

# Milestone 12: Dynamic Information Extraction

Status: Completed

Files Modified:

* rag_service.py

Implementation:

* Added extract_requested_days()
* Extracted vacation days from user question

Examples:

10-day vacation → 10
15-day vacation → 15

Outcome:
Removed hardcoded vacation length.

---

# Milestone 13: Agent Reasoning Layer

Status: Completed

Objective:
Generate business conclusions from observations.

Files Modified:

* rag_service.py

Before:

The calculation result is False.

After:

You have 12 leave days remaining.

Since your requested vacation is 15 days, you do not have enough leave available.

Architecture:

Observation
↓
Reasoning
↓
Natural Language Conclusion

Outcome:
Agent produces business-friendly answers instead of raw tool outputs.

---

# Current Architecture

User Question
↓
Gemini Planner
↓
Action List
↓
Agent Execution Loop
↓
Tool Observations
↓
Reasoning Layer
↓
Final Answer

---

Milestone 14: Agent Scratchpad (ReAct Foundation)

Status: Completed

Objective:
Make the agent's internal reasoning visible.

Files Modified:

rag_service.py
app.py

Implementation:

Added agent memory structures:

thoughts = []
observations = []

Agent now records:

thoughts.append(...)
observations.append(...)

for every tool execution.

Examples:

Leave Tool:

Thought:
I need to check the employee's remaining leave balance.

Observation:
Abhi has 12 leave days remaining.

Calculator Tool:

Thought:
I need to compare the remaining leave days with the requested vacation days.

Observation:
The calculation result is False.

UI Changes:

Added Agent Scratchpad section to Streamlit.

Displayed:

Agent Route
Thoughts
Observations
Final Answer
Sources

Architecture:

Question
↓
Planner
↓
Action List
↓
Thought
↓
Tool Execution
↓
Observation
↓
Thought
↓
Tool Execution
↓
Observation
↓
Reasoning
↓
Final Answer

Example:

Question:
Do I have enough leave days to take a 15 day vacation?

Route:

LEAVE_TOOL, CALCULATOR_TOOL

Scratchpad:

Thought:
I need to check the employee's remaining leave balance.

Observation:
Abhi has 12 leave days remaining.

Thought:
I need to compare the remaining leave days with the requested vacation days.

Observation:
The calculation result is False.

Final Answer:

You have 12 leave days remaining.

Since your requested vacation is 15 days, you do not have enough leave available.

Outcome:

Agent reasoning is now observable.
Tool execution is traceable.
Observations are visible.
Foundation for ReAct-style agents established.


---

# Milestone 15: LLM-Based Entity Extraction

Status: Completed

Objective:
Allow the agent to extract employee names dynamically from user questions instead of relying on hardcoded employee matching.

Files Modified:
- rag_service.py

Implementation:
- Replaced hardcoded employee matching with Gemini-based employee extraction.
- Added logic to extract names like John, Sarah, Michael, etc.
- Added fallback behavior for "I", "me", or "my" to return Abhi.
- Passed extracted employee name into leave tools dynamically.

Example 1:

Question:
How many leave days does John have?

Route:
LEAVE_TOOL, FINAL

Observation:
John has 8 leave days remaining.

Answer:
John has 8 leave days remaining.

Example 2:

Question:
How many leave days does Michael have?

Route:
LEAVE_TOOL, FINAL

Observation:
Employee not found.

Answer:
Employee not found.

Agent Improvement:
- Before: get_remaining_leave_days("abhi")
- After: get_remaining_leave_days(employee_name)

Additional Fix:
- Added stopping condition in react_step()
- If observation contains "Employee not found", agent returns FINAL instead of repeating LEAVE_TOOL.

Outcome:
Agent now supports dynamic tool arguments using LLM-based entity extraction.

# Milestone 16: Persistent Agent Memory

Status: Completed

Objective:
Allow the agent to remember user-specific facts across questions and sessions.

Files Added:
- memory.json
- memory_service.py

Files Modified:
- rag_service.py

Implementation:
- Created memory.json as a lightweight persistent storage file.
- Created memory_service.py with:
  - load_memory()
  - save_memory()
  - remember_fact()
  - recall_fact()
- Added memory write behavior.
- Added memory read behavior.

Example 1:

Question:
My manager is Raj.

Answer:
Okay, I will remember that your manager is Raj.

Route:
MEMORY_WRITE

Observation:
Stored manager = Raj

Example 2:

Question:
Who is my manager?

Answer:
Your manager is Raj.

Route:
MEMORY_READ

Observation:
Recalled manager = Raj

Outcome:
The agent now supports persistent memory using a local JSON file.

---

# Milestone 17: Memory as a Tool

Status: Completed

Objective:
Move memory operations into the ReAct agent loop instead of handling memory with hardcoded early-return logic.

Files Modified:
- rag_service.py
- memory_service.py
- memory.json

Implementation:
- Added MEMORY_WRITE as a ReAct action.
- Added MEMORY_READ as a ReAct action.
- Updated react_step() prompt to understand memory actions.
- Added memory execution blocks inside the agent loop.
- Removed old hardcoded memory if-statements.
- Added stopping conditions:
  - If observation contains "Stored manager", return FINAL.
  - If observation contains "Recalled manager", return FINAL.

Example 1:

Question:
My manager is Priya.

Route:
MEMORY_WRITE, FINAL

Observation:
Stored manager = Priya

Answer:
Okay, I will remember that your manager is Priya.

Example 2:

Question:
Who is my manager?

Route:
MEMORY_READ, FINAL

Observation:
Recalled manager = Priya

Answer:
Your manager is Priya.

Outcome:
Memory is now treated as a first-class tool inside the ReAct agent loop.


---

# Milestone 18: LangGraph-Style State Management

Status: Completed

## Objective

Refactor scattered agent variables into a single state object, similar to how LangGraph manages agent state.

---

## Files Modified

- rag_service.py

---

## Before

Agent state was spread across multiple variables:

```python
results = []
sources = []
actions = []

thoughts = []
observations = []

remaining_leave = None
requested_days = extract_requested_days(question)
employee_name = extract_employee_name(question)
```

Problems:

- State was scattered across many variables.
- Difficult to track what the agent currently knows.
- Harder to extend with new capabilities.
- Not aligned with production agent frameworks.

---

## After

Introduced a centralized state object:

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

---

## Refactoring Performed

### ReAct Loop

Before:

```python
action = react_step(question, observations)
actions.append(action)
```

After:

```python
action = react_step(
    state["question"],
    state["observations"]
)

state["actions"].append(action)
```

---

### Leave Tool

Before:

```python
thoughts.append(...)
remaining_leave = ...
observations.append(...)
results.append(...)
sources.append(...)
```

After:

```python
state["thoughts"].append(...)
state["remaining_leave"] = ...
state["observations"].append(...)
state["results"].append(...)
state["sources"].append(...)
```

---

### Calculator Tool

Before:

```python
if remaining_leave is not None:
```

After:

```python
if state["remaining_leave"] is not None:
```

---

### Date Tool

Before:

```python
observations.append(...)
results.append(...)
sources.append(...)
```

After:

```python
state["observations"].append(...)
state["results"].append(...)
state["sources"].append(...)
```

---

### Memory Tools

Before:

```python
thoughts.append(...)
observations.append(...)
results.append(...)
sources.append(...)
```

After:

```python
state["thoughts"].append(...)
state["observations"].append(...)
state["results"].append(...)
state["sources"].append(...)
```

---

### RAG Tool

Before:

```python
retrieved_chunks = retrieve_chunks(question)
rag_answer = generate_answer(question, retrieved_chunks)
```

After:

```python
retrieved_chunks = retrieve_chunks(state["question"])

rag_answer = generate_answer(
    state["question"],
    retrieved_chunks
)
```

---

## Lazy Employee Extraction

Before:

```python
employee_name = extract_employee_name(question)
```

This executed for every question.

Examples:

- Who is my manager?
- What is today's date?
- What is FAISS?

Even when employee information was not needed.

---

### Improvement

State now starts with:

```python
"employee_name": None
```

Employee extraction occurs only when LEAVE_TOOL is executed:

```python
if state["employee_name"] is None:
    state["employee_name"] = extract_employee_name(
        state["question"]
    )
```

Benefits:

- Reduces unnecessary LLM calls.
- Improves efficiency.
- More production-oriented architecture.

---

## Architecture Evolution

### Before

```text
Question
│
├── thoughts
├── observations
├── results
├── sources
├── employee_name
├── requested_days
└── remaining_leave
```

State distributed across many variables.

---

### After

```text
Question
        │
        ▼

      State
        │
        ├── question
        ├── thoughts
        ├── observations
        ├── actions
        ├── results
        ├── sources
        ├── employee_name
        ├── requested_days
        └── remaining_leave
```

Single source of truth.

---

## Outcome

Successfully migrated the agent toward a LangGraph-style architecture.

## Key Learning

Production agent frameworks such as LangGraph pass a shared state object between nodes.

This milestone introduces the same architectural concept into the custom agent implementation.


---

# Milestone 19: LLM Cost Optimization & Agent Reliability

Status: Completed

## Objective

Improve the reliability and maintainability of the agent by centralizing Gemini calls, adding error handling, retry logic, fallback behavior, and duplicate-action protection.

---

## Files Modified

- rag_service.py

---

## Problem

Gemini API calls were repeated across multiple functions:

```python
generate_answer()
react_step()
extract_employee_name()
select_actions()
select_route()
should_use_leave_tool()
```

This caused:

- Code duplication
- Harder maintenance
- Repeated client initialization
- Scattered error handling
- More chances of app crashes during API failures

---

## Implementation

### Centralized Gemini Helper

Created:

```python
def call_gemini(prompt, retries=2):
    ...
```

This function now handles all Gemini API communication.

---

## Added Retry Logic

If Gemini fails temporarily, the system retries before returning an error.

Flow:

```text
Attempt 1
↓
If failed, wait 2 seconds
↓
Attempt 2
↓
If failed, wait 2 seconds
↓
Attempt 3
↓
Return ERROR if still failing
```

---

## Added Error Handling

Before:

```text
Gemini failure
↓
Streamlit crash
↓
Traceback shown to user
```

After:

```text
Gemini failure
↓
call_gemini() catches error
↓
Returns ERROR
↓
Agent handles fallback safely
```

---

## Updated Functions

The following functions now use `call_gemini()`:

- generate_answer()
- react_step()
- extract_employee_name()

---

## Fallback Behavior

### react_step()

If Gemini fails:

```python
return "FINAL"
```

This prevents the agent from continuing blindly.

---

### extract_employee_name()

If Gemini fails:

```python
return "abhi"
```

This provides a safe default user fallback.

---

## Duplicate Action Guard

Added protection against repeated actions inside the ReAct loop.

Before:

```text
LEAVE_TOOL
LEAVE_TOOL
LEAVE_TOOL
```

or:

```text
MEMORY_WRITE
MEMORY_WRITE
MEMORY_WRITE
```

After:

```text
Duplicate action detected
↓
Agent stops safely
```

Implemented guard:

```python
if action in state["actions"] and action != "FINAL":
    state["observations"].append(
        f"Duplicate action detected: {action}. Stopping agent."
    )
    state["actions"].append("FINAL")
    break
```

---

## Test Case

Question:

```text
Who is my manager?
```

Result:

```text
Agent Route:
MEMORY_READ, FINAL
```

Scratchpad:

```text
Thought:
I should retrieve the stored fact from memory.

Observation:
Recalled manager = Raj
```

Answer:

```text
Your manager is Raj.
```

---

## Outcome

Completed reliability improvements:

- Centralized Gemini calls ✅
- Reduced code duplication ✅
- Added retry logic ✅
- Added graceful fallback behavior ✅
- Prevented repeated tool execution ✅
- Improved production readiness ✅

---

## Key Learning

Production AI systems must handle unreliable external APIs.

LLM calls can fail because of:

- Quota limits
- Server overload
- Network issues
- Rate limits
- Temporary unavailability

A reliable agent should not crash when the LLM fails.

It should:

```text
Catch error
↓
Retry
↓
Fallback
↓
Stop safely
```

# Milestone 20: LangGraph Style Migration

Status: Completed

Created Nodes:

- create_initial_state()
- planner_node()
- execute_action_node()
- answer_node()

Refactored Architecture:

Before:

answer_question()
├─ planning
├─ tool execution
├─ answer generation

After:

create_initial_state()
↓
planner_node()
↓
execute_action_node()
↓
answer_node()

All nodes communicate through shared state.

Key Learning:

LangGraph-style systems pass a shared state object between nodes rather than passing many independent variables.

---

# Milestone 21: Specialist Agents

Status: Completed

## Objective

Split the generic tool execution logic into specialist agents.

---

## Files Modified

- rag_service.py

---

## Problem

Previously, `execute_action_node()` directly handled all tool logic:

```text
MEMORY_READ
MEMORY_WRITE
LEAVE_TOOL
DATE_TOOL
CALCULATOR_TOOL
RAG
```

This made the executor responsible for too many domains.

---

## Implementation

Created specialist agents:

```python
hr_agent(state)
memory_agent(state)
utility_agent(state)
rag_agent(state)
```

---

## HR Agent

Responsible for leave-related workflows.

Handles:

```text
LEAVE_TOOL
```

Example:

```text
Question:
How many leave days does John have?

Route:
LEAVE_TOOL, FINAL

Thought:
HR Agent: I need to check the employee's remaining leave balance.

Observation:
John has 8 leave days remaining.
```

---

## Memory Agent

Responsible for persistent memory workflows.

Handles:

```text
MEMORY_READ
MEMORY_WRITE
```

Example:

```text
Question:
Who is my manager?

Route:
MEMORY_READ, FINAL

Thought:
Memory Agent: I should retrieve the stored fact from memory.

Observation:
Recalled manager = Raj
```

---

## Utility Agent

Responsible for utility-style tasks.

Handles:

```text
DATE_TOOL
CALCULATOR_TOOL
```

Example:

```text
Question:
Do I have enough leave days to take a 15 day vacation?

Route:
LEAVE_TOOL, CALCULATOR_TOOL, FINAL

Thoughts:
HR Agent: I need to check the employee's remaining leave balance.
Utility Agent: I need to compare the remaining leave days with the requested vacation days.

Observations:
Abhi has 12 leave days remaining.
The calculation result is False.
```

---

## RAG Agent

Responsible for document-based question answering.

Handles:

```text
RAG
```

Example:

```text
Question:
How many paid leave days do employees get?

Route:
RAG, FINAL

Observation:
RAG answer generated.

Answer:
Employees get 20 paid leave days per year.
```

---

## Updated Architecture

Before:

```text
planner_node()
↓
execute_action_node()
↓
Tool logic directly inside executor
```

After:

```text
planner_node()
↓
execute_action_node()
↓
Specialist Agent
↓
answer_node()
```

---

## Dispatcher Pattern

`execute_action_node()` now acts more like a dispatcher:

```python
if action in ["MEMORY_READ", "MEMORY_WRITE"]:
    state = memory_agent(state)

elif action == "LEAVE_TOOL":
    state = hr_agent(state)

elif action in ["DATE_TOOL", "CALCULATOR_TOOL"]:
    state = utility_agent(state)

elif action == "RAG":
    state = rag_agent(state)
```

---

## Outcome

Completed specialist agents:

- HR Agent ✅
- Memory Agent ✅
- Utility Agent ✅
- RAG Agent ✅

The system is now closer to a true multi-agent architecture.

---

## Key Learning

A specialist-agent architecture separates domain responsibility.

Instead of one executor containing all business logic, each specialist owns one domain:

```text
HR Agent       → leave workflows
Memory Agent   → memory workflows
Utility Agent  → date/calculation workflows
RAG Agent      → document retrieval workflows
```

This improves maintainability, testing, scaling, and interview-level architecture explanation.

---
# Milestone 22: Supervisor / Orchestrator Agent

Status: Completed

---

## Objective

Create a supervisor agent that controls which specialist agent should act next.

---

## Specialist Agents Available

- HR Agent
- Memory Agent
- Utility Agent
- RAG Agent

---

## Implementation

Created:

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

Updated `answer_question()` to use:

```python
state = supervisor_agent(state)
```

instead of directly calling `planner_node()`.

---

## Final Architecture

```text
User Question
↓
create_initial_state()
↓
Supervisor Agent
↓
Specialist Agent
↓
Observation
↓
Supervisor Agent
↓
Final Answer
```

---

## Example Workflow

### Question

```text
Do I have enough leave days to take a 15 day vacation?
```

### Route

```text
LEAVE_TOOL, CALCULATOR_TOOL, FINAL
```

### Scratchpad

```text
Supervisor Agent: I selected LEAVE_TOOL as the next action.
HR Agent: I need to check the employee's remaining leave balance.

Supervisor Agent: I selected CALCULATOR_TOOL as the next action.
Utility Agent: I need to compare the remaining leave days with the requested vacation days.

Supervisor Agent: I selected FINAL as the next action.
```

### Observations

```text
Abhi has 12 leave days remaining.
The calculation result is False.
```

### Answer

```text
Abhi has 12 leave days remaining.

Since your requested vacation is 15 days, you do not have enough leave available.
```

---

## Reliability Improvement

Added deterministic workflow guard for leave-comparison questions.

```python
question_lower = question.lower()
observations_text = " ".join(observations).lower()

if "enough leave" in question_lower or "vacation" in question_lower:
    if "leave days remaining" not in observations_text:
        return "LEAVE_TOOL"

    if "calculation result" not in observations_text:
        return "CALCULATOR_TOOL"

    return "FINAL"
```

This guarantees the workflow:

```text
LEAVE_TOOL
↓
CALCULATOR_TOOL
↓
FINAL
```

instead of relying entirely on LLM reasoning.

---

## Supervisor Pattern

The supervisor does not execute business logic.

Its responsibility is:

```text
Observe Current State
↓
Choose Next Action
↓
Delegate To Specialist Agent
↓
Receive Observation
↓
Choose Next Action
```

This follows the same orchestration pattern used in modern agent frameworks.

---

## Outcome

Completed:

- Supervisor Agent ✅
- Specialist Agent Routing ✅
- Multi-step Workflow Control ✅
- Observation-driven Orchestration ✅
- Deterministic Workflow Guard ✅

---

## Final System Architecture

```text
                Supervisor Agent
                        │
        ┌───────────────┼───────────────┐
        │               │               │
        ▼               ▼               ▼

    HR Agent      Memory Agent     Utility Agent
        │               │               │
        └───────────────┼───────────────┘
                        │
                        ▼

                   RAG Agent
                        │
                        ▼

                   Answer Node
```

---

## Interview Explanation

This milestone introduced a Supervisor Agent responsible for orchestrating specialist agents.

Instead of executing all business logic directly, the supervisor evaluates the current state and observations, selects the next action, and delegates execution to the appropriate specialist agent.

This architecture improves scalability, maintainability, and extensibility while aligning with modern multi-agent AI system design patterns.

---

## Key Learning

A true AI orchestrator separates:

```text
Decision Making
```

from

```text
Task Execution
```

The supervisor decides.

The specialists execute.

---

## Next Planned Milestone

### Milestone 23: Evaluation Framework

Goal:

Create automated tests for:

- Agent routes
- Tool selection
- Multi-step workflows
- Memory operations
- RAG operations
- Final answers

This will allow systematic validation of agent behavior before deployment.

---

# Milestone 23: Evaluation Framework

Status: Completed

## Objective

Create an automated evaluation framework to validate agent behavior.

---

## Files Added

- evaluation.py

---

## Problem

Before this milestone, testing was manual.

Examples:

```text
Who is my manager?
What is today's date?
How many leave days does John have?
Do I have enough leave days to take a 15 day vacation?
```

Each question had to be typed manually into Streamlit.

Manual testing does not scale as the agent grows.

---

## Implementation

Created `evaluation.py`.

It imports:

```python
from rag_service import answer_question
```

Defined test cases:

```python
TEST_CASES = [
    {
        "question": "Who is my manager?",
        "expected_route": "MEMORY_READ, FINAL"
    },
    {
        "question": "What is today's date?",
        "expected_route": "DATE_TOOL, FINAL"
    },
    {
        "question": "How many leave days does John have?",
        "expected_route": "LEAVE_TOOL, FINAL"
    },
    {
        "question": "Do I have enough leave days to take a 15 day vacation?",
        "expected_route": "LEAVE_TOOL, CALCULATOR_TOOL, FINAL"
    }
]
```

---

## Evaluation Logic

For each test case:

```text
Ask question
↓
Run answer_question()
↓
Compare actual route with expected route
↓
Print PASS or FAIL
```

---

## Metrics Added

Added route accuracy:

```python
route_accuracy = (passed / len(TEST_CASES)) * 100
```

Evaluation summary prints:

```text
Passed
Failed
Total
Route Accuracy
```

---

## Example Output

```text
Running Agent Evaluation...

Testing: Who is my manager?
Status: FAIL
Expected Route: MEMORY_READ, FINAL
Actual Route: FINAL

Testing: Do I have enough leave days to take a 15 day vacation?
Status: PASS

Evaluation Summary
Passed: 1
Failed: 3
Total: 4
Route Accuracy: 25.00%
```

---

## Important Finding

Failures were caused by Gemini quota exhaustion, not broken agent logic.

The logs showed:

```text
429 RESOURCE_EXHAUSTED
PLANNER RESPONSE: ERROR
```

Because `react_step()` falls back to:

```python
return "FINAL"
```

when Gemini fails, some routes became:

```text
FINAL
```

instead of the expected tool route.

---

## Outcome

Completed:

- Automated evaluation file ✅
- Route validation ✅
- PASS/FAIL reporting ✅
- Route accuracy metric ✅
- Failure diagnosis ✅
- Quota-related failure visibility ✅

---

## Key Learning

An evaluation framework helps separate:

```text
Agent logic failure
```

from:

```text
LLM/API availability failure
```

This is important in production AI systems because LLM calls can fail due to quota limits, rate limits, or temporary service unavailability.

---

## Next Planned Milestone

Milestone 24: Deployment & Production Readiness

Goal:

Prepare the project for GitHub, deployment, and interview demonstration.

---

# Milestone 24: Deployment & Production Readiness

Status: Completed

## Objective

Deploy the Agentic RAG Assistant to a public cloud environment and make it accessible through a live URL.

---

## Deployment Platform

Streamlit Community Cloud

---

## Live Application

```text
https://agentic-rag-assistant-aivkv4ekmlrhzrnn6jrjj8.streamlit.app
```

---

## Deployment Process

### Step 1: Prepare Repository

Verified:

- Git repository initialized
- Source code committed
- Documentation committed
- Screenshots committed
- Vector store committed
- Requirements file committed

Files verified:

```text
README.md
ARCHITECTURE.md
INTERVIEW_GUIDE.md
PROJECT_LOG.md
PROJECT_STRUCTURE.md
GIT_WORKFLOW.md

app.py
rag_service.py
rag_answer.py
memory_service.py
tools.py
evaluation.py
ingest.py
retrieve.py

data/
vector_store/
screenshots/
```

---

### Step 2: Configure Streamlit Cloud

Connected GitHub repository:

```text
agentic-rag-assistant
```

Selected:

```text
Branch: main
Main File: app.py
```

Configured application secrets:

```toml
GEMINI_API_KEY="YOUR_API_KEY"
```

---

### Step 3: Deploy Application

Deployment completed successfully.

Verified:

- Application startup
- Streamlit UI rendering
- FAISS index loading
- Gemini API connectivity

---

# Deployment Issues Encountered

## Issue 1: Missing memory.json

### Error

```text
FileNotFoundError:
No such file or directory: 'memory.json'
```

### Root Cause

Locally:

```text
memory.json existed
```

Cloud environment:

```text
Fresh container
↓
memory.json did not exist
↓
Application crashed
```

The application assumed the memory file already existed.

### Fix

Updated:

```python
memory_service.py
```

Before:

```python
def load_memory():

    with open(MEMORY_PATH, "r", encoding="utf-8") as file:
        return json.load(file)
```

After:

```python
def load_memory():

    if not os.path.exists(MEMORY_PATH):
        return {}

    with open(MEMORY_PATH, "r", encoding="utf-8") as file:
        return json.load(file)
```

Added:

```python
import os
```

### Result

Application now creates memory storage automatically when needed.

---

## Issue 2: Missing os Import

### Error

```text
NameError:
name 'os' is not defined
```

### Root Cause

Added:

```python
os.path.exists()
```

without importing:

```python
import os
```

### Fix

Added:

```python
import os
```

at the top of:

```python
memory_service.py
```

### Result

Memory service works correctly.

---

## Issue 3: Gemini Planner Failure During Deployment

### Observed Behavior

Memory requests returned:

```text
FINAL
```

instead of:

```text
MEMORY_WRITE
```

or

```text
MEMORY_READ
```

### Root Cause

Planner fallback logic:

```python
if response_text == "ERROR":
    return "FINAL"
```

caused the system to terminate when Gemini planning failed.

Possible causes:

- API failure
- Quota limit
- Temporary service issue

### Fix

Updated fallback behavior.

Before:

```python
if response_text == "ERROR":
    return "FINAL"
```

After:

```python
if response_text == "ERROR":
    return select_route(question)
```

### Result

System now uses deterministic routing when LLM planning fails.

This improves reliability and fault tolerance.

---

# Production Reliability Improvements

Added support for:

## Missing Files

System no longer crashes when:

```text
memory.json
```

is absent.

---

## LLM Failure Recovery

System now supports:

```text
Gemini Planner
↓
Failure
↓
Rule-Based Routing
↓
Continue Execution
```

instead of:

```text
Gemini Planner
↓
Failure
↓
Application Stops
```

---

## Cloud Environment Compatibility

Application now handles:

- Fresh deployments
- Container restarts
- Missing runtime files
- Temporary API failures
- LLM quota issues

---

# Lessons Learned

## Local Environment ≠ Production Environment

Code that works locally may fail after deployment because:

- Files may not exist
- Paths may differ
- APIs may behave differently
- Containers may restart

---

## Build Defensive Systems

Production systems should always assume:

- Files may be missing
- APIs may fail
- Quotas may be exceeded
- Services may be unavailable

---

## Fallback Logic Matters

Agent systems should have:

```text
Primary Path
↓
LLM Planning

Fallback Path
↓
Deterministic Routing
```

This ensures the application continues functioning even when AI services are unavailable.

---

# Deployment Outcome

Successfully deployed:

```text
Agentic RAG Assistant
```

Features verified:

```text
RAG                           ✅
FAISS Retrieval               ✅
Gemini Integration            ✅
Tool Calling                  ✅
Memory                        ✅
ReAct Workflow                ✅
Supervisor Agent              ✅
Specialist Agents             ✅
Evaluation Framework          ✅
Streamlit Deployment          ✅
```

---

# Milestone 24 Status

Completed ✅

The project has now completed the full software lifecycle:

```text
Idea
↓
Design
↓
Development
↓
Testing
↓
Documentation
↓
Version Control
↓
GitHub
↓
Deployment
↓
Production Readiness
```

This transformed the project from a local prototype into a publicly accessible AI application.