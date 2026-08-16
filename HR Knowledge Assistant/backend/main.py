from fastapi import FastAPI
from pydantic import BaseModel, Field

from services.agent_service import AgentService


app = FastAPI(
    title="HR Knowledge Assistant API",
    description="API for the HR Knowledge Assistant",
    version="1.0.0"
)


# --------------------------------------------------
# Create Agent service
# --------------------------------------------------

agent_service = AgentService()


# --------------------------------------------------
# Request model
# --------------------------------------------------

class QuestionRequest(BaseModel):

    question: str = Field(..., min_length=1)

    chat_history: list[dict] = Field(
        default_factory=list
    )


# --------------------------------------------------
# Response models
# --------------------------------------------------

class Source(BaseModel):

    source: str
    page: int
    score: float


class AnswerResponse(BaseModel):

    answer: str
    sources: list[Source]


# --------------------------------------------------
# Root endpoint
# --------------------------------------------------

@app.get("/")
def root():

    return {
        "message": "HR Knowledge Assistant API is running"
    }


# --------------------------------------------------
# Health check
# --------------------------------------------------

@app.get("/health")
def health_check():

    return {
        "status": "healthy"
    }


# --------------------------------------------------
# Ask question
# --------------------------------------------------

@app.post(
    "/ask",
    response_model=AnswerResponse
)
def ask_question(request: QuestionRequest):

    response = agent_service.ask(
        request.question
    )

    return response