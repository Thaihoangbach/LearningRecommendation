# Learning Path Recommendation & DoDo Learning Assistant

## Overview

Learning Path Recommendation & DoDo Learning Assistant là hệ thống mô phỏng một nền tảng học tập thông minh dựa trên Knowledge Graph, Recommender System và Large Language Models (LLMs).

Hệ thống đề xuất lộ trình học cá nhân hóa cho người học, đồng thời cung cấp chatbot DoDo để giải thích lý do đề xuất, nội dung khóa học, lợi ích học tập và mối liên hệ giữa các khóa học trong learning path.

Project được xây dựng như một prototype minh họa cho ý tưởng trong các nghiên cứu về:

* Explainable Recommendation Systems
* Knowledge Graph-based Learning Recommendation
* LLM-powered Educational Assistants
* Human-AI Collaborative Learning

---

## Main Features

### 1. Learning Path Recommendation

Hệ thống đề xuất chuỗi khóa học theo thứ tự học phù hợp.

Ví dụ:

1. Python for Beginners
2. Data Analysis with Python
3. Database Management
4. Machine Learning Basics

Người học có thể chọn từng khóa học để xem thông tin chi tiết và trao đổi với chatbot.

---

### 2. DoDo Learning Assistant

Chatbot hỗ trợ giải thích learning path bằng ngôn ngữ tự nhiên.

Các loại câu hỏi được hỗ trợ:

* Tại sao khóa học này được gợi ý?
* Tôi sẽ học được gì?
* Khóa học này có lợi ích gì?
* Khóa học này liên quan thế nào tới các khóa khác?
* Khóa học tiếp theo nên học là gì?

---

### 3. Intent Detection

Hệ thống phân loại câu hỏi người dùng thành các nhóm:

| Intent   | Ý nghĩa                   |
| -------- | ------------------------- |
| reason   | Lý do gợi ý               |
| content  | Nội dung khóa học         |
| benefit  | Lợi ích                   |
| relation | Quan hệ với khóa học khác |
| info     | Thông tin chung           |
| other    | Khác                      |

---

### 4. Mentor Escalation

Khi chatbot không đủ khả năng hỗ trợ:

* Sinh viên gửi yêu cầu mentor
* Mentor chấp nhận yêu cầu
* Hệ thống tạo group session
* Mentor và sinh viên có thể trao đổi trực tiếp

---

## System Architecture

### Frontend

* React
* Vite
* Tailwind CSS
* Axios

### Backend

* FastAPI
* Pydantic
* REST API

### AI Components

* Knowledge Graph
* Recommender System
* Intent Classification
* LLM-based Response Generator

---

## Project Structure

```text
project/
│
├── backend/
│   ├── .env
│   ├── data
│   │   ├── kg_ai_uet_demo.json
│   ├── kg
│   │   ├── graph_loader.py
│   │   ├── graph_query.py
│   │   ├── retriever.py
│   ├── context_builder.py
│   ├── intent_classifier.py
│   ├── llm_service.py
│   ├── main.py
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── ChatWindow.jsx
│   │   │   ├── RecommendationCard.jsx
│   │   │   ├── MessageBubble.jsx
│   │   │   └── MentorPanel.jsx
│   │   │
│   │   ├── api.js
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── index.css
│   │
│   ├── package.json
│   └── vite.config.js
│
└── README.md
```

---

## Installation

### Backend

```bash
cd backend

pip install -r requirements.txt

uvicorn main:app --reload --port 8000
```

Backend sẽ chạy tại:

```text
http://localhost:8000
```

---

### Frontend

```bash
cd frontend

npm install

npm run dev
```

Frontend sẽ chạy tại:

```text
http://localhost:5173
```







