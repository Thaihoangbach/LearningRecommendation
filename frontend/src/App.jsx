import { useState } from "react";
import ChatWindow from "./components/ChatWindow";
import RecommendationCard from "./components/RecommendationCard";

export default function App() {
  const [selectedCourse, setSelectedCourse] = useState(null);

  const sessionId = "student-001";

  return (
    <div className="h-screen bg-zinc-900 text-white">
      

        <div className="grid grid-cols-12 gap-6 h-full">

          {/* LEFT PANEL */}
          <div className="col-span-4 flex flex-col h-full min-h-0">

            {/* Course Panel */}
            <div className="
              flex-1
              min-h-0
              bg-zinc-800
              border
              border-zinc-700
              rounded-3xl
              flex
              flex-col
              overflow-hidden
            "
>
              {/* Header */}
              <div className="px-6 py-5 border-b border-zinc-700 shrink-0">
                <h2 className="text-xl font-semibold">
                  LEARNING PATH GỢI Ý
                </h2>

                <p className="text-zinc-400 text-sm mt-1">
                  Chọn khóa học để trao đổi với DoDo
                </p>
              </div>

              {/* Scroll riêng cho course list */}
              <div className="flex-1 min-h-0 overflow-y-auto p-4">
                <RecommendationCard
                  selectedCourse={selectedCourse}
                  onSelectCourse={setSelectedCourse}
                />
              </div>
            </div>

            {/* Mentor button luôn cố định */}
            <button
              onClick={() =>
                alert(
                  "Tính năng Mentor sẽ được mở rộng trong phiên bản tiếp theo."
                )
              }
              className="
                mt-4
                h-16
                rounded-2xl
                bg-emerald-100
                text-emerald-900
                font-semibold
                hover:bg-emerald-200
                transition
                shrink-0
              "
            >
              Kết nối Mentor
            </button>

          </div>

          {/* RIGHT PANEL */}
          <div className="col-span-8 h-full min-h-0">
            <ChatWindow
              sessionId={sessionId}
              course={selectedCourse}
            />
          </div>

        </div>

      </div>
  );
}