import os
import json
import faiss
import numpy as np
import re
import time

from src.utils.tools import (
    calculate_remaining_leave_days,
    get_remaining_leave_days,
    get_current_date,
    calculate
)
from src.core.memory_service import (
    remember_fact,
    recall_fact
)
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from google import genai

load_dotenv()

VECTOR_STORE_PATH = "vector_store/faiss.index"
CHUNKS_PATH = "vector_store/chunks.json"

def load_chunks():
    with open(CHUNKS_PATH, "r", encoding="utf-8") as file:
        return json.load(file)

def retrieve_chunks(question, k=3):
    chunks = load_chunks()

    index = faiss.read_index(VECTOR_STORE_PATH)

    model = SentenceTransformer("all-MiniLM-L6-v2")

    question_embedding = model.encode([question])
    question_embedding = np.array(question_embedding).astype("float32")

    distances, indices = index.search(question_embedding, k)
    print("\nRAG DEBUG")
    print("Distances:", distances)
    print("Indices:", indices)
    print("END DEBUG\n")

    # retrieved_chunks = []

    # for idx in indices[0]:
    #     retrieved_chunks.append(chunks[idx])

    # return retrieved_chunks

    retrieved_chunks = []

    threshold = 1.0

    for distance, idx in zip(distances[0], indices[0]):
        if distance <= threshold:
            retrieved_chunks.append(chunks[idx])

    return retrieved_chunks

def call_gemini(prompt, retries=2):
    for attempt in range(retries + 1):
        try:
            client = genai.Client(
                api_key=os.getenv("GEMINI_API_KEY")
            )

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )

            return response.text

        except Exception as e:
            print(f"GEMINI ERROR on attempt {attempt + 1}: {e}")

            if attempt < retries:
                time.sleep(2)
            else:
                return "ERROR"

def generate_answer(question, retrieved_chunks, call_gemini):
    context = "\n\n".join(
        [chunk["text"] for chunk in retrieved_chunks]
    )

    prompt = f"""
Answer the question using only the provided context.
Explain it in simple beginner-friendly words.

Context:
{context}

Question:
{question}
"""

    return call_gemini(prompt) 

def should_use_leave_tool(question):

    prompt = f"""
    Decide if this question is asking about an employee's remaining leave balance.

    Question:
    {question}

    Answer only YES or NO.
    """

    # response = model.generate_content(prompt)
    client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
    )

    response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt
    )

    return response.text.strip().upper() == "YES"

def select_route(question):

    prompt = f"""
    You are a routing assistant for a company AI assistant.

    Decide the best route for the user's question.

    Available routes:
    LEAVE_TOOL - use when the question asks about remaining leave balance or leave days left.
    DATE_TOOL - use when the question asks about today's date or current date.
    RAG - use for questions about company documents, policies, FAISS, embeddings, or general knowledge base content.

    Question:
    {question}

    Answer only one of these:
    LEAVE_TOOL
    DATE_TOOL
    RAG
    """

    client = genai.Client(
        api_key=os.getenv("GEMINI_API_KEY")
    )

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text.strip().upper()
#-----------------------------------------------------------------------
# def answer_question(question):
#     # if "leave days" in question.lower():
#     if should_use_leave_tool(question):
#         return {
#            "answer": calculate_remaining_leave_days("abhi"),
#            "sources": ["HR Leave Tool"]
#         }
#     retrieved_chunks = retrieve_chunks(question)

#     answer = generate_answer(question, retrieved_chunks)

#     return {
#         "answer": answer,
#         "sources": retrieved_chunks
#     }  
#-----------------------------------------------------------------------------------

def select_actions(question):

    prompt = f"""
    You are an agent planner for a company AI assistant.

    Decide which actions are needed to answer the user's question.

    Available actions:
    LEAVE_TOOL - use when the question asks about remaining leave balance or leave days left.
    DATE_TOOL - use when the question asks about today's date or current date.
    RAG - use for questions about company documents, policies, FAISS, embeddings, or knowledge base content.
    CALCULATOR_TOOL - use when the question needs arithmetic, comparison, or calculation.

    Question:
    {question}

    Return only the needed action names separated by commas.

    Examples:
    Question: How many leave days do I have?
    Answer: LEAVE_TOOL

    Question: What is today's date?
    Answer: DATE_TOOL

    Question: What is FAISS?
    Answer: RAG

    Question: How many leave days do I have and what is today's date?
    Answer: LEAVE_TOOL, DATE_TOOL
    """

    client = genai.Client(
        api_key=os.getenv("GEMINI_API_KEY")
    )

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    actions = response.text.strip().upper().split(",")
    print("PLANNER RESPONSE:", response.text)
    return [action.strip() for action in actions]

def extract_requested_days(question):
    numbers = re.findall(r"\d+", question)

    if numbers:
        return int(numbers[0])

    return None

