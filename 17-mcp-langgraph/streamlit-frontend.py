import streamlit as st
import queue
import uuid

from langchain_core.messages import (
    HumanMessage,
    AIMessage,
    ToolMessage,
)

from langgraph_backend import (
    retrieve_all_threads,
    load_conversation,
    submit_async,
    stream_chat,
)


def generate_thread_id():
    return str(uuid.uuid4())


def add_thread(thread_id):
    if thread_id not in st.session_state["chat_threads"]:
        st.session_state["chat_threads"].append(thread_id)


def reset_chat():
    thread_id = generate_thread_id()

    st.session_state["thread_id"] = thread_id
    st.session_state["message_history"] = []

    add_thread(thread_id)


def stream_response(user_input, config, status):
    output_queue = queue.Queue()

    submit_async(
        stream_chat(
            user_input,
            config,
            output_queue,
        )
    )

    while True:
        item, metadata = output_queue.get()

        if item == "__DONE__":
            break

        if item == "__ERROR__":
            raise metadata

        if isinstance(item, ToolMessage):
            tool_name = getattr(item, "name", "tool")

            if status["box"] is None:
                status["box"] = st.status(
                    f"Using `{tool_name}`...",
                    expanded=True,
                )
            else:
                status["box"].update(
                    label=f"Using `{tool_name}`...",
                    state="running",
                    expanded=True,
                )

        if isinstance(item, AIMessage):
            if isinstance(item.content, str):
                yield item.content


if "message_history" not in st.session_state:
    st.session_state["message_history"] = []

if "thread_id" not in st.session_state:
    st.session_state["thread_id"] = generate_thread_id()

if "chat_threads" not in st.session_state:
    st.session_state["chat_threads"] = retrieve_all_threads()

add_thread(st.session_state["thread_id"])


st.sidebar.title("LangGraph Chatbot")

if st.sidebar.button("New Chat"):
    reset_chat()
    st.rerun()


st.sidebar.header("My Conversations")

for thread_id in st.session_state["chat_threads"][::-1]:

    if st.sidebar.button(str(thread_id)):
        st.session_state["thread_id"] = thread_id

        messages = load_conversation(thread_id)
        history = []

        for message in messages:
            if isinstance(message, HumanMessage):
                role = "user"
            elif isinstance(message, AIMessage):
                role = "assistant"
            else:
                continue

            history.append(
                {
                    "role": role,
                    "content": message.content,
                }
            )

        st.session_state["message_history"] = history
        st.rerun()


for message in st.session_state["message_history"]:
    with st.chat_message(message["role"]):
        st.write(message["content"])


user_input = st.chat_input("Type here")


if user_input:

    st.session_state["message_history"].append(
        {
            "role": "user",
            "content": user_input,
        }
    )

    with st.chat_message("user"):
        st.write(user_input)

    thread_id = st.session_state["thread_id"]

    config = {
        "configurable": {
            "thread_id": thread_id
        },
        "metadata": {
            "thread_id": thread_id
        },
        "run_name": "chat_turn",
    }

    with st.chat_message("assistant"):

        status = {"box": None}

        try:
            response = st.write_stream(
                stream_response(
                    user_input,
                    config,
                    status,
                )
            )

            if status["box"] is not None:
                status["box"].update(
                    label="Tool finished",
                    state="complete",
                    expanded=False,
                )

        except Exception as e:
            st.error(f"Error: {e}")
            response = ""

    if response:
        st.session_state["message_history"].append(
            {
                "role": "assistant",
                "content": response,
            }
        )