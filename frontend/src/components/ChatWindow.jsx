import { useState, useRef, useEffect } from "react";
import { sendMessage, requestMentor } from "../api";
import MessageBubble from "./MessageBubble";

export default function ChatWindow({
sessionId,
course
}) {

const [messages, setMessages] = useState([
{
role: "bot",
text:
"Xin chào!\n\nTôi là DoDo - trợ lý giải thích Learning Path.\n\nBạn có thể hỏi:\n• Tại sao khóa học này được gợi ý?\n• Tôi sẽ học được gì?\n• Khóa học này liên quan thế nào tới các khóa học khác?\n\nHãy chọn một khóa học ở bên trái và bắt đầu trò chuyện."
}
]);

const [input, setInput] = useState("");
const [loading, setLoading] = useState(false);

const bottomRef = useRef(null);

useEffect(() => {
bottomRef.current?.scrollIntoView({
behavior: "smooth"
});
}, [messages]);

async function handleSend() {


if (!input.trim()) return;

const userText = input;

setInput("");

setMessages(prev => [
  ...prev,
  {
    role: "user",
    text: userText
  }
]);

setLoading(true);

try {

  const res = await sendMessage(
    sessionId,
    userText,
    course?.id
  );

  setMessages(prev => [
    ...prev,
    {
      role: "bot",
      text: res.reply,
      intent: res.intent,
      suggest_mentor: res.suggest_mentor
    }
  ]);

} catch {

  setMessages(prev => [
    ...prev,
    {
      role: "bot",
      text:
        "Xin lỗi, hiện tại tôi không thể kết nối tới hệ thống."
    }
  ]);

}

setLoading(false);


}

async function handleMentorRequest() {


try {

  await requestMentor(
    sessionId,
    "Student"
  );

  setMessages(prev => [
    ...prev,
    {
      role: "system",
      text:
        "Đã gửi yêu cầu kết nối Mentor."
    }
  ]);

} catch {

  setMessages(prev => [
    ...prev,
    {
      role: "system",
      text:
        "Không thể gửi yêu cầu kết nối Mentor."
    }
  ]);

}


}

return (


<div
  className="
    h-full
    bg-zinc-800
    border
    border-zinc-700
    rounded-3xl
    overflow-hidden
    flex
    flex-col
  "
>

  {/* HEADER */}

  <div
    className="
      px-6
      py-5
      border-b
      border-zinc-700
      bg-zinc-800
    "
  >

    <div className="flex items-center gap-3">

      <div
        className="
          w-12
          h-12
          rounded-full
          bg-indigo-600
          flex
          items-center
          justify-center
          text-xl
        "
      >
      </div>

      <div>

        <h2 className="text-xl font-semibold text-white">
          DoDo
        </h2>

        <p className="text-sm text-zinc-400">
          Trợ lý giải thích Learning Path
        </p>

      </div>

    </div>

    <div
      className="
        mt-4
        inline-flex
        items-center
        rounded-full
        bg-zinc-700
        px-4
        py-2
        text-sm
        text-zinc-300
      "
    >
      Đang thảo luận:
      <span className="ml-2 text-white font-medium">
        {course?.title || "Chưa chọn khóa học"}
      </span>
    </div>

  </div>

  {/* MESSAGES */}

  <div
    className="
      flex-1
      overflow-y-auto
      p-6
      bg-zinc-900
      space-y-4
    "
  >

    {messages.map((m, i) => (

      <MessageBubble
        key={i}
        message={m}
        onMentorRequest={handleMentorRequest}
      />

    ))}

    {loading && (

      <div className="flex justify-start">

        <div
          className="
            bg-zinc-700
            text-zinc-300
            px-4
            py-3
            rounded-2xl
            animate-pulse
          "
        >
          DoDo đang suy nghĩ...
        </div>

      </div>

    )}

    <div ref={bottomRef} />

  </div>

  {/* INPUT */}

  <div
    className="
      border-t
      border-zinc-700
      p-5
      bg-zinc-800
    "
  >

    <div className="flex gap-3">

      <input
        value={input}
        onChange={(e) =>
          setInput(e.target.value)
        }
        onKeyDown={(e) =>
          e.key === "Enter" &&
          handleSend()
        }
        placeholder="Hỏi DoDo về khóa học này..."
        className="
          flex-1
          bg-zinc-700
          border
          border-zinc-600
          rounded-2xl
          px-4
          py-3
          text-white
          placeholder:text-zinc-400
          focus:outline-none
          focus:ring-2
          focus:ring-indigo-500
        "
      />

      <button
        onClick={handleSend}
        disabled={loading}
        className="
          px-6
          rounded-2xl
          bg-indigo-600
          hover:bg-indigo-500
          text-white
          font-medium
          disabled:opacity-50
        "
      >
        Gửi
      </button>

    </div>

  </div>

</div>

);
}
