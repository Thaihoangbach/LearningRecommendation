from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from intent_classifier import classify_intent
from context_builder import (
    build_context,
    context_to_prompt_string
)
from llm_service import generate_response

from kg.graph_loader import load_graph
from kg.graph_query import get_all_courses

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


sessions = {}

class ChatMessage(BaseModel):
    session_id: str
    text: str
    course_id: str


class MentorRequest(BaseModel):
    session_id: str
    student_name: str


@app.post("/chat")
def chat(msg: ChatMessage):

    session = sessions.setdefault(
        msg.session_id,
        {
            "history": [],
            "reprompt": 0
        }
    )

    intent = classify_intent(msg.text)

    if intent == "other":

        session["reprompt"] += 1

        if session["reprompt"] >= 3:

            session["reprompt"] = 0

            return {
                "reply": (
                    "Tôi chưa thể hỗ trợ câu hỏi này. "
                    "Bạn có muốn kết nối với mentor không?"
                ),
                "intent": intent,
                "suggest_mentor": True
            }

        return {
            "reply": (
                f"Tôi chưa hiểu rõ câu hỏi của bạn "
                f"(lần {session['reprompt']}/3). "
                "Hãy hỏi về nội dung khóa học, "
                "lý do gợi ý, lợi ích hoặc mối liên hệ "
                "giữa các khóa học."
            ),
            "intent": intent,
            "suggest_mentor": False
        }

    session["reprompt"] = 0


    context = build_context(
        intent,
        msg.course_id
    )

    context_str = context_to_prompt_string(
        context
    )

    reply = generate_response(
        msg.text,
        context_str,
        session["history"]
    )

    session["history"].append({
        "role": "user",
        "content": msg.text
    })

    session["history"].append({
        "role": "assistant",
        "content": reply
    })

    return {
        "reply": reply,
        "intent": intent,
        "suggest_mentor": False
    }


@app.get("/courses")
def get_courses():

    courses = get_all_courses()

    path = [
        course["id"]
        for course in courses
    ]

    return {
        "path": path,
        "courses": courses
    }

@app.get("/kg/stats")
def kg_stats():

    G = load_graph()

    return {
        "nodes": G.number_of_nodes(),
        "edges": G.number_of_edges()
    }


@app.post("/mentor/request")
def request_mentor(req: MentorRequest):

    return {
        "status": "pending",
        "message": (
            "Yêu cầu kết nối mentor đã được ghi nhận."
        )
    }


@app.get("/")
def root():

    return {
        "message": "Learning Recommendation API",
        "status": "running"
    }
