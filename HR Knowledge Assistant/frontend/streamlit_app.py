import streamlit as st
import requests


# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="HR Knowledge Assistant",
    page_icon="🤖",
    layout="centered"
)


# --------------------------------------------------
# Header
# --------------------------------------------------

st.title("🤖 HR Knowledge Assistant")

st.caption(
    "Ask questions about HR policies and get answers "
    "from the organization's documents."
)


# --------------------------------------------------
# Initialize Chat History
# --------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []


# --------------------------------------------------
# Display Previous Messages
# --------------------------------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

        # Display sources for assistant messages
        if (
            message["role"] == "assistant"
            and "sources" in message
        ):

            st.markdown("**📚 Sources**")

            unique_sources = set()

            for source in message["sources"]:

                source_key = (
                    source["source"],
                    source["page"]
                )

                if source_key not in unique_sources:

                    unique_sources.add(source_key)

                    with st.container(border=True):

                        st.markdown(
                            f"📄 **{source['source']}**"
                        )

                        st.caption(
                            f"Page {source['page']}"
                        )


# --------------------------------------------------
# Chat Input
# --------------------------------------------------

question = st.chat_input(
    "Ask an HR question..."
)


# --------------------------------------------------
# Process Question
# --------------------------------------------------

if question:

    # --------------------------------------------------
    # Display User Question
    # --------------------------------------------------

    with st.chat_message("user"):

        st.markdown(question)


    # --------------------------------------------------
    # Save User Message
    # --------------------------------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )


    # --------------------------------------------------
    # Call FastAPI
    # --------------------------------------------------

    try:

        with st.chat_message("assistant"):

            with st.spinner("Searching HR policies..."):

                response = requests.post(
                    "http://127.0.0.1:8000/ask",
                    json={
                        "question": question,

                        # Send previous conversation,
                        # excluding the current question
                        "chat_history": (
                            st.session_state.messages[:-1]
                        )
                    },
                    timeout=300
                )


            # --------------------------------------------------
            # Successful Response
            # --------------------------------------------------

            if response.status_code == 200:

                result = response.json()

                answer = result["answer"]

                sources = result.get("sources", [])


                # --------------------------------------------------
                # Display Answer
                # --------------------------------------------------

                st.markdown(answer)


                # --------------------------------------------------
                # Display Sources
                # --------------------------------------------------

                if sources:

                    st.markdown("**📚 Sources**")

                    unique_sources = set()

                    for source in sources:

                        source_key = (
                            source["source"],
                            source["page"]
                        )

                        if source_key not in unique_sources:

                            unique_sources.add(source_key)

                            with st.container(border=True):

                                st.markdown(
                                    f"📄 **{source['source']}**"
                                )

                                st.caption(
                                    f"Page {source['page']}"
                                )


                # --------------------------------------------------
                # Save Assistant Response
                # --------------------------------------------------

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": answer,
                        "sources": sources
                    }
                )


            # --------------------------------------------------
            # API Error
            # --------------------------------------------------

            else:

                st.error(
                    f"API Error: {response.status_code}\n\n"
                    f"{response.text}"
                )


    # --------------------------------------------------
    # FastAPI Connection Error
    # --------------------------------------------------

    except requests.exceptions.ConnectionError as e:

        st.error(
            "Could not connect to the FastAPI server.\n\n"
            f"Details: {e}"
        )


    # --------------------------------------------------
    # Timeout
    # --------------------------------------------------

    except requests.exceptions.Timeout:

        st.error(
            "The request took too long. "
            "Please try again."
        )


    # --------------------------------------------------
    # Other Errors
    # --------------------------------------------------

    except Exception as e:

        st.error(
            f"Something went wrong: {e}"
        )