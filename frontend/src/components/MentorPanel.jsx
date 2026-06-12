import { useState, useEffect } from "react";
import axios from "axios";

const BASE = "http://localhost:8000";

export default function MentorPanel() {

  const [queue, setQueue] = useState([]);
  const [selected, setSelected] = useState(null);

  const [replyText, setReplyText] = useState("");

  const [groupId, setGroupId] = useState(null);

  async function fetchQueue() {
    try {
      const res = await axios.get(`${BASE}/mentor/queue`);
      setQueue(res.data);
    } catch (err) {
      console.error(err);
    }
  }

  useEffect(() => {
    fetchQueue();

    const interval = setInterval(fetchQueue, 3000);

    return () => clearInterval(interval);
  }, []);

  async function handleAccept() {

    if (!selected) return;

    try {

      const res = await axios.post(
        `${BASE}/mentor/accept`,
        {
          session_id: selected.session_id,
          mentor_name: "Prof. Mentor"
        }
      );

      setGroupId(res.data.group_id);

      alert(
        `Đã tạo Group Session: ${res.data.group_id}`
      );

    } catch (err) {
      console.error(err);
      alert("Không thể tạo group session");
    }
  }

  async function handleReply() {

    if (!selected) return;

    if (!replyText.trim()) return;

    try {

      await axios.post(
        `${BASE}/mentor/reply`,
        {
          session_id: selected.session_id,
          mentor_name: "Prof. Mentor",
          text: replyText
        }
      );

      setReplyText("");

      alert("Đã gửi phản hồi");

    } catch (err) {
      console.error(err);
      alert("Gửi phản hồi thất bại");
    }
  }

  return (
    <div className="bg-white rounded-2xl shadow p-6 space-y-6">

      <div>
        <h2 className="text-xl font-semibold">
          Mentor Dashboard
        </h2>

        <p className="text-sm text-gray-500">
          Quản lý yêu cầu hỗ trợ từ sinh viên
        </p>
      </div>

      <div>

        <h3 className="font-medium mb-3">
          Yêu cầu chờ ({queue.length})
        </h3>

        {queue.length === 0 ? (
          <div className="border rounded-xl p-6 text-center text-gray-400">
            Chưa có yêu cầu nào
          </div>
        ) : (

          <div className="space-y-3">

            {queue.map((req, idx) => (

              <div
                key={idx}
                onClick={() => setSelected(req)}
                className={`
                  cursor-pointer
                  border
                  rounded-xl
                  p-4
                  transition

                  ${
                    selected?.session_id === req.session_id
                      ? "border-indigo-500 bg-indigo-50"
                      : "border-gray-200 hover:border-indigo-300"
                  }
                `}
              >
                <div className="font-medium">
                  👤 {req.student_name}
                </div>

                <div className="text-xs text-gray-500">
                  Session: {req.session_id}
                </div>

              </div>

            ))}

          </div>

        )}

      </div>

      {selected && (

        <div className="border-t pt-5 space-y-4">

          <div>

            <p className="font-medium">
              Sinh viên:
              <span className="text-indigo-600 ml-1">
                {selected.student_name}
              </span>
            </p>

            <p className="text-xs text-gray-500">
              Session ID: {selected.session_id}
            </p>

          </div>

          <div className="flex gap-2">

            <button
              onClick={handleAccept}
              className="
                bg-green-600
                hover:bg-green-700
                text-white
                px-4
                py-2
                rounded-xl
              "
            >
              Accept & Create Group
            </button>

            <button
              onClick={() => setSelected(null)}
              className="
                border
                px-4
                py-2
                rounded-xl
              "
            >
              Hủy
            </button>

          </div>

          {groupId && (

            <div className="bg-green-50 border border-green-200 rounded-xl p-3">

              <p className="text-green-700 font-medium">
                Group Session đã được tạo
              </p>

              <p className="text-sm text-green-600">
                {groupId}
              </p>

            </div>

          )}

          <textarea
            value={replyText}
            onChange={(e) => setReplyText(e.target.value)}
            rows={4}
            placeholder="Nhập phản hồi cho sinh viên..."
            className="
              w-full
              border
              rounded-xl
              p-3
              resize-none
            "
          />

          <button
            onClick={handleReply}
            disabled={!replyText.trim()}
            className="
              w-full
              bg-indigo-600
              hover:bg-indigo-700
              text-white
              rounded-xl
              py-2
              disabled:opacity-50
            "
          >
            Gửi phản hồi
          </button>

        </div>

      )}

      <div className="bg-gray-50 rounded-xl p-4 text-sm text-gray-500">

        <div className="font-medium mb-2">
          Workflow theo bài báo
        </div>

        <ol className="list-decimal pl-5 space-y-1">
          <li>Sinh viên gửi yêu cầu hỗ trợ</li>
          <li>Mentor chọn sinh viên</li>
          <li>Mentor nhấn Accept</li>
          <li>Hệ thống tạo Group Session</li>
          <li>Student + Mentor + Chatbot cùng trao đổi</li>
        </ol>

      </div>

    </div>
  );
}