import { useState } from "react";
import ChatWindow from "./components/ChatWindow";
import RecommendationCard from "./components/RecommendationCard";

export default function App() {

const [selectedCourse, setSelectedCourse] =
useState(null);

const sessionId = "student-001";

return (


<div className="min-h-screen bg-zinc-900 text-white">

  <div className="h-screen p-6">

    <div className="grid grid-cols-12 gap-6 h-full">

      <div className="col-span-4 flex flex-col">

        <div
          className="
            flex-1
            bg-zinc-800
            border
            border-zinc-700
            rounded-3xl
            overflow-hidden
          "
        >

          <div className="px-6 py-5 border-b border-zinc-700">

            <h2 className="text-xl font-semibold">
              LEARNING PATH GỢI Ý
            </h2>

            <p className="text-zinc-400 text-sm mt-1">
              Chọn khóa học để trao đổi với DoDo
            </p>

          </div>

          <div className="flex-1 overflow-y-auto p-4">

            <RecommendationCard
              selectedCourse={selectedCourse}
              onSelectCourse={setSelectedCourse}
            />

          </div>

        </div>

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
          "
        >
          Kết nối Mentor
        </button>

      </div>

      <div className="col-span-8">

        <ChatWindow
          sessionId={sessionId}
          course={selectedCourse}
        />

      </div>

    </div>

  </div>

</div>


);

}