# def extract_employee_name(question):

#     known_employees = ["abhi", "john", "sarah"]

#     question_lower = question.lower()

#     for employee in known_employees:
#         if employee in question_lower:
#             return employee

#     return "abhi"

def extract_employee_name(question):

    prompt = f"""
    Extract the employee name from the user's question.

    If the user says "I", "me", or "my", return Abhi.

    If no employee name is mentioned, return Abhi.

    Question:
    {question}

    Return only the employee name.
    """

    response_text = call_gemini(prompt)

    if response_text == "ERROR":
        return "abhi"

    return response_text.strip().lower()

def react_step(question, observations):

    question_lower = question.lower()
    observations_text = " ".join(observations).lower()

    if "enough leave" in question_lower or "vacation" in question_lower:
        if "leave days remaining" not in observations_text:
            return "LEAVE_TOOL"

        if "calculation result" not in observations_text:
            return "CALCULATOR_TOOL"

        return "FINAL"
        
    prompt = f"""
    You are a ReAct-style agent.

    Decide the next best action based on the user's question and previous observations.

    Available actions:
    LEAVE_TOOL - get employee remaining leave balance.
    CALCULATOR_TOOL - compare remaining leave days with requested vacation days.
    DATE_TOOL - get today's date.
    RAG - answer using company documents.
    FINAL - use only when previous observations already contain enough information to answer.
    If the previous observations contain "Employee not found", return FINAL.
    If the previous observations contain "Stored manager", return FINAL.
    If the previous observations contain "Recalled manager", return FINAL.
    MEMORY_WRITE - store a user-provided fact in memory.
    MEMORY_READ - retrieve a previously stored fact from memory.
    If the question asks about company policy, employee handbook, paid leave policy, FAISS, embeddings, or document-based knowledge, return RAG unless the answer is already present in previous observations.
    If the previous observations contain a RAG/document answer, return FINAL.
    If the question requires comparing leave days with requested vacation days:
     - First use LEAVE_TOOL to get the balance.
     - Then use CALCULATOR_TOOL to perform the comparison.
     - Only after the comparison return FINAL.

    Example:
    User question:
    My manager is Raj.

    Previous observations:
    []

    Answer:
    MEMORY_WRITE

    Example:
    User question:
    Who is my manager?

    Previous observations:
    []

    Answer:
    MEMORY_READ

    User question:
    {question}

    Previous observations:
    {observations}

    Answer only one action name:
    LEAVE_TOOL
    CALCULATOR_TOOL
    DATE_TOOL
    RAG
    MEMORY_WRITE
    MEMORY_READ
    FINAL
    """

    response_text = call_gemini(prompt)

    print("PLANNER RESPONSE:", response_text)

    if response_text == "ERROR":
        return "FINAL"

    return response_text.strip().upper()

