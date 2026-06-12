from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from intent_classifier import classify_intent
from context_builder import build_context, context_to_prompt_string
from llm_service import generate_response

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

sessions: dict = {}
group_sessions = {}
mentor_queue: list = []

class ChatMessage(BaseModel):
    session_id: str
    text: str
    course_id: str = "data_analysis"

class MentorRequest(BaseModel):
    session_id: str
    student_name: str

class MentorReply(BaseModel):
    session_id: str
    mentor_name: str
    text: str
class MentorAccept(BaseModel):
    session_id: str
    mentor_name: str
class GroupMessage(BaseModel):
    group_id: str
    sender: str
    text: str

@app.post("/chat")
def chat(msg: ChatMessage):
    session = sessions.setdefault(msg.session_id, {"history": [], "reprompt": 0})
    intent  = classify_intent(msg.text)

    if intent == "other":
        session["reprompt"] += 1
        if session["reprompt"] >= 3:
            session["reprompt"] = 0
            return {
                "reply": "Tôi không thể hỗ trợ câu hỏi này. Bạn có muốn kết nối với mentor không?",
                "intent": intent,
                "suggest_mentor": True
            }
        return {
            "reply": (
                f"Tôi chưa hiểu rõ câu hỏi của bạn (lần {session['reprompt']}/3). "
                "Bạn có thể diễn đạt lại không? "
                "Tôi hỗ trợ các câu hỏi về lý do gợi ý, nội dung, lợi ích và mối liên hệ của khóa học."
            ),
            "intent": intent,
            "suggest_mentor": False
        }

    session["reprompt"] = 0

    context     = build_context(intent, msg.course_id)
    context_str = context_to_prompt_string(context)

    reply = generate_response(msg.text, context_str, session["history"])

    session["history"].append({"role": "user",      "content": msg.text})
    session["history"].append({"role": "assistant",  "content": reply})

    return {
        "reply": reply,
        "intent": intent,
        "suggest_mentor": False,
    }

@app.post("/mentor/request")
def request_mentor(req: MentorRequest):
    mentor_queue.append(req.dict())
    return {"status": "pending", "message": "Đã gửi yêu cầu. Mentor sẽ tham gia sớm!"}

@app.get("/mentor/queue")
def get_queue():
    return mentor_queue

@app.post("/mentor/reply")
def mentor_reply(rep: MentorReply):
    session = sessions.setdefault(rep.session_id, {"history": [], "reprompt": 0})
    session["history"].append({"role": "assistant", "content": f"[Mentor {rep.mentor_name}]: {rep.text}"})
    return {"status": "ok"}

@app.get("/courses")
def list_courses():
    from knowledge_graph import get_learning_path, get_course
    path = get_learning_path()
    return {"path": path, "courses": [get_course(c) for c in path]}
@app.post("/mentor/accept")
def mentor_accept(req: MentorAccept):

    group_id = f"group_{req.session_id}"

    group_sessions[group_id] = {
        "student": req.session_id,
        "mentor": req.mentor_name,
        "messages": []
    }

    return {
        "group_id": group_id,
        "status": "accepted"
    }
@app.post("/group/message")
def send_group_message(msg: GroupMessage):

    group_sessions[msg.group_id]["messages"].append({
        "sender": msg.sender,
        "text": msg.text
    })

    return {"status":"ok"}
@app.get("/group/{group_id}")
def get_group(group_id:str):
    return group_sessions[group_id]