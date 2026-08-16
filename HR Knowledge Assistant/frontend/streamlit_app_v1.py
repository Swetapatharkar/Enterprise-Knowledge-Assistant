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

st.write(
    "Ask questions about HR policies and get answers "
    "from the organization's documents."
)


# --------------------------------------------------
# Question Input
# --------------------------------------------------

question = st.text_input(
    "Ask your question:",
    placeholder=(
        "e.g. How many weeks of maternity leave "
        "are employees entitled to?"
    )
)


# --------------------------------------------------
# Ask Button
# --------------------------------------------------

if st.button("Ask"):

    if not question.strip():

        st.warning("Please enter a question.")

    else:

        try:

            with st.spinner("Searching HR policies..."):

                response = requests.post(
                    "http://127.0.0.1:8000/ask",
                    json={
                        "question": question
                    },
                    timeout=120
                )


            # --------------------------------------------------
            # Successful Response
            # --------------------------------------------------

            if response.status_code == 200:

                result = response.json()


                # ------------------------------
                # Answer
                # ------------------------------

                st.subheader("💡 Answer")

                st.write(result["answer"])


                # ------------------------------
                # Sources
                # ------------------------------

                st.subheader("📚 Sources")

                unique_sources = set()

                for source in result["sources"]:

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
            # API Error
            # --------------------------------------------------

            else:

                st.error(
                    f"API Error: {response.status_code}"
                )


        # --------------------------------------------------
        # FastAPI Connection Error
        # --------------------------------------------------

        except requests.exceptions.ConnectionError:

            st.error(
                "Could not connect to the FastAPI server. "
                "Please make sure FastAPI is running."
            )


        # --------------------------------------------------
        # Request Timeout
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