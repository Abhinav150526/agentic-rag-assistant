import streamlit as st
from src.core.rag_service import answer_question

st.set_page_config(
    page_title="Company Knowledge Assistant",
    page_icon="🤖"
)

st.title("Company Knowledge Assistant")
st.write("Ask questions about company documents, policies, and engineering notes.")
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

question = st.text_input(
    "Enter your question:"
)
if st.button("Ask Question"):
    if question:
        st.write("Thinking...")
        # result = answer_question(question)
        try:
            result = answer_question(question)
            print("RESULT =", result)
        except Exception as error:
            st.error("Something went wrong while generating the answer. Please try again.")
            st.write(error)
            result = None
        # st.session_state.chat_history.append({
        #     "question": question,
        #     "answer": result["answer"],
        #     "sources": result["sources"]
        # })
    if result:
        st.session_state.chat_history.append({
            "question": question,
            "answer": result["answer"],
            "sources": result["sources"]
        }) 
        
        st.subheader("Agent Route")
        st.write(result["route"])

        st.subheader("Agent Scratchpad")
        st.write("Thoughts:")
        for thought in result["thoughts"]:
            st.write(f"- {thought}")

        st.write("Observations:")
        for observation in result["observations"]:
            st.write(f"- {observation}")

        st.subheader("Answer")
        st.write(result["answer"])

        st.subheader("Sources")

        # for source in result["sources"]:
        #     st.write(source["source"])
        #--------------------------------------------
        # for source in result["sources"]:
        #     if isinstance(source, dict):
        #         st.write(source["source"])
        #     else:
        #         st.write(source)
        # Problem
        # Current sources show:
               # faiss.txt
               # faiss.txt
               # faiss.txt
            # because multiple retrieved chunks came from the same file.
        # We want:
             # faiss.txt
             # only once.
        #--------------------------------------------
        # below is Source Deduplication.
        unique_sources = set()

        for source in result["sources"]:
            if isinstance(source, dict):
                unique_sources.add(source["source"])
            else:
                unique_sources.add(source)

        for source in unique_sources:
            st.write(source)

st.subheader("Chat History")

for chat in st.session_state.chat_history:
    st.write(f"**You:** {chat['question']}")
    st.write(f"**Assistant:** {chat['answer']}")
    st.write("---")