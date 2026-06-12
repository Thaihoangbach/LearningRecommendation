from knowledge_graph import get_full_context

EXPERT_RULES = {
    "reason": [
        "Giải thích dựa trên similarity score và learning path, không tự suy diễn",
        "Giữ câu trả lời dưới 100 từ",
        "Đề cập đến mối liên hệ với các khóa học đã học trước",
    ],
    "benefit": [
        "Tập trung vào learning outcomes cụ thể từ KG",
        "Liên hệ với ứng dụng thực tế",
        "Không hứa hẹn kết quả không có trong dữ liệu",
    ],
    "content": [
        "Chỉ liệt kê topics có trong KG",
        "Không thêm nội dung ngoài dữ liệu",
        "Trình bày có cấu trúc rõ ràng",
    ],
    "relation": [
        "Dùng similarity scores để giải thích mức độ liên quan",
        "So sánh dựa trên domain và topics chung",
    ],
    "info": [
        "Cung cấp metadata chính xác từ KG",
        "Không ước đoán thông tin không có trong database",
    ],
    "context": [
        "Liên hệ với domain và learning outcomes thực tế",
        "Tránh generalize quá mức",
    ],
}

DOMAIN_DEFINITIONS = {
    "knowledge_graph": "Cấu trúc dữ liệu dạng đồ thị biểu diễn mối quan hệ giữa các khái niệm học tập",
    "similarity_score": "Điểm từ 0-1 biểu thị mức độ tương đồng giữa hai khóa học, tính bởi RE algorithm",
    "learning_path": "Trình tự các khóa học được sắp xếp tối ưu theo mức độ khó và phụ thuộc kiến thức",
    "domain_community": "Nhóm các khóa học thuộc cùng lĩnh vực, được kết nối trong Knowledge Graph",
}

def build_context(intent: str, course_id: str):
    kg = get_full_context(course_id)

    path = kg["learning_path"]

    try:
        path_position = path.index(course_id) + 1
    except ValueError:
        path_position = None

    return {
        "intent": intent,
        "course": kg["course"],
        "similar_courses": kg["similar_courses"],
        "domain_community": kg["domain_community"],
        "learning_path": path,
        "path_position": path_position,
        "path_length": len(path),
    }

def context_to_prompt_string(ctx):
    return f"""
ROLE
You are an explainable learning recommendation chatbot.

DEFINITIONS
Intent: {ctx['intent']}

RULES
1. Explain recommendations using knowledge graph evidence.
2. Use learning path information.
3. Be concise and educational.
4. If information is unavailable, say so.

SUPPORTING CONTENT

Current Course:
{ctx['course']}

Learning Path:
{ctx['learning_path']}

Current Position:
Step {ctx['path_position']} of {ctx['path_length']}

Similar Courses:
{ctx['similar_courses']}

Domain Community:
{ctx['domain_community']}
"""