def create_initial_state(question):
    return {
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

def planner_node(state):
    action = react_step(
        state["question"],
        state["observations"]
    )

    state["next_action"] = action

    return state

def hr_agent(state):
    if state["employee_name"] is None:
        state["employee_name"] = extract_employee_name(
            state["question"]
        )

    state["thoughts"].append(
        "HR Agent: I need to check the employee's remaining leave balance."
    )

    leave_result = calculate_remaining_leave_days(
        state["employee_name"]
    )

    state["remaining_leave"] = get_remaining_leave_days(
        state["employee_name"]
    )

    state["observations"].append(leave_result)
    state["results"].append(leave_result)
    state["sources"].append("HR Leave Tool")

    return state

def memory_agent(state):
    action = state["next_action"]

    if action == "MEMORY_READ":
        state["thoughts"].append(
            "Memory Agent: I should retrieve the stored fact from memory."
        )

        manager_name = recall_fact("manager")

        observation = f"Recalled manager = {manager_name}"

        state["observations"].append(observation)
        state["results"].append(f"Your manager is {manager_name}.")
        state["sources"].append("Memory")

    elif action == "MEMORY_WRITE":
        state["thoughts"].append(
            "Memory Agent: I should store the user's fact in memory."
        )

        manager_name = state["question"].split("is")[-1].strip().replace(".", "")

        remember_fact("manager", manager_name)

        observation = f"Stored manager = {manager_name}"

        state["observations"].append(observation)
        state["results"].append(
            f"Okay, I will remember that your manager is {manager_name}."
        )
        state["sources"].append("Memory")

    return state

def utility_agent(state):
    action = state["next_action"]

    if action == "DATE_TOOL":
        state["thoughts"].append(
            "Utility Agent: I need to check the current date."
        )

        date_result = get_current_date()

        state["observations"].append(date_result)
        state["results"].append(date_result)
        state["sources"].append("Date Tool")

    elif action == "CALCULATOR_TOOL":
        state["thoughts"].append(
            "Utility Agent: I need to compare the remaining leave days with the requested vacation days."
        )

        if state["remaining_leave"] is not None and state["requested_days"] is not None:
            calculation_result = calculate(
                f"{state['remaining_leave']} >= {state['requested_days']}"
            )
        else:
            calculation_result = "Required values were not available for calculation."

        state["observations"].append(calculation_result)
        state["results"].append(calculation_result)
        state["sources"].append("Calculator Tool")

    return state

def rag_agent(state):
    retrieved_chunks = retrieve_chunks(state["question"])

    rag_answer = generate_answer(
        state["question"],
        retrieved_chunks,
        call_gemini
    )

    if rag_answer == "ERROR":
        rag_answer = (
            "The relevant document was found, but Gemini could not generate "
            "the final answer right now due to API limits. Please try again shortly."
        )

    state["results"].append(rag_answer)
    state["observations"].append("RAG answer generated.")
    state["sources"].extend(retrieved_chunks)

    return state

def execute_action_node(state):
    action = state["next_action"]

    if action == "MEMORY_READ":
        state = memory_agent(state)

    elif action == "MEMORY_WRITE":
        state = memory_agent(state)

    elif action == "LEAVE_TOOL":
        state = hr_agent(state)

    elif action == "DATE_TOOL":
        state = utility_agent(state)

    elif action == "CALCULATOR_TOOL":
        state = utility_agent(state)
        
    elif action == "RAG":
        state = rag_agent(state)

    return state

def answer_node(state):
    if state["remaining_leave"] is not None and state["requested_days"] is not None:
        if state["remaining_leave"] >= state["requested_days"]:
            final_answer = (
                f"{state['employee_name'].title()} has {state['remaining_leave']} leave days remaining.\n\n"
                f"Since your requested vacation is {state['requested_days']} days, "
                f"you have enough leave available."
            )
        else:
            final_answer = (
                f"{state['employee_name'].title()} has {state['remaining_leave']} leave days remaining.\n\n"
                f"Since your requested vacation is {state['requested_days']} days, "
                f"you do not have enough leave available."
            )
    else:
        final_answer = "\n\n".join(state["results"])

    state["final_answer"] = final_answer

    return state

def answer_question(question):
    question_lower = question.lower()

    # if "my manager is" in question_lower:
    #     manager_name = question.split("is")[-1].strip().replace(".", "")

    #     remember_fact("manager", manager_name)

    #     return {
    #         "answer": f"Okay, I will remember that your manager is {manager_name}.",
    #         "sources": ["Memory"],
    #         "route": "MEMORY_WRITE",
    #         "thoughts": ["The user shared a personal fact that should be stored."],
    #         "observations": [f"Stored manager = {manager_name}"]
    #     }

    # if "who is my manager" in question_lower:
    #     manager_name = recall_fact("manager")

    #     return {
    #        "answer": f"Your manager is {manager_name}.",
    #        "sources": ["Memory"],
    #        "route": "MEMORY_READ",
    #        "thoughts": ["The user asked for a previously stored fact."],
    #        "observations": [f"Recalled manager = {manager_name}"]
    #     }

    #actions = select_actions(question)
    # actions = []

    # results = []
    # sources = []

    # thoughts = []
    # observations = []

    # remaining_leave = None
    # requested_days = extract_requested_days(question)
    # employee_name = extract_employee_name(question)

    # state = {
    # "question": question,
    # "results": [],
    # "sources": [],
    # "actions": [],
    # "thoughts": [],
    # "observations": [],
    # "remaining_leave": None,
    # "requested_days": extract_requested_days(question),
    # "employee_name": None
    # }

    state = create_initial_state(question)

    #for action in actions:
    for step in range(3):
        # action = react_step(question, observations)
        # actions.append(action)
#------------------------------------------------------
        # action = react_step(
        #     state["question"],
        #     state["observations"]
        # )

        # state["actions"].append(action)

        # if action == "FINAL":
        #     break
#---------------------------------------------------
        # action = react_step(
        #     state["question"],
        #     state["observations"]
        # )

        # state = planner_node(state)
        state = supervisor_agent(state)
        action = state["next_action"]

        if action in state["actions"] and action != "FINAL":
            state["observations"].append(
                f"Duplicate action detected: {action}. Stopping agent."
            )
            state["actions"].append("FINAL")
            break

        state["actions"].append(action)

        if action == "FINAL":
            break

        state = execute_action_node(state)
#----------------------------------------------------------------------
        # if action == "LEAVE_TOOL":
        #     leave_result = calculate_remaining_leave_days("abhi")
        #     remaining_leave = get_remaining_leave_days("abhi")
        #     results.append(leave_result)
        #     sources.append("HR Leave Tool")
#------------------------------------------------------------
        # if action == "MEMORY_WRITE":

        #    state["thoughts"].append("I should store the user's fact in memory.")

        #    manager_name = question.split("is")[-1].strip().replace(".", "")

        #    remember_fact("manager", manager_name)

        #    observation = f"Stored manager = {manager_name}"

        #    state["observations"].append(observation)
        #    state["results"].append(f"Okay, I will remember that your manager is {manager_name}.")
        #    state["sources"].append("Memory")

        # elif action == "MEMORY_READ":

        #     state["thoughts"].append("I should retrieve the stored fact from memory.")

        #     manager_name = recall_fact("manager")

        #     observation = f"Recalled manager = {manager_name}"

        #     state["observations"].append(observation)
        #     state["results"].append(f"Your manager is {manager_name}.")
        #     state["sources"].append("Memory")   
        
        # if action == "LEAVE_TOOL":
        #     thoughts.append("I need to check the employee's remaining leave balance.")

        #     leave_result = calculate_remaining_leave_days(employee_name)
        #     remaining_leave = get_remaining_leave_days(employee_name)

        #     observations.append(leave_result)

        #     results.append(leave_result)
        #     sources.append("HR Leave Tool")

        # if action == "LEAVE_TOOL":

        #     if state["employee_name"] is None:
        #         state["employee_name"] = extract_employee_name(
        #             state["question"]
        #         )
        #     state["thoughts"].append("I need to check the employee's remaining leave balance.")

        #     leave_result = calculate_remaining_leave_days(state["employee_name"])
        #     state["remaining_leave"] = get_remaining_leave_days(state["employee_name"])

        #     state["observations"].append(leave_result)

        #     state["results"].append(leave_result)
        #     state["sources"].append("HR Leave Tool")

        # elif action == "DATE_TOOL":
        #     thoughts.append("I need to check the current date.")

        #     date_result = get_current_date()

        #     observations.append(date_result)

        #     results.append(date_result)
        #     sources.append("Date Tool")
        # elif action == "DATE_TOOL":
        #     state["thoughts"].append("I need to check the current date.")

        #     date_result = get_current_date()

        #     state["observations"].append(date_result)

        #     state["results"].append(date_result)
        #     state["sources"].append("Date Tool")

        # elif action == "CALCULATOR_TOOL":
        #     thoughts.append("I need to compare the remaining leave days with the requested vacation days.")

        #     if remaining_leave is not None and requested_days is not None:
        #         calculation_result = calculate(f"{remaining_leave} >= {requested_days}")
        #     else:
        #         calculation_result = "Required values were not available for calculation."

        #     observations.append(calculation_result)

        #     results.append(calculation_result)
        #     sources.append("Calculator Tool")

        # elif action == "CALCULATOR_TOOL":
        #     state["thoughts"].append("I need to compare the remaining leave days with the requested vacation days.")

        #     if state["remaining_leave"] is not None and state["requested_days"] is not None:
        #         calculation_result = calculate(
        #             f"{state['remaining_leave']} >= {state['requested_days']}"
        #         )
        #     else:
        #         calculation_result = "Required values were not available for calculation."

        #     state["observations"].append(calculation_result)

        #     state["results"].append(calculation_result)
        #     state["sources"].append("Calculator Tool")

        # elif action == "RAG":
        #     retrieved_chunks = retrieve_chunks(state["question"])
        #     rag_answer = generate_answer(state["question"], retrieved_chunks)

        #     state["results"].append(rag_answer)
        #     state["sources"].extend(retrieved_chunks)

    # if state["remaining_leave"] is not None and state["requested_days"] is not None:
    #     if state["remaining_leave"] >= state["requested_days"]:
    #         final_answer = (
    #             f"{state['employee_name'].title()} has {state['remaining_leave']} leave days remaining.\n\n"
    #             f"Since your requested vacation is {state['requested_days']} days, "
    #             f"you have enough leave available."
    #         )
    #     else:
    #        final_answer = (
    #            f"{state['employee_name'].title()} has {state['remaining_leave']} leave days remaining.\n\n"
    #            f"Since your requested vacation is {state['requested_days']} days, "
    #            f"you do not have enough leave available."
    #         )
    # else:
    #     final_answer = "\n\n".join(state["results"])

    state = answer_node(state)

    return {
       #"answer": final_answer,
       "answer": state["final_answer"],
       "sources": state["sources"],
       "route": ", ".join(state["actions"]),
       "thoughts": state["thoughts"],
       "observations": state["observations"]
    }

# print(
#     react_step(
#         "Do I have enough leave days to take a 15 day vacation?",
#         []
#     )
# )

# if __name__ == "__main__":
#     result = answer_question(
#         "How many paid leave days do employees get?"
#     )

#     print(result["answer"])

#     print("\nSources:\n")

#     for source in result["sources"]:
#         print(source["source"])