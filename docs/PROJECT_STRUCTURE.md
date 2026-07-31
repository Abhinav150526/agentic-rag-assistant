# Project Structure

## app.py
Streamlit UI layer.

Responsibilities:
- Accept user question
- Call answer_question()
- Display agent route
- Display scratchpad
- Display final answer
- Display sources
- Display chat history

## rag_service.py
Main agent orchestration layer.

Responsibilities:
- Create initial state
- Run supervisor agent
- Dispatch to specialist agents
- Execute ReAct-style loop
- Return final response

Main components:
- call_gemini()
- react_step()
- create_initial_state()
- supervisor_agent()
- hr_agent()
- memory_agent()
- utility_agent()
- rag_agent()
- execute_action_node()
- answer_node()
- answer_question()

## memory_service.py
Persistent memory layer.

Responsibilities:
- Load memory
- Save memory
- Store facts
- Recall facts

## memory.json
Local memory database.

## tools.py
Tool layer.

Responsibilities:
- Leave calculation
- Date tool
- Calculator tool

## evaluation.py
Agent evaluation framework.

Responsibilities:
- Run fixed test cases
- Check expected route
- Print pass/fail
- Calculate route accuracy

## data/
Source data used for RAG.

## vector_store/
Stored FAISS index and chunks.

## .env
Environment variables such as GEMINI_API_KEY.

## PROJECT_LOG.md
Milestone-by-milestone development history.