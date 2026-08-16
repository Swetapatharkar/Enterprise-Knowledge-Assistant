class QueryRewriterService:

    def rewrite(self, question, chat_history):

        current_question = question.strip()

        # No conversation history
        if not chat_history:
            return current_question

        # Get previous user questions
        previous_user_questions = []

        for message in chat_history:

            if message.get("role") == "user":

                content = message.get("content", "").strip()

                if content:
                    previous_user_questions.append(content)

        # No previous user question
        if not previous_user_questions:
            return current_question

        previous_question = previous_user_questions[-1]

        # --------------------------------------------------
        # Detect common follow-up patterns
        # --------------------------------------------------

        follow_up_patterns = [
            "what about",
            "how about",
            "what if",
            "and what about",
            "and how about",
            "for someone",
            "for an employee",
            "what happens"
        ]

        is_follow_up = any(
            current_question.lower().startswith(pattern)
            for pattern in follow_up_patterns
        )

        # Not a follow-up
        if not is_follow_up:
            return current_question

        # --------------------------------------------------
        # Build contextual retrieval query
        # --------------------------------------------------

        return (
            f"{previous_question} "
            f"Specific case: {current_question}"
        )