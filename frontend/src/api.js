import axios from "axios";
const BASE = "http://localhost:8000";

export const sendMessage = (session_id, text, course_id) =>
  axios.post(`${BASE}/chat`, { session_id, text, course_id }).then(r => r.data);

export const requestMentor = (session_id, student_name) =>
  axios.post(`${BASE}/mentor/request`, { session_id, student_name }).then(r => r.data);

export const getCourses = () =>
  axios.get(`${BASE}/courses`).then(r => r.data);